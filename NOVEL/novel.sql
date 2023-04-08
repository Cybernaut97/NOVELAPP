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
-- Table structure for table `customer_phone_numbers`
--

DROP TABLE IF EXISTS `customer_phone_numbers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_phone_numbers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ice_cream_shop_id` int NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `flavor_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ice_cream_shop_id` (`ice_cream_shop_id`),
  KEY `flavor_id` (`flavor_id`),
  CONSTRAINT `customer_phone_numbers_ibfk_1` FOREIGN KEY (`ice_cream_shop_id`) REFERENCES `ice_cream_shops` (`id`),
  CONSTRAINT `customer_phone_numbers_ibfk_2` FOREIGN KEY (`flavor_id`) REFERENCES `flavors` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_phone_numbers`
--

LOCK TABLES `customer_phone_numbers` WRITE;
/*!40000 ALTER TABLE `customer_phone_numbers` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_phone_numbers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flavors`
--

DROP TABLE IF EXISTS `flavors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flavors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_ice_cream` tinyint(1) DEFAULT '0',
  `type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flavors`
--

LOCK TABLES `flavors` WRITE;
/*!40000 ALTER TABLE `flavors` DISABLE KEYS */;
INSERT INTO `flavors` VALUES (55,'Acai Sorbet (Brazilian Acai Sorbet)','Made with Brazilian palmberry Acai.','2023-02-28 03:45:28','2023-03-02 09:26:32',0,NULL),(56,'Aztec Chocolate (Mexican Hot Chocolate)','Made with dark cocoa, fresh ground cinnamon, and a touch of cayenne.','2023-02-28 03:46:18','2023-03-05 11:52:26',1,NULL),(57,'Almond Joy','A coconut cream base with dark chocolate, fire roasted almonds, and sweetened coconut flakes.','2023-02-28 03:46:33','2023-02-28 03:46:33',1,NULL),(58,'Andes Mountain','A white mint base with a milk chocolate swirl, mint cookie pieces, and Andes Mints.','2023-02-28 03:46:43','2023-02-28 03:46:43',1,NULL),(59,'Arizona Skies','Our mystery flavor made with a unique blend of local ingredients in a sky blue base with marshmallow cloud cream.','2023-02-28 03:47:10','2023-02-28 03:47:10',1,NULL),(60,'Arnold Palmer Sorbet','Made with fresh squeezed lemonade and Sun brewed sweet tea.','2023-02-28 03:47:48','2023-02-28 03:47:48',0,NULL),(61,'Banana Sorbet','Made with ripe whipped banana.','2023-02-28 03:47:58','2023-02-28 03:47:58',0,NULL),(62,'Bananas Foster ','A buttered banana cream base, made with ripe bananas caramelized in dark rum, cinnamon, and brown sugar.','2023-02-28 03:48:06','2023-02-28 03:48:06',1,NULL),(63,'Banana Bread Pudding','Banana custard base with chopped walnuts layered with brioche bread soaked in butter, cinnamon, and nutmeg ','2023-02-28 03:48:29','2023-02-28 03:48:29',1,NULL),(64,'Banana Cream Pie','An old fashioned banana cream pie recipe made with ripe whipped banana, pure vanilla, and Nilla Wafers','2023-02-28 03:48:38','2023-02-28 03:48:38',1,NULL),(65,'Banana Infused Nutella','A whipped Nutella base infused with a sweetened reduction of ripe bananas.','2023-02-28 03:48:54','2023-02-28 03:48:54',1,NULL),(66,'Banana Nutella Crepe','A classic crepe  recipe made with real butter and pure vanilla with a light swirl of Nutella and chocolate dipped banana pieces.','2023-02-28 03:49:19','2023-02-28 03:49:19',1,NULL),(67,'BeeNut Butter Biscuit','Made with honey whipped peanut butter, rolled oats, toasted coconut, and golden syrup. Optional drizzle with New Zealand Manuka Honey blend. ','2023-02-28 03:49:29','2023-02-28 03:49:29',1,NULL),(68,'Birthday Cake','A white cake batter base with blue buttercream frosting and handmade birthday cake pieces.','2023-02-28 03:49:37','2023-02-28 03:49:37',1,NULL),(69,'Biscoff (Biscoff Cookie)','A cookie butter base made with European Lotus Biscoff Cookies.','2023-02-28 03:49:49','2023-02-28 03:49:49',1,NULL),(70,'Black Cherry (Oregon Black Cherry)','A black cherry base infused with pure cherry juice and pieces of Pacific Northwest black cherries.','2023-02-28 03:49:58','2023-02-28 03:49:58',1,NULL),(71,'Black Cherry Sorbet (Oregon Black Cherry Sorbet)','Made with pure cherry juice and whipped Oregon Black cherries.','2023-02-28 03:50:08','2023-02-28 03:50:08',0,NULL),(72,'Blackberry Merlot Sorbet','Made with Pacific Northwest blackberries and Napa Merlot.','2023-02-28 03:50:50','2023-02-28 03:50:50',0,NULL),(73,'Blue Moon (Revenge of the Nerds)','Midwest Blue Moon ice cream (tastes kind of like Froot Loops) topped with optional Nerds candy.','2023-02-28 03:51:10','2023-02-28 03:51:10',1,NULL),(74,'Blueberry Basil Sorbet (Wild Blueberry Basil Sorbet)','Made with Pacific Northwest blueberries and Mediterranean basil.','2023-02-28 03:51:26','2023-02-28 03:51:26',0,NULL),(75,'Blueberry Pie (Wild Blueberry Pie)','Made with sweetened heavy cream, Pacific Northwest wild blueberries, and a whole handmade blueberry pie in every batch.','2023-02-28 03:51:40','2023-02-28 03:51:40',1,NULL),(76,'Blueberry Thyme (Wild Blueberry Thyme)','Made with Pacific Northwest blueberries, sweetened heavy cream, and chopped thyme.','2023-02-28 03:51:50','2023-03-21 11:45:52',0,NULL),(77,'Bonfire Brûlée','A toasted marshmallow base with a hard milk chocolate swirl, toasted graham, and bourbon brûlée sauce.','2023-02-28 03:52:08','2023-02-28 18:41:08',1,NULL),(78,'Boysenberry Buttercake','Buttered sweet cream with a reduction of California boysenberries and handmade buttercake crumble.','2023-02-28 03:52:16','2023-02-28 03:52:16',1,NULL),(80,'Peanut Butter and Jelly (PB&J Sandwich)','A white bread base, made with all the same ingredients as a classic white bread, creamy peanut butter, grape jelly, and crustless pieces of PB&J sandwich.','2023-03-02 10:23:59','2023-03-21 11:50:44',1,NULL),(85,'Ecto Cooler Sorbet ','A tangerine citrus sorbet made to look and taste exactly like Hi-C Ecto Cooler.','2023-03-21 11:52:42','2023-03-21 11:52:42',0,NULL),(86,'Forest Berry Sorbet','Made with Pacific Northwest raspberries, blackberries, strawberries, and blueberries. Made with Pacific Northwest raspberries, blackberries, strawberries, and blueberries.','2023-03-21 11:53:55','2023-03-21 11:53:55',0,NULL),(87,'Wumpa Fruit Sorbet','A blend of whipped ataulfo mango and cold pressed Fuji apples.','2023-03-21 12:13:19','2023-03-21 12:13:19',0,NULL),(89,'Straight up Strawberry','PNW strawberries','2023-03-22 22:35:22','2023-03-22 22:35:22',1,NULL),(90,'Wumpa Fruit Sorbet','wsedqadqwdwqd','2023-03-22 22:37:40','2023-03-22 22:37:40',1,NULL),(91,'asdasdasd','asdasdasdasdasd','2023-03-22 22:43:48','2023-03-22 22:43:48',0,NULL);
/*!40000 ALTER TABLE `flavors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `freezer_inventories`
--

DROP TABLE IF EXISTS `freezer_inventories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `freezer_inventories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `shop_id` int NOT NULL,
  `flavor_id` int NOT NULL,
  `quantity` int DEFAULT '0',
  `is_current` tinyint DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `current_flavor` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `shop_id` (`shop_id`),
  KEY `flavor_id` (`flavor_id`),
  CONSTRAINT `freezer_inventories_ibfk_1` FOREIGN KEY (`shop_id`) REFERENCES `ice_cream_shops` (`id`),
  CONSTRAINT `freezer_inventories_ibfk_2` FOREIGN KEY (`flavor_id`) REFERENCES `flavors` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `freezer_inventories`
--

LOCK TABLES `freezer_inventories` WRITE;
/*!40000 ALTER TABLE `freezer_inventories` DISABLE KEYS */;
INSERT INTO `freezer_inventories` VALUES (9,2,70,3,0,'2023-03-21 05:16:40','2023-03-24 03:54:34',1),(30,4,64,1,0,'2023-03-22 16:06:49','2023-03-23 04:32:26',1),(32,4,80,2,0,'2023-03-22 16:07:41','2023-03-23 04:32:05',0),(35,2,68,3,0,'2023-03-22 17:02:42','2023-03-24 03:54:34',1),(44,4,86,3,0,'2023-03-23 04:37:47','2023-03-23 04:38:24',1),(60,2,66,5,0,'2023-03-23 06:03:30','2023-03-24 03:54:51',1),(68,3,76,3,0,'2023-03-23 06:38:27','2023-03-23 17:01:05',1),(69,3,85,3,0,'2023-03-23 06:38:32','2023-03-23 07:01:55',1),(70,3,87,5,0,'2023-03-23 06:39:11','2023-03-23 06:57:11',1),(72,3,66,2,0,'2023-03-23 06:57:20','2023-03-23 07:01:56',1),(75,3,89,5,0,'2023-03-23 16:58:11','2023-03-23 16:58:11',0),(76,7,56,3,0,'2023-03-23 17:14:10','2023-03-23 17:14:10',0),(77,7,58,6,0,'2023-03-23 17:14:14','2023-03-23 17:14:14',0),(78,7,60,5,0,'2023-03-23 17:14:18','2023-03-23 17:14:18',0),(79,7,55,1,0,'2023-03-23 17:14:20','2023-03-23 17:14:20',0),(80,7,76,6,0,'2023-03-23 17:14:25','2023-03-23 17:14:25',0),(81,8,55,3,0,'2023-03-23 17:14:45','2023-03-23 17:14:45',0),(82,8,76,9,0,'2023-03-23 17:14:51','2023-03-23 17:14:59',0),(83,8,56,3,0,'2023-03-23 17:15:04','2023-03-23 17:15:04',0),(84,8,57,2,0,'2023-03-23 17:15:06','2023-03-23 17:15:06',0),(85,8,62,1,0,'2023-03-23 17:15:08','2023-03-23 17:15:08',0),(86,2,86,3,0,'2023-03-24 03:47:10','2023-03-24 03:54:52',1),(87,2,87,4,0,'2023-03-24 03:47:29','2023-03-24 03:54:53',1),(88,2,71,3,0,'2023-03-24 03:56:37','2023-03-24 03:56:39',1),(89,2,74,4,0,'2023-03-24 03:56:44','2023-03-24 03:56:46',1);
/*!40000 ALTER TABLE `freezer_inventories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `headquarters`
--

DROP TABLE IF EXISTS `headquarters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `headquarters` (
  `id` int NOT NULL AUTO_INCREMENT,
  `flavor_id` int NOT NULL,
  `quantity` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `headquarters`
--

LOCK TABLES `headquarters` WRITE;
/*!40000 ALTER TABLE `headquarters` DISABLE KEYS */;
/*!40000 ALTER TABLE `headquarters` ENABLE KEYS */;
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
  `address` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `location` varchar(255) DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ice_cream_shops`
--

LOCK TABLES `ice_cream_shops` WRITE;
/*!40000 ALTER TABLE `ice_cream_shops` DISABLE KEYS */;
INSERT INTO `ice_cream_shops` VALUES (2,'Mesa','40 N Macdonald #2, Mesa, AZ 85201','(602) 784-4729','2023-03-21 12:05:39','2023-03-21 12:05:39',NULL,2),(3,'Sedona','Some where in Sedona','(623) 920-2110','2023-03-21 12:09:29','2023-03-21 12:09:29',NULL,3),(4,'Phoenix','1028 Grand Ave #6, Phoenix, AZ 85007','(602) 373-2235','2023-03-21 12:28:01','2023-03-21 12:28:01',NULL,4),(7,'Moreno Valley','California','(951) 840-5985','2023-03-24 00:13:00','2023-03-24 00:13:00',NULL,5),(8,'New York','New york','(752) 445-4564','2023-03-24 00:13:57','2023-03-24 00:13:57',NULL,5);
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
  KEY `shop_id` (`shop_id`),
  KEY `fk_shop_flavors_flavor_id` (`flavor_id`),
  CONSTRAINT `fk_shop_flavors_flavor_id` FOREIGN KEY (`flavor_id`) REFERENCES `flavors` (`id`),
  CONSTRAINT `shop_flavors_ibfk_1` FOREIGN KEY (`flavor_id`) REFERENCES `flavors` (`id`),
  CONSTRAINT `shop_flavors_ibfk_2` FOREIGN KEY (`shop_id`) REFERENCES `ice_cream_shops` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `shop_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'kuzco','kuzco','kuzco@gmail.com','$2b$12$yTyAe9CpWjviNSVgec5qTuuWAnxnjuNYGYSfnwmB0N7/calDRQgNe','2023-03-21 11:59:58','2023-03-21 11:59:58',NULL),(2,'asdasdasd','asdasdasd','asdasdasd@gmail.com','$2b$12$XW3A8oJyXf/4hbs0ZuvS2uMTBVn3P1eQJ5.5vBDDZZ.PjryEYfijy','2023-03-21 12:04:54','2023-03-21 12:04:54',NULL),(3,'maasds','asdasdsd','ManyFaces@gmail.com','$2b$12$kPczToUHnNEBT//swbFfQe0b6liizcvIlG4Yqbymu4A8VPL484QTS','2023-03-21 12:08:28','2023-03-21 12:08:28',NULL),(4,'phxaz','asdasd','phx@gmail.com','$2b$12$mL5GQo/yjpIHmtrQZgeYSOuBjMKyUAf.RrBqRqIFLbnpAKtO638eK','2023-03-21 12:27:28','2023-03-21 12:27:28',NULL),(5,'Francisco','Acosta','franjuarez19971219@gmail.com','$2b$12$E.GDxdgx.8HPqbBOuRzj9ulOlzxZcD81.xcR6RM8rXuGNovfflrxK','2023-03-21 12:38:26','2023-03-21 12:38:26',NULL);
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

-- Dump completed on 2023-03-24 16:07:20
