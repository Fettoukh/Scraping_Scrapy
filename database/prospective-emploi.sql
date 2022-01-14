-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 07, 2021 at 03:41 PM
-- Server version: 8.0.18
-- PHP Version: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `prospective-emploi`
--

-- --------------------------------------------------------

--
-- Table structure for table `pre_normalized_offre_emploi`
--

DROP TABLE IF EXISTS `pre_normalized_offre_emploi`;
CREATE TABLE IF NOT EXISTS `pre_normalized_offre_emploi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_poste` int(11) NOT NULL DEFAULT '1',
  `entreprise` text,
  `secteur` varchar(255) DEFAULT NULL,
  `metier` varchar(255) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `region` varchar(50) DEFAULT NULL,
  `formation` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `niv_experience` varchar(255) DEFAULT NULL,
  `type_de_contrat` varchar(255) DEFAULT NULL,
  `description` text,
  `source` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
