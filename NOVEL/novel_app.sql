CREATE DATABASE  IF NOT EXISTS `novel_app` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `novel_app`;
-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: novel_app
-- ------------------------------------------------------
-- Server version	8.0.26

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
-- Table structure for table `flavors`
--

DROP TABLE IF EXISTS `flavors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flavors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_ice_cream` tinyint(1) DEFAULT '0',
  `type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flavors`
--

LOCK TABLES `flavors` WRITE;
/*!40000 ALTER TABLE `flavors` DISABLE KEYS */;
INSERT INTO `flavors` VALUES (1,'Wumpa Fruit Sorbet','A blend of whipped ataulfo mango and cold pressed Fuji apples.','2023-02-24 13:36:08','2023-02-24 13:36:08',0,NULL),(2,'Aztec Chocolate (Mexican Hot Chocolate)','Made with dark cocoa, fresh ground cinnamon, and a touch of cayenne.','2023-02-24 13:37:34','2023-02-24 13:37:34',1,NULL),(3,'Cherry Cheesecake ','A cheesecake base with ripe cherries and handmade pieces of New York style cheesecake ','2023-02-24 15:24:52','2023-02-24 15:24:52',1,NULL),(5,'Peach Habanero Sorbet','Made with ripe whipped peaches and a touch of habanero pepper.','2023-02-25 10:58:03','2023-02-25 10:58:03',0,NULL),(6,'Piña Colada Sorbet','Made with ripe whipped pineapple and coconut cream.','2023-02-25 11:18:34','2023-02-25 11:18:34',0,NULL),(7,'Peppermint Chip (Pink Peppermint Bark)','Vanilla ice cream with pink peppermint bark and chocolate chips','2023-02-25 12:19:13','2023-02-25 12:19:13',0,NULL),(8,'Pineapple Dream','Pineapple ice cream with chunks of pineapple and coconut flakes','2023-02-25 12:19:13','2023-02-25 12:19:13',0,NULL),(9,'Piña Colada Sorbet','Pineapple and coconut sorbet','2023-02-25 12:19:13','2023-02-25 12:19:13',0,NULL),(10,'Pomegranate Sorbet','Pomegranate sorbet','2023-02-25 12:19:13','2023-02-25 12:19:13',0,NULL),(11,'Peppermint Chip (Pink Peppermint Bark)','Vanilla ice cream with pink peppermint bark and chocolate chips','2023-02-25 12:21:19','2023-02-25 12:21:19',0,NULL),(12,'Pineapple Dream','Pineapple ice cream with chunks of pineapple and coconut flakes','2023-02-25 12:21:19','2023-02-25 12:21:19',0,NULL),(13,'Piña Colada Sorbet','Pineapple and coconut sorbet','2023-02-25 12:21:19','2023-02-25 12:21:19',0,NULL),(14,'Pomegranate Sorbet','Pomegranate sorbet','2023-02-25 12:21:19','2023-02-25 12:21:19',0,NULL);
/*!40000 ALTER TABLE `flavors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ice_cream_shops`
--

DROP TABLE IF EXISTS `ice_cream_shops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ice_cream_shops` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ice_cream_shops`
--

LOCK TABLES `ice_cream_shops` WRITE;
/*!40000 ALTER TABLE `ice_cream_shops` DISABLE KEYS */;
INSERT INTO `ice_cream_shops` VALUES (5,'MESA','40 N Macdonald #2, Mesa, AZ 85201','(602) 784-4729','2023-02-25 12:17:34','2023-02-25 12:17:34'),(6,'Phoenix',' 1028 Grand Ave #6, Phoenix, AZ 85007','(602) 373-2235','2023-02-25 12:18:09','2023-02-25 12:18:09');
/*!40000 ALTER TABLE `ice_cream_shops` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shop_flavors`
--

DROP TABLE IF EXISTS `shop_flavors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shop_flavors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `flavor_id` int NOT NULL,
  `shop_id` int NOT NULL,
  `is_current` tinyint(1) NOT NULL DEFAULT '0',
  `is_ice_cream` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `flavor_id` (`flavor_id`),
  KEY `shop_id` (`shop_id`),
  CONSTRAINT `shop_flavors_ibfk_1` FOREIGN KEY (`flavor_id`) REFERENCES `flavors` (`id`),
  CONSTRAINT `shop_flavors_ibfk_2` FOREIGN KEY (`shop_id`) REFERENCES `ice_cream_shops` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_flavors`
--

LOCK TABLES `shop_flavors` WRITE;
/*!40000 ALTER TABLE `shop_flavors` DISABLE KEYS */;
/*!40000 ALTER TABLE `shop_flavors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Frank','Acosta','franjuarez19971219@gmail.com','$2b$12$rOLtbi68OWC/0mRwpnOw7.1HEIvOad3AbMAxUTdTOlt6EJLlOEncW','2023-02-24 12:07:47','2023-02-24 12:07:47');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-26  4:29:23
