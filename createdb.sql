-- creates clean database for smartfiets
DROP USER IF EXISTS 'sensem'@'localhost';
DROP DATABASE IF EXISTS smartfiets;
CREATE DATABASE smartfiets;
USE smartfiets;
CREATE TABLE gps_locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    longitude DECIMAL(9, 6) DEFAULT NULL,
    latitude DECIMAL(8, 6) DEFAULT NULL
);
CREATE TABLE gyro_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE USER 'sensem'@'localhost' IDENTIFIED BY 'h@';
GRANT INSERT ON smartfiets.gps_locations TO 'sensem'@'localhost';
GRANT SELECT ON smartfiets.* TO 'sensem'@'localhost';
GRANT DELETE ON smartfiets.* TO 'sensem'@'localhost';
