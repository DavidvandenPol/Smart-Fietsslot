-- creates clean database for weerstation 
DROP USER IF EXISTS 'sensem'@'localhost';
DROP DATABASE IF EXISTS smartfiets;
CREATE DATABASE smartfiets;
USE smartfiets;
CREATE TABLE locatiedata (
  id INT(11) NOT NULL AUTO_INCREMENT,
  naam VARCHAR(45),
  eenheid VARCHAR(45),
  PRIMARY KEY (id)
); 
CREATE USER 'sensem'@'localhost' IDENTIFIED BY 'h@';
GRANT SELECT ON smartfiets.* TO 'sensem'@'localhost';
