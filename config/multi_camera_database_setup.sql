-- config/multi_camera_database_setup.sql (FIXED VERSION)
-- MySQL compatible schema for multi-camera system

USE dc_test;

-- Add columns to cameras table (MySQL compatible way)
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='cameras' AND COLUMN_NAME='primary_use_case') > 0,
    'SELECT "Column primary_use_case already exists"',
    'ALTER TABLE cameras ADD COLUMN primary_use_case VARCHAR(100) DEFAULT ''people_counting'''
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='cameras' AND COLUMN_NAME='zone_configuration') > 0,
    'SELECT "Column zone_configuration already exists"',
    'ALTER TABLE cameras ADD COLUMN zone_configuration JSON DEFAULT NULL'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='cameras' AND COLUMN_NAME='processing_rules') > 0,
    'SELECT "Column processing_rules already exists"',
    'ALTER TABLE cameras ADD COLUMN processing_rules JSON DEFAULT NULL'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='cameras' AND COLUMN_NAME='connection_status') > 0,
    'SELECT "Column connection_status already exists"',
    'ALTER TABLE cameras ADD COLUMN connection_status ENUM(''connected'', ''disconnected'', ''error'') DEFAULT ''disconnected'''
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='cameras' AND COLUMN_NAME='last_seen') > 0,
    'SELECT "Column last_seen already exists"',
    'ALTER TABLE cameras ADD COLUMN last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Create camera_use_cases table
CREATE TABLE IF NOT EXISTS camera_use_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    camera_id INT NOT NULL,
    use_case VARCHAR(100) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    configuration JSON DEFAULT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (camera_id) REFERENCES cameras(camera_id) ON DELETE CASCADE,
    UNIQUE KEY unique_camera_use_case (camera_id, use_case)
);

-- Create camera_health table
CREATE TABLE IF NOT EXISTS camera_health (
    health_id INT AUTO_INCREMENT PRIMARY KEY,
    camera_id INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    connection_status ENUM('connected', 'disconnected', 'error') NOT NULL,
    fps DECIMAL(5,2) DEFAULT 0.00,
    frames_processed INT DEFAULT 0,
    events_detected INT DEFAULT 0,
    cpu_usage DECIMAL(5,2) DEFAULT 0.00,
    memory_usage DECIMAL(5,2) DEFAULT 0.00,
    error_message TEXT DEFAULT NULL,
    FOREIGN KEY (camera_id) REFERENCES cameras(camera_id) ON DELETE CASCADE,
    INDEX idx_camera_timestamp (camera_id, timestamp)
);

-- Add columns to events table
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='events' AND COLUMN_NAME='camera_name') > 0,
    'SELECT "Column camera_name already exists"',
    'ALTER TABLE events ADD COLUMN camera_name VARCHAR(255) DEFAULT NULL'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='events' AND COLUMN_NAME='processing_time_ms') > 0,
    'SELECT "Column processing_time_ms already exists"',
    'ALTER TABLE events ADD COLUMN processing_time_ms INT DEFAULT NULL'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='events' AND COLUMN_NAME='model_version') > 0,
    'SELECT "Column model_version already exists"',
    'ALTER TABLE events ADD COLUMN model_version VARCHAR(50) DEFAULT NULL'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Create system_performance table
CREATE TABLE IF NOT EXISTS system_performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_cameras INT DEFAULT 0,
    active_cameras INT DEFAULT 0,
    total_fps DECIMAL(8,2) DEFAULT 0.00,
    total_events_per_minute INT DEFAULT 0,
    cpu_usage_percent DECIMAL(5,2) DEFAULT 0.00,
    memory_usage_percent DECIMAL(5,2) DEFAULT 0.00,
    disk_usage_percent DECIMAL(5,2) DEFAULT 0.00,
    gpu_usage_percent DECIMAL(5,2) DEFAULT 0.00,
    pending_uploads INT DEFAULT 0,
    INDEX idx_timestamp (timestamp)
);

-- Update existing project for multi-camera
INSERT IGNORE INTO projects (project_id, user_id, name, description, type, location, status)
VALUES 
('multi-cam-project-001', 'admin-user', 'Multi-Camera Monitoring System', 
 'Production multi-camera system with specialized use cases per camera', 'multi_camera_production', 'Main Facility', 'active');

-- Insert initial system performance record
INSERT IGNORE INTO system_performance (
    total_cameras, active_cameras, total_fps, total_events_per_minute,
    cpu_usage_percent, memory_usage_percent, disk_usage_percent, gpu_usage_percent
) VALUES (0, 0, 0.0, 0, 0.0, 0.0, 0.0, 0.0);

-- Verify the setup
SELECT 'Multi-Camera Database Setup Completed!' AS Status;

-- Show current camera table structure
SELECT 'Camera table structure updated successfully!' AS Info;
DESCRIBE cameras;

SELECT 'Database ready for multi-camera system!' AS Ready;