CREATE DATABASE  IF NOT EXISTS `competitor_data` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `competitor_data`;
-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: competitor_data
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `offical_data`
--

DROP TABLE IF EXISTS `offical_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offical_data` (
  `date_time` datetime NOT NULL,
  `shop_id` int NOT NULL,
  `shop_name` varchar(100) NOT NULL,
  `fans_count` int NOT NULL,
  `products_count` int NOT NULL,
  `followers` int NOT NULL,
  `rating` float NOT NULL,
  `rating_counts` int NOT NULL,
  `response_rate` float NOT NULL,
  PRIMARY KEY (`date_time`,`shop_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offical_data`
--

LOCK TABLES `offical_data` WRITE;
/*!40000 ALTER TABLE `offical_data` DISABLE KEYS */;
INSERT INTO `offical_data` VALUES ('2023-04-19 00:00:00',3045968,'開心農元',12000,497,62,5,14000,0.98),('2023-04-19 00:00:00',4877504,'麗都',41000,217,11,5,28000,0.89),('2023-04-19 00:00:00',7432754,'小李植栽',14000,240,105,5,14000,0.94),('2023-04-19 00:00:00',15227497,'珍奇植物',12000,431,96,5,13000,0.99),('2023-04-19 00:00:00',161364427,'沐時園藝',29000,281,1,5,25000,0.94),('2023-04-19 00:00:00',268986085,'南犬',289,7,25,5,265,0.86),('2023-04-19 00:00:00',369371665,'糀町',734,135,29,4.9,743,0.83);
/*!40000 ALTER TABLE `offical_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-08  0:09:32
