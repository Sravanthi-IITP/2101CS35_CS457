-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 23, 2025 at 05:50 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `role_based_access`
--

-- --------------------------------------------------------

--
-- Table structure for table `stud_info`
--

CREATE TABLE `stud_info` (
  `roll` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `branch` varchar(50) DEFAULT NULL,
  `hometown` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stud_info`
--

INSERT INTO `stud_info` (`roll`, `name`, `age`, `branch`, `hometown`) VALUES
(101, 'Alice', 19, 'Computer Science', 'New York'),
(102, 'Bob Smith', 21, 'Electrical Engineering', 'Los Angeles'),
(103, 'Charlie Brown', 22, 'Mechanical Engineering', 'Chicago');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','editor','viewer') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `role`) VALUES
(1, 'sravs_929', 'scrypt:32768:8:1$VcUoVrrMU2OVzYYp$c8b74faec06e335d29fc6fb74eb791464c30b81371d2435a6beaf441c3ed51edf1136ab55f3b384d19bd5da47297aa307b0afc6d8d4364c3092e2da0d40f5a3b', 'viewer'),
(3, 'admin_user', 'scrypt:32768:8:1$4nW9cWsd97OFGiuE$a5b515ff9c79dd9422ec38b6d55c5f487fa12da8b89307e63c84c2100ac669d2ea6542c594d033afd66633450e1d1a5b13b2122d5b81f5bc961da5bdaa1da6a1', 'admin'),
(4, 'editor_user', 'scrypt:32768:8:1$xHEndk0iJbpnZvUx$b50cccc476177164fff0b5bde00024f62fe4981d2f5507e6fefc0894857a929ffdce8bd995570080baaf81299525d015820fdae87e591dabe89ebc27d96ec32e', 'editor'),
(5, 'viewer_user', '$2b$12$nCQsPyrJ0Nh8a6hxU/4EGOisFFXKmUY/a7TQd1WOMvMiRf0VeH3zq', 'viewer');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `stud_info`
--
ALTER TABLE `stud_info`
  ADD PRIMARY KEY (`roll`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
