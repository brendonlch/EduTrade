-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stock`
--
CREATE DATABASE IF NOT EXISTS `stock` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `stock`;

-- --------------------------------------------------------

--
-- Table structure for table `stock`
--

DROP TABLE IF EXISTS `stock`;
CREATE TABLE IF NOT EXISTS `stock` (
  `symbol` varchar(64) NOT NULL,
  `stockname` varchar(64) NOT NULL,	
  `apikey` varchar(64) NOT NULL, 
  `apicount` int(10) NOT NULL, 
  PRIMARY KEY (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `stockdata`;
CREATE TABLE IF NOT EXISTS `stockdata` (
  `symbol` varchar(64) NOT NULL,
  `stockname` varchar(64) NOT NULL,	
  `price` decimal(10,4) NOT NULL,  
  `volume` int(20) NOT NULL,
  `time` datetime NOT NULL,
  PRIMARY KEY (`symbol`,`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Dumping data for table `stock`
--

INSERT INTO `stock` (`symbol`, `stockname`, `apikey` ,`apicount`) VALUES
('MSFT', 'Microsoft', 'PJDSK0VOZUWF971S', 0),
('FB', 'Facebook', '7KALYIYBFKXYJXTE', 0),
('GOOG', 'Google', 'YA414KN48BBZB5NL', 0),
('TWTR', 'Twitter', 'MOS0P9ZM8WIFP5BP', 0),
('TSLA', 'Tesla', 'QRU4WHI39YLPPO7F',0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
