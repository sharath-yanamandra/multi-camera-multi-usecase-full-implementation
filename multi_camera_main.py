# flexible_multi_camera_main.py - NEW MAIN LAUNCHER
# Launcher for flexible multi-camera system

import os
import sys
import argparse
import logging
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_banner():
    """Print application banner"""
    print("="*80)
    print(" 🎥 FLEXIBLE MULTI-CAMERA MONITORING SYSTEM")
    print("="*80)
    print(f" ⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" 🔧 Features: Multiple use cases per camera with easy enable/disable")
    print(f" 🎯 Control: Runtime enable/disable of specific models per camera")
    print("="*80)

def run_flexible_system():
    """Run the flexible multi-camera system"""
    try:
        # Import flexible components
        from interface.flexible_camera_management import FlexibleCameraConfigurationManager
        from core.flexible_multi_camera_processor import FlexibleMultiCameraProcessor
        from config.multi_camera_config import MultiCameraConfig
        
        print("🎥 Welcome to Flexible Multi-Camera System!")
        
        # Run configuration manager
        manager = FlexibleCameraConfigurationManager()
        camera_configs = manager.run_interactive_menu()
        
        if camera_configs:
            print(f"\n🚀 Starting Flexible Multi-Camera System with {len(camera_configs)} cameras...")
            
            # Show configuration summary
            print("\n📋 Configuration Summary:")
            for config in camera_configs:
                enabled_count = len(config.get('enabled_use_cases', []))
                available_count = len(config.get('available_use_cases', []))
                print(f"  📷 {config['camera_id']}: {enabled_count}/{available_count} models enabled")
                
                enabled_models = ", ".join([uc.replace('_', ' ').title() 
                                          for uc in config.get('enabled_use_cases', [])])
                print(f"      Active: {enabled_models}")
            
            # Create and start processor
            processor = FlexibleMultiCameraProcessor(MultiCameraConfig)
            processor.load_camera_configurations(camera_configs)
            
            print("\n🔄 Starting processing (Ctrl+C to stop)...")
            processor.start_processing()
            
        else:
            print("❌ No camera configurations provided")
    
    except KeyboardInterrupt:
        print("\n⏹️  System stopped by user")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you have created the flexible_multi_camera_processor.py file")
    except Exception as e:
        print(f"❌ System error: {e}")
        logging.getLogger(__name__).error(f"System error: {e}", exc_info=True)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Flexible Multi-Camera Monitoring System')
    
    parser.add_argument('command', nargs='?', default='run',
                       choices=['run', 'config', 'help'],
                       help='Command to execute')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        print_banner()
        
        if args.command == 'run':
            run_flexible_system()
        elif args.command == 'config':
            from interface.flexible_camera_management import FlexibleCameraConfigurationManager
            manager = FlexibleCameraConfigurationManager()
            manager.run_interactive_menu()
        elif args.command == 'help':
            print("\n🎯 Flexible Multi-Camera System Commands:")
            print("  python flexible_multi_camera_main.py run     - Start the system")
            print("  python flexible_multi_camera_main.py config  - Configure cameras only")
            print("  python flexible_multi_camera_main.py help    - Show this help")
            
            print("\n💡 Features:")
            print("  • Multiple use cases per camera")
            print("  • Easy enable/disable of specific models")
            print("  • Runtime configuration changes")
            print("  • Per-camera model selection")
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"❌ Application error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
# multi_camera_main.py - NEW FILE
# Main launcher for multi-camera system
'''
import os
import sys
import argparse
import logging
import time
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import your existing components
from config.multi_camera_config import MultiCameraConfig
from core.multi_camera_processor import MultiCameraProcessor
from core.database_handler import DatabaseHandler
from interface.camera_management import CameraConfigurationManager

def setup_logging(log_level='INFO'):
    """Setup logging for multi-camera system"""
    os.makedirs('logs', exist_ok=True)
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_file = os.path.join('logs', 'multi_camera_system.log')
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def print_banner():
    """Print application banner"""
    print("="*80)
    print(" 🎥 MULTI-CAMERA MONITORING SYSTEM")
    print("="*80)
    print(f" ⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" 🏗️  Architecture: Multiple cameras, specialized use cases")
    print(f" 🔧 Configuration: {MultiCameraConfig.MYSQL_DATABASE}")
    print(f" ☁️  Storage: {MultiCameraConfig.GCP_BUCKET_NAME}")
    print("="*80)

def validate_system_requirements():
    """Validate system requirements for multi-camera setup"""
    print("🔍 Validating system requirements...")
    
    errors = []
    warnings = []
    
    # Check model files
    required_models = [
        MultiCameraConfig.DETECTION_MODEL_PATH,
        MultiCameraConfig.PPE_DETECTION_MODEL_PATH,
        MultiCameraConfig.POSE_ESTIMATION_MODEL_PATH
    ]
    
    for model_path in required_models:
        if not os.path.exists(model_path):
            errors.append(f"Model not found: {model_path}")
        else:
            print(f"   ✅ Model found: {os.path.basename(model_path)}")
    
    # Check GCP credentials
    if not os.path.exists(MultiCameraConfig.GCP_CREDENTIALS_PATH):
        errors.append(f"GCP credentials not found: {MultiCameraConfig.GCP_CREDENTIALS_PATH}")
    else:
        print(f"   ✅ GCP credentials found")
    
    # Check database connectivity
    try:
        db = DatabaseHandler({
            'host': MultiCameraConfig.MYSQL_HOST,
            'user': MultiCameraConfig.MYSQL_USER,
            'password': MultiCameraConfig.MYSQL_PASSWORD,
            'database': MultiCameraConfig.MYSQL_DATABASE,
            'port': MultiCameraConfig.MYSQL_PORT
        })
        
        if db.connect():
            print(f"   ✅ Database connection successful")
            db.disconnect()
        else:
            errors.append("Database connection failed")
    except Exception as e:
        errors.append(f"Database connection error: {e}")
    
    # Check available memory
    try:
        import psutil
        memory = psutil.virtual_memory()
        available_gb = memory.available / (1024**3)
        
        if available_gb < 2:
            warnings.append(f"Low available memory: {available_gb:.1f}GB (recommended: 4GB+)")
        else:
            print(f"   ✅ Available memory: {available_gb:.1f}GB")
    except ImportError:
        warnings.append("psutil not available - cannot check memory usage")
    
    # Print results
    if errors:
        print("\n❌ SYSTEM VALIDATION FAILED:")
        for error in errors:
            print(f"   • {error}")
        return False
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   • {warning}")
    
    print("\n✅ System validation completed successfully!")
    return True

def load_camera_configurations(source='interactive'):
    """Load camera configurations from various sources"""
    
    if source == 'interactive':
        print("\n🎥 Loading camera configurations interactively...")
        manager = CameraConfigurationManager()
        return manager.run_interactive_menu()
    
    elif source == 'database':
        print("\n🎥 Loading camera configurations from database...")
        try:
            db = DatabaseHandler({
                'host': MultiCameraConfig.MYSQL_HOST,
                'user': MultiCameraConfig.MYSQL_USER,
                'password': MultiCameraConfig.MYSQL_PASSWORD,
                'database': MultiCameraConfig.MYSQL_DATABASE,
                'port': MultiCameraConfig.MYSQL_PORT
            })
            
            if db.connect():
                configs = MultiCameraConfig.load_camera_configurations_from_database(db)
                db.disconnect()
                return configs
            else:
                print("❌ Failed to connect to database")
                return None
        except Exception as e:
            print(f"❌ Error loading from database: {e}")
            return None
    
    elif source == 'file':
        print("\n🎥 Loading camera configurations from file...")
        config_file = "config/camera_configurations.json"
        
        if os.path.exists(config_file):
            try:
                import json
                with open(config_file, 'r') as f:
                    configs = json.load(f)
                print(f"✅ Loaded {len(configs)} camera configurations from file")
                return configs
            except Exception as e:
                print(f"❌ Error loading from file: {e}")
                return None
        else:
            print(f"❌ Configuration file not found: {config_file}")
            return None
    
    elif source == 'default':
        print("\n🎥 Using default camera configurations...")
        return MultiCameraConfig.create_default_camera_configurations()
    
    else:
        print(f"❌ Unknown configuration source: {source}")
        return None

def initialize_database_schema():
    """Initialize database schema for multi-camera system"""
    print("🗄️  Initializing database schema...")
    
    try:
        db = DatabaseHandler({
            'host': MultiCameraConfig.MYSQL_HOST,
            'user': MultiCameraConfig.MYSQL_USER,
            'password': MultiCameraConfig.MYSQL_PASSWORD,
            'database': MultiCameraConfig.MYSQL_DATABASE,
            'port': MultiCameraConfig.MYSQL_PORT
        })
        
        if db.connect():
            # Read and execute multi-camera schema
            schema_file = "config/multi_camera_database_setup.sql"
            
            if os.path.exists(schema_file):
                with open(schema_file, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                
                # Split and execute statements
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                
                for statement in statements:
                    if statement and not statement.startswith('--'):
                        try:
                            db.execute_query(statement)
                        except Exception as e:
                            print(f"⚠️  Statement warning: {e}")
                
                print("✅ Database schema initialized successfully")
                db.disconnect()
                return True
            else:
                print(f"❌ Schema file not found: {schema_file}")
                db.disconnect()
                return False
        else:
            print("❌ Failed to connect to database")
            return False
            
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

def start_multi_camera_system(camera_configs, run_time=None):
    """Start the multi-camera system"""
    
    if not camera_configs:
        print("❌ No camera configurations provided")
        return False
    
    print(f"\n🚀 Starting Multi-Camera System with {len(camera_configs)} cameras...")
    
    # Display camera summary
    print("\n📋 Camera Configuration Summary:")
    print("-" * 60)
    for config in camera_configs:
        print(f"  🎥 {config['camera_id']}: {config['name']}")
        print(f"      📍 Use Case: {config['use_case'].replace('_', ' ').title()}")
        print(f"      🔗 URL: {config['stream_url']}")
        print()
    
    try:
        # Create and configure processor
        processor = MultiCameraProcessor(MultiCameraConfig)
        processor.load_camera_configurations(camera_configs)
        
        # Start processing
        if run_time:
            print(f"⏱️  Running for {run_time} seconds...")
            
            import threading
            import time
            
            # Start processor in separate thread
            processor_thread = threading.Thread(target=processor.start_processing, daemon=True)
            processor_thread.start()
            
            # Wait for specified time
            time.sleep(run_time)
            
            # Stop processor
            processor.stop()
            processor_thread.join(timeout=10)
            
            print("✅ Multi-camera system test completed")
        else:
            print("🔄 Running continuously (Ctrl+C to stop)...")
            processor.start_processing()
        
        return True
        
    except KeyboardInterrupt:
        print("\n⏹️  System stopped by user")
        return True
    except Exception as e:
        print(f"❌ System error: {e}")
        logging.getLogger(__name__).error(f"System error: {e}", exc_info=True)
        return False

def run_system_diagnostics():
    """Run comprehensive system diagnostics"""
    print("\n🔧 Running System Diagnostics...")
    print("="*60)
    
    # Test database connection
    print("1. Testing database connection...")
    try:
        db = DatabaseHandler({
            'host': MultiCameraConfig.MYSQL_HOST,
            'user': MultiCameraConfig.MYSQL_USER,
            'password': MultiCameraConfig.MYSQL_PASSWORD,
            'database': MultiCameraConfig.MYSQL_DATABASE,
            'port': MultiCameraConfig.MYSQL_PORT
        })
        
        if db.connect():
            print("   ✅ Database connection successful")
            
            # Test camera configurations query
            configs = MultiCameraConfig.load_camera_configurations_from_database(db)
            print(f"   ✅ Found {len(configs)} camera configurations in database")
            
            db.disconnect()
        else:
            print("   ❌ Database connection failed")
    except Exception as e:
        print(f"   ❌ Database error: {e}")
    
    # Test GCP connection
    print("\n2. Testing GCP storage...")
    try:
        from core.gcp_uploader import GCPUploader
        
        uploader = GCPUploader(
            MultiCameraConfig.GCP_CREDENTIALS_PATH,
            MultiCameraConfig.GCP_BUCKET_NAME,
            MultiCameraConfig.GCP_PROJECT_ID
        )
        
        if uploader.test_connection():
            print("   ✅ GCP storage connection successful")
        else:
            print("   ❌ GCP storage connection failed")
        
        uploader.stop()
    except Exception as e:
        print(f"   ❌ GCP error: {e}")
    
    # Test YOLO model loading
    print("\n3. Testing YOLO model loading...")
    try:
        from ultralytics import YOLO
        
        model = YOLO(MultiCameraConfig.DETECTION_MODEL_PATH)
        print(f"   ✅ YOLO model loaded: {MultiCameraConfig.DETECTION_MODEL_PATH}")
        
        # Test inference on dummy data
        import numpy as np
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        results = model(dummy_frame, verbose=False)
        print("   ✅ YOLO inference test successful")
        
    except Exception as e:
        print(f"   ❌ YOLO model error: {e}")
    
    # Test camera model imports
    print("\n4. Testing camera model imports...")
    try:
        from camera_models.people_count_monitoring import PeopleCountingMonitor
        from camera_models.ppe_kit_monitoring import PPEDetector
        from camera_models.tailgating_zone_monitoring import TailgatingZoneMonitor
        from camera_models.intrusion_zone_monitoring import IntrusionZoneMonitor
        from camera_models.loitering_zone_monitoring import LoiteringZoneMonitor
        
        print("   ✅ All camera models imported successfully")
    except Exception as e:
        print(f"   ❌ Camera model import error: {e}")
    
    print("\n✅ System diagnostics completed")

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description='Multi-Camera Monitoring System')
    
    parser.add_argument('command', nargs='?', default='interactive',
                       choices=['interactive', 'start', 'config', 'diagnostics', 'init-db'],
                       help='Command to execute')
    
    parser.add_argument('--config-source', default='interactive',
                       choices=['interactive', 'database', 'file', 'default'],
                       help='Source for camera configurations')
    
    parser.add_argument('--log-level', default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level')
    
    parser.add_argument('--run-time', type=int,
                       help='Run time in seconds (for testing)')
    
    parser.add_argument('--validate-only', action='store_true',
                       help='Only validate system requirements')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        # Print banner
        print_banner()
        
        # Validate system requirements
        if not validate_system_requirements():
            print("\n❌ System validation failed. Please fix issues before continuing.")
            return 1
        
        if args.validate_only:
            print("\n✅ System validation completed - system is ready!")
            return 0
        
        # Execute command
        if args.command == 'interactive':
            # Load configurations and start system
            camera_configs = load_camera_configurations('interactive')
            
            if camera_configs:
                success = start_multi_camera_system(camera_configs, args.run_time)
                return 0 if success else 1
            else:
                print("❌ No camera configurations provided")
                return 1
        
        elif args.command == 'start':
            # Load configurations from specified source and start system
            camera_configs = load_camera_configurations(args.config_source)
            
            if camera_configs:
                success = start_multi_camera_system(camera_configs, args.run_time)
                return 0 if success else 1
            else:
                print("❌ Failed to load camera configurations")
                return 1
        
        elif args.command == 'config':
            # Run configuration manager only
            manager = CameraConfigurationManager()
            manager.run_interactive_menu()
            return 0
        
        elif args.command == 'diagnostics':
            # Run system diagnostics
            run_system_diagnostics()
            return 0
        
        elif args.command == 'init-db':
            # Initialize database schema
            success = initialize_database_schema()
            return 0 if success else 1
        
        else:
            parser.print_help()
            return 1
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Application stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        print(f"\n❌ Application error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

    '''