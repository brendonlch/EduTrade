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
-- Database: `transaction`
--
CREATE DATABASE IF NOT EXISTS `transaction` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `transaction`;

-- --------------------------------------------------------

--
-- Table structure for table `trading`
--

DROP TABLE IF EXISTS `trading`;
CREATE TABLE IF NOT EXISTS `trading` (
  `transactionid` int(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `symbol` varchar(64) NOT NULL,	
  `price` decimal(10,2) NOT NULL,  
  `qty` int(64) NOT NULL,
  `transactiontype` varchar(64) NOT NULL,
  `transactiontime` datetime NOT NULL,
  PRIMARY KEY (`transactionid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `correlation`;
CREATE TABLE IF NOT EXISTS `correlation` (
  `corrid` varchar(64) NOT NULL,
  `status` varchar(64) NOT NULL,	
  PRIMARY KEY (`corrid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
--

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
