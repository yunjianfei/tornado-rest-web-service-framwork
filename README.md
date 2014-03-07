tornado-rest-web-service-framwork
=================================

Use tornado make rest web service

First, you must create database 'test', use Mysql.

Then, you must create table 'Host':

CREATE TABLE IF NOT EXISTS `test`.`Host` (
  `host_id` INT NOT NULL AUTO_INCREMENT,
  `host_type` INT NOT NULL DEFAULT 0,
  `hostname` VARCHAR(45) NULL,
  `ip` VARCHAR(45) NULL,
  `create_time` DATETIME NULL,
  `cpu_count` INT NULL,
  `memory` INT NULL,
  `os` VARCHAR(200) NULL,
  `worker_num` INT NOT NULL DEFAULT 6,
  `comment` VARCHAR(200) NULL,
  PRIMARY KEY (`host_id`),
  UNIQUE KEY `hostname` (`hostname`),
  UNIQUE KEY `ip` (`ip`))
ENGINE = InnoDB;


After create table, you can start the tornado server by master.py, the command is :
./master.py --port=9999

The port parameter can set by yourself.



