-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema certificacion
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema certificacion
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `certificacion` DEFAULT CHARACTER SET utf8 ;
USE `certificacion` ;

-- -----------------------------------------------------
-- Table `certificacion`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `certificacion`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `certificacion`.`peliculas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `certificacion`.`peliculas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_pelicula` VARCHAR(45) NULL,
  `director` VARCHAR(45) NULL,
  `fecha_estreno` VARCHAR(45) NULL,
  `sinopsis` TEXT NULL,
  `usuario_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_peliculas_usuarios_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_peliculas_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `certificacion`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `certificacion`.`comentarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `certificacion`.`comentarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `comentario` TEXT NOT NULL,
  `usuario_id` INT NOT NULL,
  `pelicula_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comentarios_usuarios_idx` (`usuario_id` ASC) VISIBLE,
  INDEX `fk_comentarios_peliculas1_idx` (`pelicula_id` ASC) VISIBLE,
  CONSTRAINT `fk_comentarios_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `certificacion`.`usuarios` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_comentarios_peliculas1`
    FOREIGN KEY (`pelicula_id`)
    REFERENCES `certificacion`.`peliculas` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;