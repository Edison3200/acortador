-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.5.9-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Volcando estructura para tabla acortador.url
CREATE TABLE IF NOT EXISTS `url` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `url_original` varchar(250) NOT NULL DEFAULT '',
  `url_corta` varchar(50) NOT NULL DEFAULT '',
  `id_usu` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url_corta` (`url_corta`),
  KEY `FK_url_usuarios` (`id_usu`),
  CONSTRAINT `FK_url_usuarios` FOREIGN KEY (`id_usu`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla acortador.url: ~2 rows (aproximadamente)
DELETE FROM `url`;
/*!40000 ALTER TABLE `url` DISABLE KEYS */;
INSERT INTO `url` (`id`, `url_original`, `url_corta`, `id_usu`) VALUES
	(46, 'https://www.youtube.com/watch?v=bmoT9-PjDhg&list=RD1vkvTAJf_JA&index=10&ab_channel=PauloLondra', 'http://127.0.0.1:5000/i7wi', 33),
	(52, 'https://www.youtube.com/watch?v=wsVFmCoykZ4&ab_channel=ImagineDragonsVEVO', 'http://127.0.0.1:5000/kird', NULL),
	(53, 'https://cine24h.net/episode/dragon-ball-super-1x89/', 'http://127.0.0.1:5000/mz66', 33);
/*!40000 ALTER TABLE `url` ENABLE KEYS */;

-- Volcando estructura para tabla acortador.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombres` char(50) NOT NULL DEFAULT '',
  `email` varchar(100) NOT NULL DEFAULT '0',
  `password` varchar(100) NOT NULL DEFAULT '0',
  `verificado` int(1) NOT NULL DEFAULT 0,
  `fecha_ver` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla acortador.usuarios: ~1 rows (aproximadamente)
DELETE FROM `usuarios`;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` (`id`, `nombres`, `email`, `password`, `verificado`, `fecha_ver`) VALUES
	(33, 'Manuel54', 'jenadob576@zcai77.com', 'admin123', 1, '2021-04-17 08:16:17'),
	(35, 'Canelo23', 'canelo@gmail.com', 'admin123', 1, '2021-04-20 08:20:27');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
