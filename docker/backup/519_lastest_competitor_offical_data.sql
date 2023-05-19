-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: (test)_lastest_competitor
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
  `date` date NOT NULL,
  `shop_name` varchar(100) NOT NULL,
  `fans_count` int NOT NULL,
  `products_count` int NOT NULL,
  `rating_counts` int NOT NULL,
  PRIMARY KEY (`date`,`shop_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offical_data`
--

LOCK TABLES `offical_data` WRITE;
/*!40000 ALTER TABLE `offical_data` DISABLE KEYS */;
INSERT INTO `offical_data` VALUES ('2023-04-19','南犬植栽',289,7,265),('2023-04-19','宅栽工作室',8833,243,5535),('2023-04-19','小李植栽',14000,240,14000),('2023-04-19','沐時園藝',29000,281,25000),('2023-04-19','珍奇植物',12000,431,13000),('2023-04-19','糀町植葉',734,135,743),('2023-04-19','開心農元',12000,497,14000),('2023-04-19','麗都花園',41000,217,28000),('2023-05-18','南犬植栽',292,7,273),('2023-05-18','宅栽工作室',8832,243,5535),('2023-05-18','小李植栽',15000,243,15000),('2023-05-18','沐時園藝',30000,271,26000),('2023-05-18','珍奇植物',12000,440,14000),('2023-05-18','糀町植葉',739,135,746),('2023-05-18','開心農元',14000,517,15000),('2023-05-18','麗都花園',41000,217,28000);
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

-- Dump completed on 2023-05-19 19:08:45
