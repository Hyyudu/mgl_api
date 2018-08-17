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


-- Дамп структуры для представление magellan.v_nodes
DROP VIEW IF EXISTS `v_nodes`;
-- Создание временной таблицы для обработки ошибок зависимостей представлений
CREATE TABLE `v_nodes` (
	`id` INT(11) NOT NULL COMMENT 'ID узла',
	`model_id` INT(11) NOT NULL,
	`company` VARCHAR(3) NOT NULL COLLATE 'utf8_general_ci',
	`node_type_code` VARCHAR(50) NOT NULL COMMENT 'Код типа (shields, hull etc.)' COLLATE 'utf8_general_ci',
	`model_name` VARCHAR(50) NOT NULL COMMENT 'Наименования модели' COLLATE 'utf8_general_ci',
	`az_level` INT(11) NOT NULL COMMENT 'Уровень АЗ',
	`status` VARCHAR(10) NOT NULL COMMENT 'Статус' COLLATE 'utf8_general_ci',
	`date_created` DATETIME NOT NULL COMMENT 'Дата и время создания',
	`password` VARCHAR(50) NULL COLLATE 'utf8_general_ci',
	`flight_id` BIGINT(11) NULL
) ENGINE=MyISAM;


-- Дамп структуры для представление magellan.v_nodes
DROP VIEW IF EXISTS `v_nodes`;
-- Удаление временной таблицы и создание окончательной структуры представления
DROP TABLE IF EXISTS `v_nodes`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `v_nodes` AS select n.id,
	m.id model_id,
	m.company, 
	m.node_type_code,
	m.name model_name,
	n.az_level,
	n.`status`,
	n.date_created,
	n.password,
	if (f.status is not null, b.flight_id, Null) flight_id
from nodes n
join models m on n.model_id = m.id 
left join builds b on b.node_id = n.id 
left join flights f on f.id = b.flight_id and f.`status` in ('freight', 'prepare') ;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
