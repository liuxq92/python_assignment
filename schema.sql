CREATE DATABASE IF NOT EXISTS python_assignment;

USE python_assignment;

DROP TABLE IF EXISTS `financial_data`;

CREATE TABLE `financial_data`(
   `symbol` VARCHAR(256) NOT NULL,
   `date` VARCHAR(10) NOT NULL,
   `open_price` VARCHAR(100) NOT NULL,
   `close_price` VARCHAR(100) NOT NULL,
   `volume` VARCHAR(100) NOT NULL,
   PRIMARY KEY (`symbol`,  `date`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;