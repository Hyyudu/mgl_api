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


-- Дамп структуры для таблица magellan.nodes
CREATE TABLE IF NOT EXISTS `nodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID узла',
  `model_id` int(11) NOT NULL DEFAULT '0' COMMENT 'ID модели',
  `name` varchar(50) DEFAULT '' COMMENT 'Название (только для корпусов)',
  `az_level` int(11) NOT NULL DEFAULT '100' COMMENT 'Уровень АЗ',
  `status` varchar(10) NOT NULL DEFAULT 'free' COMMENT 'Статус',
  `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата и время создания',
  `connected_to_hull_id` int(11) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `premium_expires` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_status_code` (`status`),
  KEY `FK_model_id` (`model_id`),
  CONSTRAINT `FK_model_id` FOREIGN KEY (`model_id`) REFERENCES `models` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_status_code` FOREIGN KEY (`status`) REFERENCES `node_statuses` (`code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=283 DEFAULT CHARSET=utf8 COMMENT='Узлы в технопарке';

-- Дамп данных таблицы magellan.nodes: ~160 rows (приблизительно)
DELETE FROM `nodes`;
/*!40000 ALTER TABLE `nodes` DISABLE KEYS */;
INSERT INTO `nodes` (`id`, `model_id`, `name`, `az_level`, `status`, `date_created`, `connected_to_hull_id`, `password`, `premium_expires`) VALUES
	(101, 101, '', 4, 'free', '2018-08-06 21:38:39', NULL, '', '2018-01-01 00:00:00'),
	(102, 102, '', 0, 'free', '2018-08-06 21:38:39', NULL, '', '2018-01-01 00:00:00'),
	(103, 103, '', 13, 'free', '2018-08-06 21:38:40', NULL, '', '2018-01-01 00:00:00'),
	(104, 104, '', 52, 'free', '2018-08-06 21:38:40', NULL, '', '2018-01-01 00:00:00'),
	(105, 105, '', 64, 'free', '2018-08-06 21:38:40', NULL, '', '2018-01-01 00:00:00'),
	(106, 106, '', 0, 'free', '2018-08-06 21:38:41', NULL, '', '2018-01-01 00:00:00'),
	(107, 107, '', 0, 'free', '2018-08-06 21:38:41', NULL, '', '2018-01-01 00:00:00'),
	(108, 108, '', 91, 'free', '2018-08-06 21:38:41', NULL, '', '2018-01-01 00:00:00'),
	(109, 109, '', 92, 'free', '2018-08-06 21:38:41', NULL, '', '2018-01-01 00:00:00'),
	(110, 110, '', 0, 'free', '2018-08-06 21:38:42', NULL, '', '2018-01-01 00:00:00'),
	(111, 111, '', 28, 'free', '2018-08-06 21:38:42', NULL, '', '2018-01-01 00:00:00'),
	(112, 112, '', 0, 'free', '2018-08-06 21:38:42', NULL, '', '2018-01-01 00:00:00'),
	(113, 113, '', 2, 'free', '2018-08-06 21:38:42', NULL, '', '2018-01-01 00:00:00'),
	(114, 114, '', 21, 'free', '2018-08-06 21:38:43', NULL, '', '2018-01-01 00:00:00'),
	(115, 115, '', 0, 'free', '2018-08-06 21:38:43', NULL, '', '2018-01-01 00:00:00'),
	(116, 116, '', 0, 'free', '2018-08-06 21:38:43', NULL, '', '2018-01-01 00:00:00'),
	(117, 117, '', 49, 'free', '2018-08-06 21:38:43', NULL, '', '2018-01-01 00:00:00'),
	(118, 118, '', 39, 'free', '2018-08-06 21:38:44', NULL, '', '2018-01-01 00:00:00'),
	(119, 119, '', 71, 'free', '2018-08-06 21:38:44', NULL, '', '2018-01-01 00:00:00'),
	(120, 120, '', 0, 'free', '2018-08-06 21:38:44', NULL, '', '2018-01-01 00:00:00'),
	(121, 121, '', 0, 'free', '2018-08-06 21:38:45', NULL, '', '2018-01-01 00:00:00'),
	(122, 122, '', -3, 'free', '2018-08-06 21:38:45', NULL, '', '2018-01-01 00:00:00'),
	(123, 123, '', 52, 'free', '2018-08-06 21:38:45', NULL, '', '2018-01-01 00:00:00'),
	(124, 124, '', 6, 'free', '2018-08-06 21:38:45', NULL, '', '2018-01-01 00:00:00'),
	(125, 125, '', 16, 'free', '2018-08-06 21:38:46', NULL, '', '2018-01-01 00:00:00'),
	(126, 126, '', 0, 'free', '2018-08-06 21:38:46', NULL, '', '2018-01-01 00:00:00'),
	(127, 127, '', 91, 'free', '2018-08-06 21:38:46', NULL, '', '2018-01-01 00:00:00'),
	(128, 128, '', 100, 'free', '2018-08-06 21:38:46', NULL, '', '2018-01-01 00:00:00'),
	(129, 129, '', 91, 'free', '2018-08-06 21:38:47', NULL, '', '2018-01-01 00:00:00'),
	(130, 130, '', 100, 'free', '2018-08-06 21:38:47', NULL, '', '2018-01-01 00:00:00'),
	(131, 131, '', 37, 'free', '2018-08-06 21:38:47', NULL, '', '2018-01-01 00:00:00'),
	(132, 132, '', 100, 'free', '2018-08-06 21:38:47', NULL, '', '2018-01-01 00:00:00'),
	(133, 133, '', 106, 'free', '2018-08-06 21:38:48', NULL, '', '2018-01-01 00:00:00'),
	(134, 134, '', 81, 'free', '2018-08-06 21:38:48', NULL, '', '2018-01-01 00:00:00'),
	(135, 135, '', 115, 'free', '2018-08-06 21:38:48', NULL, '', '2018-01-01 00:00:00'),
	(136, 136, '', 100, 'free', '2018-08-06 21:38:48', NULL, '', '2018-01-01 00:00:00'),
	(137, 137, '', 100, 'free', '2018-08-06 21:38:48', NULL, '', '2018-01-01 00:00:00'),
	(138, 138, '', 37, 'free', '2018-08-06 21:38:49', NULL, '', '2018-01-01 00:00:00'),
	(139, 139, '', 29, 'free', '2018-08-06 21:38:49', NULL, '', '2018-01-01 00:00:00'),
	(140, 140, '', 100, 'free', '2018-08-06 21:38:49', NULL, '', '2018-01-01 00:00:00'),
	(141, 141, '', 100, 'free', '2018-08-06 21:38:49', NULL, '', '2018-01-01 00:00:00'),
	(142, 142, '', 100, 'free', '2018-08-06 21:38:50', NULL, '', '2018-01-01 00:00:00'),
	(143, 143, '', -6, 'free', '2018-08-06 21:38:50', NULL, '', '2018-01-01 00:00:00'),
	(144, 144, '', -32, 'free', '2018-08-06 21:38:50', NULL, '', '2018-01-01 00:00:00'),
	(145, 145, '', 115, 'free', '2018-08-06 21:38:51', NULL, '', '2018-01-01 00:00:00'),
	(146, 146, '', 100, 'free', '2018-08-06 21:38:51', NULL, '', '2018-01-01 00:00:00'),
	(147, 147, '', 0, 'free', '2018-08-06 21:38:51', NULL, '', '2018-01-01 00:00:00'),
	(148, 148, '', 0, 'free', '2018-08-06 21:38:52', NULL, '', '2018-01-01 00:00:00'),
	(149, 149, '', 0, 'free', '2018-08-06 21:38:52', NULL, '', '2018-01-01 00:00:00'),
	(150, 150, '', 100, 'decomm', '2018-08-06 21:38:52', NULL, '', '2018-01-01 00:00:00'),
	(151, 151, '', 48, 'free', '2018-08-06 21:38:52', NULL, '', '2018-01-01 00:00:00'),
	(152, 152, '', 100, 'decomm', '2018-08-06 21:38:53', NULL, '', '2018-01-01 00:00:00'),
	(153, 153, '', 0, 'free', '2018-08-06 21:38:53', NULL, '', '2018-01-01 00:00:00'),
	(154, 154, '', 9, 'free', '2018-08-06 21:38:53', NULL, '', '2018-01-01 00:00:00'),
	(155, 155, '', -72, 'free', '2018-08-06 21:38:54', NULL, '', '2018-01-01 00:00:00'),
	(156, 156, '', 25, 'free', '2018-08-06 21:38:54', NULL, '', '2018-01-01 00:00:00'),
	(157, 157, '', 42, 'free', '2018-08-06 21:38:54', NULL, '', '2018-01-01 00:00:00'),
	(158, 158, '', 49, 'free', '2018-08-06 21:38:54', NULL, '', '2018-01-01 00:00:00'),
	(159, 159, '', 2, 'free', '2018-08-06 21:38:54', NULL, '', '2018-01-01 00:00:00'),
	(160, 160, '', 100, 'decomm', '2018-08-06 21:38:55', NULL, '', '2018-01-01 00:00:00'),
	(161, 161, '', 25, 'free', '2018-08-06 21:38:55', NULL, '', '2018-01-01 00:00:00'),
	(162, 162, '', 13, 'free', '2018-08-06 21:38:55', NULL, '', '2018-01-01 00:00:00'),
	(163, 163, '', 52, 'free', '2018-08-06 21:38:56', NULL, '', '2018-01-01 00:00:00'),
	(164, 164, '', 32, 'free', '2018-08-06 21:38:56', NULL, '', '2018-01-01 00:00:00'),
	(165, 165, '', 34, 'free', '2018-08-06 21:38:56', NULL, '', '2018-01-01 00:00:00'),
	(166, 166, '', 61, 'free', '2018-08-06 21:38:56', NULL, '', '2018-01-01 00:00:00'),
	(167, 167, '', 11, 'decomm', '2018-08-06 21:38:56', NULL, '', '2018-01-01 00:00:00'),
	(168, 168, '', 82, 'free', '2018-08-06 21:38:57', NULL, '', '2018-01-01 00:00:00'),
	(169, 169, '', 91, 'free', '2018-08-06 21:38:57', NULL, '', '2018-01-01 00:00:00'),
	(170, 170, '', 51, 'free', '2018-08-06 21:38:57', NULL, '', '2018-01-01 00:00:00'),
	(171, 171, '', 58, 'free', '2018-08-06 21:38:57', NULL, '', '2018-01-01 00:00:00'),
	(172, 172, 'Нинья-172', 100, 'decomm', '2018-08-06 21:38:58', NULL, '', '2018-01-01 00:00:00'),
	(173, 173, 'Пинта-173', 100, 'free', '2018-08-06 21:38:59', NULL, '', '2018-01-01 00:00:00'),
	(174, 174, 'Санта-Мария-174', 85, 'free', '2018-08-06 21:39:00', NULL, '', '2018-01-01 00:00:00'),
	(175, 175, 'Adventureland-175', 100, 'free', '2018-08-06 21:39:01', NULL, '', '2018-01-01 00:00:00'),
	(176, 176, 'Mickey\'s Toontown-176', 100, 'free', '2018-08-06 21:39:02', NULL, '', '2018-01-01 00:00:00'),
	(177, 177, 'Ленинград-5-177', 70, 'free', '2018-08-06 21:39:03', NULL, '', '2018-01-01 00:00:00'),
	(178, 178, 'Ленинград-3-178', 115, 'free', '2018-08-06 21:39:04', NULL, '', '2018-01-01 00:00:00'),
	(179, 179, 'МСТ-М4-179', 115, 'free', '2018-08-06 21:39:04', NULL, '', '2018-01-01 00:00:00'),
	(180, 180, 'Unity-180', 100, 'decomm', '2018-08-06 21:39:06', NULL, '', '2018-01-01 00:00:00'),
	(181, 181, 'Cutis-S-181', 100, 'free', '2018-08-06 21:39:07', NULL, '', '2018-01-01 00:00:00'),
	(182, 182, 'Cutis-M-182', 100, 'free', '2018-08-06 21:39:08', NULL, '', '2018-01-01 00:00:00'),
	(183, 183, 'Cutis-L-183', 70, 'free', '2018-08-06 21:39:10', NULL, '', '2018-01-01 00:00:00'),
	(184, 184, '', 28, 'free', '2018-08-06 21:39:11', NULL, '', '2018-01-01 00:00:00'),
	(185, 185, '', 100, 'decomm', '2018-08-06 21:39:11', NULL, '', '2018-01-01 00:00:00'),
	(186, 186, '', 100, 'free', '2018-08-06 21:39:11', NULL, '', '2018-01-01 00:00:00'),
	(187, 187, '', 21, 'free', '2018-08-06 21:39:12', NULL, '', '2018-01-01 00:00:00'),
	(188, 188, '', 43, 'free', '2018-08-06 21:39:12', NULL, '', '2018-01-01 00:00:00'),
	(189, 189, '', 8, 'free', '2018-08-06 21:39:12', NULL, '', '2018-01-01 00:00:00'),
	(190, 190, '', 40, 'free', '2018-08-06 21:39:12', NULL, '', '2018-01-01 00:00:00'),
	(191, 191, '', 0, 'decomm', '2018-08-06 21:39:12', NULL, '', '2018-01-01 00:00:00'),
	(192, 192, '', 66, 'free', '2018-08-06 21:39:13', NULL, '', '2018-01-01 00:00:00'),
	(193, 193, '', 5, 'free', '2018-08-06 21:39:13', NULL, '', '2018-01-01 00:00:00'),
	(194, 194, '', 0, 'free', '2018-08-06 21:39:13', NULL, '', '2018-01-01 00:00:00'),
	(195, 195, '', 46, 'free', '2018-08-06 21:39:13', NULL, '', '2018-01-01 00:00:00'),
	(215, 107, '', 100, 'decomm', '2018-08-16 00:49:36', NULL, '', '2018-01-01 00:00:00'),
	(216, 116, '', 100, 'decomm', '2018-08-16 00:50:23', NULL, '', '2018-01-01 00:00:00'),
	(218, 177, 'Ленинград-5-218', 115, 'decomm', '2018-08-16 09:55:42', NULL, '', '2018-01-01 00:00:00'),
	(219, 177, 'Ленинград-5-219', 70, 'free', '2018-08-16 09:55:45', NULL, '', '2018-01-01 00:00:00'),
	(220, 177, 'Ленинград-5-220', 85, 'free', '2018-08-16 09:57:54', NULL, '', '2018-01-01 00:00:00'),
	(221, 190, '', 115, 'free', '2018-08-16 09:59:53', NULL, '', '2018-01-01 00:00:00'),
	(222, 152, '', 37, 'free', '2018-08-16 10:42:24', NULL, '', '2018-01-01 00:00:00'),
	(223, 177, 'Ленинград-5-223', 85, 'free', '2018-08-16 11:28:27', NULL, '', '2018-01-01 00:00:00'),
	(224, 177, 'Ленинград-5-224', 100, 'free', '2018-08-16 12:00:04', NULL, '', '2018-01-01 00:00:00'),
	(225, 217, 'Offspring-L-225', 70, 'free', '2018-08-16 12:05:33', NULL, '', '2018-01-01 00:00:00'),
	(226, 218, 'Offspring-L-226', 70, 'free', '2018-08-16 12:05:43', NULL, '', '2018-01-01 00:00:00'),
	(227, 126, '', -17, 'free', '2018-08-16 12:11:51', NULL, '', '2018-01-01 00:00:00'),
	(228, 219, '', 100, 'decomm', '2018-08-16 12:40:27', NULL, '', '2018-01-01 00:00:00'),
	(229, 220, '', 100, 'decomm', '2018-08-16 12:40:29', NULL, '', '2018-01-01 00:00:00'),
	(230, 222, '', 100, 'decomm', '2018-08-16 12:40:55', NULL, '', '2018-01-01 00:00:00'),
	(231, 221, '', 100, 'decomm', '2018-08-16 12:40:55', NULL, '', '2018-01-01 00:00:00'),
	(232, 223, '', 100, 'decomm', '2018-08-16 12:41:19', NULL, '', '2018-01-01 00:00:00'),
	(233, 224, '', 100, 'decomm', '2018-08-16 12:41:25', NULL, '', '2018-01-01 00:00:00'),
	(234, 225, '', 100, 'decomm', '2018-08-16 12:41:38', NULL, '', '2018-01-01 00:00:00'),
	(235, 226, '', 100, 'decomm', '2018-08-16 12:42:12', NULL, '', '2018-01-01 00:00:00'),
	(236, 227, '', 0, 'free', '2018-08-16 12:42:42', NULL, '', '2018-01-01 00:00:00'),
	(237, 228, '', 31, 'free', '2018-08-16 12:43:11', NULL, '', '2018-01-01 00:00:00'),
	(238, 229, '', 6, 'free', '2018-08-16 12:43:20', NULL, '', '2018-01-01 00:00:00'),
	(239, 230, '', 100, 'decomm', '2018-08-16 12:43:49', NULL, '', '2018-01-01 00:00:00'),
	(240, 231, '', 0, 'free', '2018-08-16 12:45:08', NULL, '', '2018-01-01 00:00:00'),
	(241, 232, '', 6, 'free', '2018-08-16 12:46:11', NULL, '', '2018-01-01 00:00:00'),
	(243, 234, '', 55, 'free', '2018-08-16 12:47:22', NULL, '', '2018-01-01 00:00:00'),
	(244, 235, '', 0, 'free', '2018-08-16 12:47:49', NULL, '', '2018-01-01 00:00:00'),
	(245, 236, '', 0, 'free', '2018-08-16 12:48:53', NULL, '', '2018-01-01 00:00:00'),
	(246, 237, '', 0, 'free', '2018-08-16 12:49:37', NULL, '', '2018-01-01 00:00:00'),
	(248, 126, '', 0, 'free', '2018-08-16 15:06:21', NULL, '', '2018-01-01 00:00:00'),
	(249, 234, '', 0, 'lost', '2018-08-16 15:07:33', NULL, '', '2018-01-01 00:00:00'),
	(250, 235, '', 77, 'free', '2018-08-16 15:07:36', NULL, '', '2018-01-01 00:00:00'),
	(251, 235, '', 100, 'decomm', '2018-08-16 15:10:28', NULL, '', '2018-01-01 00:00:00'),
	(252, 239, '', 0, 'free', '2018-08-16 15:16:50', NULL, '', '2018-01-01 00:00:00'),
	(253, 217, 'Offspring-L-253', 0, 'free', '2018-08-16 15:22:59', NULL, '', '2018-01-01 00:00:00'),
	(254, 231, '', 100, 'free', '2018-08-16 15:25:46', NULL, '', '2018-01-01 00:00:00'),
	(255, 231, '', 6, 'free', '2018-08-16 15:28:58', NULL, '', '2018-01-01 00:00:00'),
	(256, 236, '', 10, 'free', '2018-08-16 16:22:58', NULL, '', '2018-08-16 14:48:48'),
	(257, 240, '', 12, 'free', '2018-08-16 17:59:53', NULL, '3086', NULL),
	(258, 129, '', 0, 'free', '2018-08-16 20:38:46', NULL, '', '2018-08-07 00:35:23'),
	(259, 129, '', 93, 'free', '2018-08-16 20:39:08', NULL, '', '2018-08-07 00:35:23'),
	(260, 181, 'Cutis-S-260', 100, 'free', '2018-08-16 20:39:59', NULL, '', '2018-08-07 00:35:33'),
	(261, 241, '', 100, 'free', '2018-08-16 20:42:30', NULL, '1399', NULL),
	(262, 242, '', 100, 'free', '2018-08-16 20:44:23', NULL, '9341', NULL),
	(263, 243, 'Мембрана-263', 100, 'free', '2018-08-16 20:45:31', NULL, '1772', NULL),
	(264, 244, 'Вакуоль-264', 100, 'free', '2018-08-16 20:46:39', NULL, '5049', NULL),
	(265, 104, '', 115, 'free', '2018-08-16 20:49:02', NULL, '', '2018-08-07 00:35:16'),
	(266, 245, 'Discovery Kingdom-266', 115, 'free', '2018-08-16 20:58:02', NULL, '1225', NULL),
	(267, 246, '', 100, 'free', '2018-08-16 20:58:07', NULL, '1877', NULL),
	(268, 175, 'Adventureland-268', 115, 'free', '2018-08-16 21:01:18', NULL, '', '2018-08-07 00:35:32'),
	(269, 247, '', 115, 'free', '2018-08-16 21:07:21', NULL, '6398', NULL),
	(270, 248, '', 102, 'free', '2018-08-16 21:33:02', NULL, '2026', NULL),
	(271, 249, '', 47, 'free', '2018-08-16 22:27:40', NULL, '8696', NULL),
	(272, 250, '', 43, 'free', '2018-08-16 22:32:31', NULL, '6604', NULL),
	(273, 251, '', 115, 'free', '2018-08-16 22:34:21', NULL, '2552', NULL),
	(274, 252, '', 115, 'free', '2018-08-16 22:36:19', NULL, '3087', NULL),
	(275, 253, '', 115, 'free', '2018-08-16 22:37:56', NULL, '1664', NULL),
	(276, 254, '', 0, 'lost', '2018-08-16 22:41:24', NULL, '2930', NULL),
	(277, 255, 'Ленинград-6-277', 115, 'free', '2018-08-16 22:51:40', NULL, '1727', NULL),
	(278, 256, '', 100, 'decomm', '2018-08-17 01:34:24', NULL, '5524', NULL),
	(279, 256, '', 100, 'decomm', '2018-08-17 01:35:50', NULL, '', '2018-08-17 03:34:23'),
	(280, 257, '', 100, 'decomm', '2018-08-17 01:39:17', NULL, '4203', NULL),
	(281, 257, '', 100, 'decomm', '2018-08-17 01:41:17', NULL, '', '2018-08-17 03:39:16'),
	(282, 258, '', 100, 'decomm', '2018-08-17 01:43:31', NULL, '5465', NULL);
/*!40000 ALTER TABLE `nodes` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
