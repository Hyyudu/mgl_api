-- --------------------------------------------------------
-- Хост:                         127.0.0.1
-- Версия сервера:               10.1.22-MariaDB - mariadb.org binary distribution
-- ОС Сервера:                   Win32
-- HeidiSQL Версия:              9.3.0.4984
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Дамп структуры базы данных magellan
CREATE DATABASE IF NOT EXISTS `magellan` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `magellan`;


-- Дамп структуры для представление magellan.v_builds
-- Создание временной таблицы для обработки ошибок зависимостей представлений
CREATE TABLE `v_builds` (
	`flight_id` INT(11) NOT NULL COMMENT 'ID полета',
	`node_type_code` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
	`node_id` INT(11) NOT NULL COMMENT 'ID узла',
	`node_name` VARCHAR(50) NULL COMMENT 'Название (только для корпусов)' COLLATE 'utf8_general_ci',
	`model_id` INT(11) NOT NULL COMMENT 'ID модели',
	`model_name` VARCHAR(50) NOT NULL COMMENT 'Наименования модели' COLLATE 'utf8_general_ci',
	`company` VARCHAR(3) NOT NULL COLLATE 'utf8_general_ci',
	`level` SMALLINT(6) NOT NULL COMMENT 'Уровень модели',
	`az_level` INT(11) NOT NULL COMMENT 'Уровень АЗ',
	`size` ENUM('small','medium','large') NOT NULL COLLATE 'utf8_general_ci',
	`hull_vector` VARCHAR(16) NULL COLLATE 'utf8_general_ci',
	`node_vector` VARCHAR(16) NULL COLLATE 'utf8_general_ci',
	`vector` VARCHAR(16) NULL COMMENT 'Вектор рассинхрона (узел xor корпус)' COLLATE 'utf8_general_ci',
	`correction` VARCHAR(16) NULL COMMENT 'Вектор корректировки' COLLATE 'utf8_general_ci',
	`correction_func` VARCHAR(100) NULL COLLATE 'utf8_general_ci',
	`total` VARCHAR(16) NULL COMMENT 'Итоговый вектор' COLLATE 'utf8_general_ci',
	`params_json` TEXT NULL COMMENT 'JSON с получившимися параметрами' COLLATE 'utf8_general_ci',
	`slots_json` TEXT NULL COLLATE 'utf8_general_ci'
) ENGINE=MyISAM;


-- Дамп структуры для представление magellan.v_builds
-- Удаление временной таблицы и создание окончательной структуры представления
DROP TABLE IF EXISTS `v_builds`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `v_builds` AS SELECT `b`.`flight_id` AS `flight_id`,`b`.`node_type_code` AS `node_type_code`,`b`.`node_id` AS `node_id`,`n`.`name` AS `node_name`,`n`.`model_id` AS `model_id`,`m`.`name` AS `model_name`,`m`.`company` AS `company`,`m`.`level` AS `level`, n.az_level, `m`.`size` AS `size`,`hv`.`vector` AS `hull_vector`,`bv`.`vector` AS `node_vector`,`b`.`vector` AS `vector`,`b`.`correction` AS `correction`,`b`.`correction_func` AS `correction_func`,`b`.`total` AS `total`,`b`.`params_json` AS `params_json`,`b`.`slots_json` AS `slots_json`
FROM (((((`builds` `b`
JOIN `nodes` `n` ON((`n`.`id` = `b`.`node_id`)))
JOIN `models` `m` ON((`m`.`id` = `n`.`model_id`)))
JOIN `builds` `b_hull` ON(((`b`.`flight_id` = `b_hull`.`flight_id`) AND (`b_hull`.`node_type_code` = 'hull'))))
LEFT JOIN `hull_vectors` `hv` ON(((`hv`.`hull_id` = `b_hull`.`node_id`) AND (`hv`.`node_type_code` = `b`.`node_type_code`))))
LEFT JOIN `base_freq_vectors` `bv` ON(((`bv`.`company` = `m`.`company`) AND (`bv`.`node_code` = `b`.`node_type_code`) AND (`bv`.`level` = `m`.`level`) AND (`bv`.`size` = `m`.`size`)))) ;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
