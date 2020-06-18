-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema me_etl
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema me_etl
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `me_etl` DEFAULT CHARACTER SET utf8 ;
USE `me_etl` ;

-- -----------------------------------------------------
-- Table `me_etl`.`headers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `me_etl`.`headers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content_length` VARCHAR(191) NULL,
  `via` VARCHAR(191) NULL,
  `connection` VARCHAR(191) NULL,
  `access_control_allow_credentials` VARCHAR(191) NULL,
  `content_type` VARCHAR(191) NULL,
  `server` VARCHAR(191) NULL,
  `access_control_allow_origin` VARCHAR(191) NULL,
  `accept` VARCHAR(45) NULL,
  `host` VARCHAR(45) NULL,
  `user_agent` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `me_etl`.`requests`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `me_etl`.`requests` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `method` VARCHAR(191) NOT NULL,
  `uri` VARCHAR(191) NULL,
  `url` VARCHAR(191) NOT NULL,
  `size` VARCHAR(191) NOT NULL,
  `querystring` VARCHAR(191) NULL,
  `headers_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_requests_headers1_idx` (`headers_id` ASC),
  CONSTRAINT `fk_requests_headers1`
    FOREIGN KEY (`headers_id`)
    REFERENCES `me_etl`.`headers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `me_etl`.`response`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `me_etl`.`response` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(191) NOT NULL,
  `size` VARCHAR(191) NOT NULL,
  `headers_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_response_headers1_idx` (`headers_id` ASC),
  CONSTRAINT `fk_response_headers1`
    FOREIGN KEY (`headers_id`)
    REFERENCES `me_etl`.`headers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `me_etl`.`consumer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `me_etl`.`consumer` (
  `id` VARCHAR(191) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `me_etl`.`services`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `me_etl`.`services` (
  `id` VARCHAR(191) NOT NULL,
  `connect_timeout` INT NOT NULL,
  `host` VARCHAR(191) NOT NULL,
  `name` VARCHAR(191) NOT NULL,
  `path` VARCHAR(191) NOT NULL,
  `port` INT NOT NULL,
  `protocol` VARCHAR(45) NOT NULL,
  `read_timeout` INT NOT NULL,
  `retries` INT NOT NULL,
  `write_timeout` INT NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `me_etl`.`routes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `me_etl`.`routes` (
  `id` VARCHAR(191) NOT NULL,
  `hosts` VARCHAR(191) NULL,
  `methods` TEXT NOT NULL,
  `paths` TEXT NOT NULL,
  `protocols` TEXT NOT NULL,
  `preserve_host` TINYINT(1) NOT NULL,
  `regex_priority` INT NOT NULL,
  `strip_path` TINYINT(1) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  `services_id` VARCHAR(191) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_routes_services1_idx` (`services_id` ASC),
  CONSTRAINT `fk_routes_services1`
    FOREIGN KEY (`services_id`)
    REFERENCES `me_etl`.`services` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `me_etl`.`latencies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `me_etl`.`latencies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `proxy` INT NOT NULL,
  `kong` INT NOT NULL,
  `request` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `me_etl`.`process`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `me_etl`.`process` (
  `id` INT NOT NULL,
  `upstream_uri_id` VARCHAR(191) NOT NULL,
  `client_ip` VARCHAR(45) NOT NULL,
  `started_at` DATETIME NOT NULL,
  `requests_id` INT NOT NULL,
  `response_id` INT NOT NULL,
  `consumer_id` VARCHAR(191) NOT NULL,
  `routes_id` VARCHAR(191) NOT NULL,
  `latencies_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_process_requests1_idx` (`requests_id` ASC),
  INDEX `fk_process_response1_idx` (`response_id` ASC),
  INDEX `fk_process_consumer1_idx` (`consumer_id` ASC),
  INDEX `fk_process_routes1_idx` (`routes_id` ASC),
  INDEX `fk_process_latencies1_idx` (`latencies_id` ASC),
  CONSTRAINT `fk_process_requests1`
    FOREIGN KEY (`requests_id`)
    REFERENCES `me_etl`.`requests` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_process_response1`
    FOREIGN KEY (`response_id`)
    REFERENCES `me_etl`.`response` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_process_consumer1`
    FOREIGN KEY (`consumer_id`)
    REFERENCES `me_etl`.`consumer` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_process_routes1`
    FOREIGN KEY (`routes_id`)
    REFERENCES `me_etl`.`routes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_process_latencies1`
    FOREIGN KEY (`latencies_id`)
    REFERENCES `me_etl`.`latencies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
