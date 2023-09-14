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
CREATE TABLE gyro_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    islocked boolean not null default 0
);
CREATE TABLE gyro_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    notification BOOLEAN DEFAULT FALSE
);


CREATE USER 'sensem'@'localhost' IDENTIFIED BY 'h@';
GRANT INSERT ON smartfiets.gps_locations TO 'sensem'@'localhost';
GRANT INSERT ON smartfiets.gyro_status TO 'sensem'@'localhost';
GRANT UPDATE ON smartfiets.gyro_status TO 'sensem'@'localhost';
GRANT INSERT ON smartfiets.gyro_notifications TO 'sensem'@'localhost';
GRANT UPDATE ON smartfiets.gyro_notifications TO 'sensem'@'localhost';
GRANT SELECT ON smartfiets.* TO 'sensem'@'localhost';
GRANT DELETE ON smartfiets.* TO 'sensem'@'localhost';
