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
-- Database: `user`
--
CREATE DATABASE IF NOT EXISTS `user` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user`;

-- --------------------------------------------------------

--
-- Table structure for table `userinfo`
--

DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE IF NOT EXISTS `userinfo` (
  `username` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,	
  `name` varchar(64) NOT NULL,  
  `age` int(3) NOT NULL,
  `email` varchar(64) NOT NULL,
  `institution` varchar(64) NOT NULL,
  `credit` decimal(10,2) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `holdings`;
CREATE TABLE IF NOT EXISTS `holdings` (
  `username` varchar(64) NOT NULL,
  `symbol` varchar(64) NOT NULL,	
  `qty` varchar(64) NOT NULL,  
  `buyprice` decimal(10,2) NOT NULL,
  `limit` decimal(10,2),
  `datepurchased` datetime NOT NULL,
  PRIMARY KEY (`username`, `datepurchased`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `userinfo`
--

-- INSERT INTO `userinfo` (`userid`, `password`, `name`, `age`, `email`, `institution`, `credit`) VALUES
-- ('01', 'hiimnew', 'amy', 14, 'amy@gmail.com', 'SMU', '100.00'),
-- ('02', 'hiimnew', 'benny', 16, 'benny@gmail.com', 'SMU', '100.00');
-- COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
