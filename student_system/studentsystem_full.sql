-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: studentsystem
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `course_code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `course_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `credits` int NOT NULL,
  `department` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  UNIQUE KEY `ix_courses_course_code` (`course_code`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'COE307','Database Management Systems','Relational DB design, SQL, normalization.',4,'Computer Engineering'),(2,'SWE314','Web Programming','Frontend/backend web development basics.',4,'Software Engineering'),(3,'SWE307','Software Analysis and Design','Requirements, UML, design principles.',4,'Software Engineering'),(4,'MAT201','Calculus II','Integration techniques and applications.',4,'Mathematics'),(5,'PHY101','General Physics I','Mechanics, motion, and forces.',4,'Physics'),(6,'BUS101','Introduction to Management','Core management principles.',3,'Business'),(7,'ECO201','Microeconomics','Supply, demand, market structures.',3,'Economics'),(8,'COE205','Data Structures','Arrays, lists, trees, graphs.',4,'Computer Engineering'),(9,'SWE309','Programming Languages','Concepts, paradigms, semantics.',4,'Software Engineering'),(10,'MAT301','Probability','Probability theory and applications.',3,'Mathematics'),(11,'CS101','Introduction to Computer Science','An introductory course covering basic programming concepts',3,'Computer Science');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrollments`
--

DROP TABLE IF EXISTS `enrollments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enrollments` (
  `enrollment_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `section_id` int NOT NULL,
  `enrollment_date` date DEFAULT (curdate()),
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'Active',
  PRIMARY KEY (`enrollment_id`),
  UNIQUE KEY `unique_student_section` (`student_id`,`section_id`),
  KEY `section_id` (`section_id`),
  CONSTRAINT `enrollments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE,
  CONSTRAINT `enrollments_ibfk_2` FOREIGN KEY (`section_id`) REFERENCES `sections` (`section_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrollments`
--

LOCK TABLES `enrollments` WRITE;
/*!40000 ALTER TABLE `enrollments` DISABLE KEYS */;
INSERT INTO `enrollments` VALUES (1,1,1,'2025-09-20','Active'),(2,2,2,'2025-09-20','Active'),(3,3,3,'2025-09-20','Active'),(4,4,4,'2025-09-20','Active'),(5,5,5,'2025-09-20','Active'),(6,6,6,'2025-09-20','Active'),(7,7,7,'2025-09-20','Active'),(8,8,8,'2025-09-20','Active'),(9,9,9,'2025-09-20','Active'),(10,10,10,'2025-09-20','Active'),(12,1,2,'2026-01-05','Active'),(13,13,11,'2026-01-05','Active');
/*!40000 ALTER TABLE `enrollments` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_section_capacity_before_enrollment` BEFORE INSERT ON `enrollments` FOR EACH ROW BEGIN
    DECLARE v_capacity INT;
    DECLARE v_current  INT;

    -- section capacity al
    SELECT capacity INTO v_capacity
      FROM sections
     WHERE section_id = NEW.section_id;

    -- capacity null ise sınırsız kabul et
    IF v_capacity IS NULL THEN
        SET v_capacity = 999999;
    END IF;

    -- mevcut enrollment sayısı
    SELECT COUNT(*) INTO v_current
      FROM enrollments
     WHERE section_id = NEW.section_id
       AND status IN ('ENROLLED', 'ACTIVE', 'APPROVED');

    IF v_current >= v_capacity THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Section capacity exceeded: enrollment blocked';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `grades`
--

DROP TABLE IF EXISTS `grades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grades` (
  `grade_id` int NOT NULL AUTO_INCREMENT,
  `enrollment_id` int NOT NULL,
  `assessment_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `score` decimal(5,2) NOT NULL,
  `max_score` decimal(5,2) DEFAULT '100.00',
  `weight` decimal(5,2) DEFAULT NULL,
  `graded_date` date DEFAULT (curdate()),
  `notes` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`grade_id`),
  KEY `enrollment_id` (`enrollment_id`),
  CONSTRAINT `grades_ibfk_1` FOREIGN KEY (`enrollment_id`) REFERENCES `enrollments` (`enrollment_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades`
--

LOCK TABLES `grades` WRITE;
/*!40000 ALTER TABLE `grades` DISABLE KEYS */;
INSERT INTO `grades` VALUES (1,1,'Midterm',78.50,100.00,0.40,'2025-10-20','Good performance'),(2,2,'Midterm',85.00,100.00,0.40,'2025-10-20','Strong understanding'),(3,3,'Midterm',92.00,100.00,0.40,'2025-10-20','Excellent'),(4,4,'Midterm',66.50,100.00,0.40,'2025-10-20','Needs improvement'),(5,5,'Midterm',74.00,100.00,0.40,'2025-10-20','Average'),(6,6,'Midterm',88.00,100.00,0.40,'2025-10-20','Very good'),(7,7,'Midterm',59.00,100.00,0.40,'2025-10-20','Below expected'),(8,8,'Midterm',81.00,100.00,0.40,'2025-10-20','Good'),(9,9,'Midterm',90.00,100.00,0.40,'2025-10-20','Great'),(10,10,'Midterm',70.00,100.00,0.40,'2025-10-20','Satisfactory'),(11,13,'Midterm',85.00,100.00,0.40,'2026-01-05',NULL),(12,13,'Final',90.00,100.00,0.60,'2026-01-05',NULL);
/*!40000 ALTER TABLE `grades` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_grade_validation_before_insert` BEFORE INSERT ON `grades` FOR EACH ROW BEGIN
    -- max_score pozitif olmalı
    IF NEW.max_score IS NULL OR NEW.max_score <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid max_score: must be > 0';
    END IF;

    -- score 0..max_score aralığında olmalı
    IF NEW.score IS NULL OR NEW.score < 0 OR NEW.score > NEW.max_score THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid score: must be between 0 and max_score';
    END IF;

    -- weight 0..1 aralığında olmalı
    IF NEW.weight IS NULL OR NEW.weight < 0 OR NEW.weight > 1 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid weight: must be between 0 and 1';
    END IF;

    -- assessment_type boş olmasın
    IF NEW.assessment_type IS NULL OR TRIM(NEW.assessment_type) = '' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid assessment_type: cannot be empty';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Check_Grade_Range` BEFORE INSERT ON `grades` FOR EACH ROW BEGIN
    IF NEW.score < 0 OR NEW.score > 100 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Score must be between 0 and 100.';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `instructors`
--

DROP TABLE IF EXISTS `instructors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instructors` (
  `instructor_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `first_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `department` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hire_date` date DEFAULT NULL,
  PRIMARY KEY (`instructor_id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `instructors_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instructors`
--

LOCK TABLES `instructors` WRITE;
/*!40000 ALTER TABLE `instructors` DISABLE KEYS */;
INSERT INTO `instructors` VALUES (1,11,'John','Smith','john.smith@uni.edu','0212-111-0001','Computer Engineering','2018-09-01'),(2,12,'Sarah','Brown','sarah.brown@uni.edu','0212-111-0002','Software Engineering','2019-02-15'),(3,13,'David','Wilson','david.wilson@uni.edu','0212-111-0003','Mathematics','2017-10-10'),(4,14,'Emily','Taylor','emily.taylor@uni.edu','0212-111-0004','Physics','2020-01-20'),(5,15,'Michael','Anderson','michael.anderson@uni.edu','0212-111-0005','Business','2016-06-05'),(6,16,'Olivia','Thomas','olivia.thomas@uni.edu','0212-111-0006','Economics','2021-03-12'),(7,17,'Daniel','Martin','daniel.martin@uni.edu','0212-111-0007','Computer Engineering','2015-11-25'),(8,18,'Sophia','Moore','sophia.moore@uni.edu','0212-111-0008','Software Engineering','2018-04-30'),(9,19,'James','Jackson','james.jackson@uni.edu','0212-111-0009','Mathematics','2014-09-09'),(10,20,'Mia','White','mia.white@uni.edu','0212-111-0010','Physics','2022-09-01'),(11,29,'Edip','Instructor','edip@instructor.local',NULL,NULL,NULL);
/*!40000 ALTER TABLE `instructors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sections`
--

DROP TABLE IF EXISTS `sections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sections` (
  `section_id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `instructor_id` int DEFAULT NULL,
  `semester_id` int NOT NULL,
  `section_number` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `capacity` int DEFAULT NULL,
  `schedule` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `room` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`section_id`),
  KEY `course_id` (`course_id`),
  KEY `instructor_id` (`instructor_id`),
  KEY `semester_id` (`semester_id`),
  CONSTRAINT `sections_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE,
  CONSTRAINT `sections_ibfk_2` FOREIGN KEY (`instructor_id`) REFERENCES `instructors` (`instructor_id`) ON DELETE SET NULL,
  CONSTRAINT `sections_ibfk_3` FOREIGN KEY (`semester_id`) REFERENCES `semesters` (`semester_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sections`
--

LOCK TABLES `sections` WRITE;
/*!40000 ALTER TABLE `sections` DISABLE KEYS */;
INSERT INTO `sections` VALUES (1,1,1,4,'A',30,'Mon 10:00-12:00','B201'),(2,2,2,4,'A',35,'Tue 14:00-16:00','C105'),(3,3,8,4,'A',25,'Wed 09:00-11:00','D303'),(4,4,3,4,'A',40,'Thu 13:00-15:00','M101'),(5,5,4,4,'A',40,'Fri 10:00-12:00','P202'),(6,6,5,4,'A',50,'Mon 13:00-15:00','E210'),(7,7,6,4,'A',45,'Tue 09:00-11:00','E211'),(8,8,7,4,'A',30,'Wed 14:00-16:00','B204'),(9,9,2,4,'B',35,'Thu 10:00-12:00','C106'),(10,10,9,4,'A',40,'Fri 14:00-16:00','M102'),(11,11,11,1,'A',NULL,'Mon 10:00-12:00','B-201');
/*!40000 ALTER TABLE `sections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semesters`
--

DROP TABLE IF EXISTS `semesters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `semesters` (
  `semester_id` int NOT NULL AUTO_INCREMENT,
  `semester_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `year` int NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`semester_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semesters`
--

LOCK TABLES `semesters` WRITE;
/*!40000 ALTER TABLE `semesters` DISABLE KEYS */;
INSERT INTO `semesters` VALUES (1,'Fall',2024,'2024-09-16','2024-12-27',1),(2,'Spring',2025,'2025-02-10','2025-06-06',0),(3,'Summer',2025,'2025-07-01','2025-08-15',0),(4,'Fall',2025,'2025-09-15','2025-12-26',1),(5,'Spring',2026,'2026-02-09','2026-06-05',0),(6,'Summer',2026,'2026-07-01','2026-08-14',0),(7,'Fall',2026,'2026-09-14','2026-12-25',0),(8,'Spring',2027,'2027-02-08','2027-06-04',0),(9,'Summer',2027,'2027-07-01','2027-08-13',0),(10,'Fall',2027,'2027-09-13','2027-12-24',0);
/*!40000 ALTER TABLE `semesters` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Protect_Active_Semester` BEFORE DELETE ON `semesters` FOR EACH ROW BEGIN
    IF OLD.is_active = 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Cannot delete the currently active semester.';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `first_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `enrollment_date` date DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,1,'Ayse','Yilmaz','ayse.yilmaz@uni.edu','0500-000-0001','2003-02-11','2024-09-16'),(2,2,'Ahmet','Demir','ahmet.demir@uni.edu','0500-000-0002','2002-07-21','2024-09-16'),(3,3,'Elif','Kaya','elif.kaya@uni.edu','0500-000-0003','2003-11-03','2024-09-16'),(4,4,'Mehmet','Celik','mehmet.celik@uni.edu','0500-000-0004','2001-05-14','2024-09-16'),(5,5,'Zeynep','Aydin','zeynep.aydin@uni.edu','0500-000-0005','2002-01-28','2024-09-16'),(6,6,'Mert','Arslan','mert.arslan@uni.edu','0500-000-0006','2003-09-09','2024-09-16'),(7,7,'Seda','Koc','seda.koc@uni.edu','0500-000-0007','2002-03-31','2024-09-16'),(8,8,'Can','Sahin','can.sahin@uni.edu','0500-000-0008','2001-12-22','2024-09-16'),(9,9,'Ece','Oz','ece.oz@uni.edu','0500-000-0009','2003-06-06','2024-09-16'),(10,10,'Kerem','Yildiz','kerem.yildiz@uni.edu','0500-000-0010','2002-10-17','2024-09-16'),(11,23,'Student','User','student@student.local',NULL,NULL,NULL),(12,24,'Transaction','Demo','trans.demo@uni.edu',NULL,NULL,'2026-01-05'),(13,30,'Edip','Student','edip@student.local',NULL,NULL,NULL);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT (now()),
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `ix_users_username` (`username`),
  KEY `ix_users_role` (`role`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'student01','hash_student01','Student','2026-01-05 11:42:02'),(2,'student02','hash_student02','Student','2026-01-05 11:42:02'),(3,'student03','hash_student03','Student','2026-01-05 11:42:02'),(4,'student04','hash_student04','Student','2026-01-05 11:42:02'),(5,'student05','hash_student05','Student','2026-01-05 11:42:02'),(6,'student06','hash_student06','Student','2026-01-05 11:42:02'),(7,'student07','hash_student07','Student','2026-01-05 11:42:02'),(8,'student08','hash_student08','Student','2026-01-05 11:42:02'),(9,'student09','hash_student09','Student','2026-01-05 11:42:02'),(10,'student10','hash_student10','Student','2026-01-05 11:42:02'),(11,'instr01','hash_instr01','Instructor','2026-01-05 11:42:02'),(12,'instr02','hash_instr02','Instructor','2026-01-05 11:42:02'),(13,'instr03','hash_instr03','Instructor','2026-01-05 11:42:02'),(14,'instr04','hash_instr04','Instructor','2026-01-05 11:42:02'),(15,'instr05','hash_instr05','Instructor','2026-01-05 11:42:02'),(16,'instr06','hash_instr06','Instructor','2026-01-05 11:42:02'),(17,'instr07','hash_instr07','Instructor','2026-01-05 11:42:02'),(18,'instr08','hash_instr08','Instructor','2026-01-05 11:42:02'),(19,'instr09','hash_instr09','Instructor','2026-01-05 11:42:02'),(20,'instr10','hash_instr10','Instructor','2026-01-05 11:42:02'),(21,'admin01','hash_admin01','Admin','2026-01-05 11:42:02'),(22,'admin','scrypt:32768:8:1$pbK3JiSdAcpoiDxl$8f95959e6ec5f23b2997e9ca7839f578f27ad14e10815c243ef99a8b3bc57d485a9e726c25ec119ef22d86c38faf0596e1612781918cc72f9c388374ff40210e','Student','2026-01-05 12:22:17'),(23,'student','scrypt:32768:8:1$fOAViwEORxFECm6d$0717c71550e48b88aaa0a517e67db3e8202cd1cf156a6141d704d9180ac26011c39422873ceb2f1288b5476524d1fff46cdc14f580a14b8554429883579c9ff8','Student','2026-01-05 12:22:45'),(24,'trans_user','hash123','Student','2026-01-05 16:30:37'),(25,'admin_student','scrypt:32768:8:1$Wc2Z4d5AOxHh4TG8$8603736143baf1732836fd809b1e546da09fe98775c6ca3563e2ae252d26373216f2c92b96288ec8c8bfd5c7aad7dcceeb08504179e568463cbdb5aafa139480','Student','2026-01-05 17:37:02'),(26,'admin_admin','scrypt:32768:8:1$9csOFuXi89874SNu$9a94c3518d4d0e5b7e36aedb6f3e0412b92520b8038baaf5472081a294fd689e4c147a4afd33e551eacf4e9c822f7bdf695270edde6f46054091e757ddbecdef','Admin','2026-01-05 17:37:14'),(27,'admin_instructor','scrypt:32768:8:1$H4zxksLaPoaDfuNB$d998f1c58d6bf58f61557a470f51b473263dc5f28ec9762caf0b25bcd55e2d52fc5ed582b266bf6da5017a2ffe05a416a0b51a00f38db4bef5c3f26e87ff14a8','Instructor','2026-01-05 17:37:33'),(28,'edip_admin','scrypt:32768:8:1$4JyJXPq3Hzoe9yHQ$788a48f0c3f06d6e0e4865fa4058bb7e41a50c0c45a938eb8bed2e47bffdc1c19dfe795548d2ed3bec043ac0d2c44d22dfb8b4c2ab36523ae67eee73b0d6a3ca','Admin','2026-01-05 17:43:14'),(29,'edip_instructor','scrypt:32768:8:1$GIBCiWpsfrMvmpv0$110a130fe8290171605867653a7eb945ae63715f225c706b6175db8979074ab77a13e45761e2e2a1f9e2be0d4d971959d1af5cb01ad0738b217c2f413904286d','Instructor','2026-01-05 17:45:26'),(30,'edip_student','scrypt:32768:8:1$zhahqn5r5p1TNge4$5c149899bc9f61aa67c366d31c3206c34b39a316a001f6eeb3476a808ad40708c985ead78c69b270a8613267a577a628f1f6c94ffa008b5e78986f5d3a65c2d3','Student','2026-01-05 17:48:54');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `view_high_performing_courses`
--

DROP TABLE IF EXISTS `view_high_performing_courses`;
/*!50001 DROP VIEW IF EXISTS `view_high_performing_courses`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `view_high_performing_courses` AS SELECT 
 1 AS `course_name`,
 1 AS `average_score`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `view_student_contacts`
--

DROP TABLE IF EXISTS `view_student_contacts`;
/*!50001 DROP VIEW IF EXISTS `view_student_contacts`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `view_student_contacts` AS SELECT 
 1 AS `first_name`,
 1 AS `last_name`,
 1 AS `email`,
 1 AS `username`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_section_performance`
--

DROP TABLE IF EXISTS `vw_section_performance`;
/*!50001 DROP VIEW IF EXISTS `vw_section_performance`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_section_performance` AS SELECT 
 1 AS `section_id`,
 1 AS `course_code`,
 1 AS `course_name`,
 1 AS `semester_name`,
 1 AS `year`,
 1 AS `instructor_name`,
 1 AS `enrolled_students`,
 1 AS `avg_score`,
 1 AS `min_score`,
 1 AS `max_score`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_student_transcript`
--

DROP TABLE IF EXISTS `vw_student_transcript`;
/*!50001 DROP VIEW IF EXISTS `vw_student_transcript`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_student_transcript` AS SELECT 
 1 AS `student_id`,
 1 AS `student_name`,
 1 AS `student_email`,
 1 AS `semester_name`,
 1 AS `year`,
 1 AS `course_code`,
 1 AS `course_name`,
 1 AS `credits`,
 1 AS `department`,
 1 AS `section_id`,
 1 AS `section_number`,
 1 AS `schedule`,
 1 AS `room`,
 1 AS `instructor_name`,
 1 AS `assessment_type`,
 1 AS `score`,
 1 AS `max_score`,
 1 AS `weight`,
 1 AS `letter_grade`,
 1 AS `section_avg_score`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'studentsystem'
--

--
-- Dumping routines for database 'studentsystem'
--
/*!50003 DROP FUNCTION IF EXISTS `CalculateStudentGPA` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `CalculateStudentGPA`(s_id INT) RETURNS decimal(5,2)
    DETERMINISTIC
BEGIN
    DECLARE avg_score DECIMAL(5,2);
    SELECT AVG(score) INTO avg_score
    FROM grades g
    JOIN enrollments e ON g.enrollment_id = e.enrollment_id
    WHERE e.student_id = s_id;
    RETURN IFNULL(avg_score, 0);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `fn_instructor_section_count` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `fn_instructor_section_count`(p_instructor_id INT, p_semester_id INT) RETURNS int
    DETERMINISTIC
BEGIN
    DECLARE cnt INT;

    SELECT COUNT(*)
      INTO cnt
      FROM sections s
     WHERE s.instructor_id = p_instructor_id
       AND s.semester_id   = p_semester_id;

    RETURN cnt;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `fn_letter_grade` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `fn_letter_grade`(p_score DECIMAL(5,2)) RETURNS varchar(2) CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci
    DETERMINISTIC
BEGIN
    DECLARE g VARCHAR(2);

    SET g = CASE
        WHEN p_score >= 90 THEN 'AA'
        WHEN p_score >= 85 THEN 'BA'
        WHEN p_score >= 80 THEN 'BB'
        WHEN p_score >= 75 THEN 'CB'
        WHEN p_score >= 70 THEN 'CC'
        WHEN p_score >= 65 THEN 'DC'
        WHEN p_score >= 60 THEN 'DD'
        WHEN p_score >= 50 THEN 'FD'
        ELSE 'FF'
    END;

    RETURN g;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `GetTotalEnrolled` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `GetTotalEnrolled`(sec_id INT) RETURNS int
    DETERMINISTIC
BEGIN
    DECLARE total INT;
    SELECT COUNT(*) INTO total
    FROM enrollments
    WHERE section_id = sec_id AND status = 'Active';
    RETURN total;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AnalyzeDeptPerformance` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AnalyzeDeptPerformance`()
BEGIN
    SELECT 
        c.department, 
        COUNT(c.course_id) as total_courses, 
        AVG(c.credits) as avg_credits
    FROM courses c
    GROUP BY c.department
    ORDER BY total_courses DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetStudentTranscript` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetStudentTranscript`(IN s_id INT)
BEGIN
    SELECT 
        c.course_code, 
        c.course_name, 
        g.assessment_type, 
        g.score 
    FROM enrollments e
    INNER JOIN sections s ON e.section_id = s.section_id
    INNER JOIN courses c ON s.course_id = c.course_id
    LEFT JOIN grades g ON e.enrollment_id = g.enrollment_id
    WHERE e.student_id = s_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_section_performance_stats` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_section_performance_stats`(IN p_section_id INT)
BEGIN
    /*
      Section bazında:
      - kaç öğrenci kayıtlı
      - grade ortalaması, min, max (score)
      - course, semester, instructor bilgileri
      JOIN + GROUP BY + AVG/MIN/MAX/COUNT içerir
    */
    SELECT
        s.section_id,
        c.course_code,
        c.course_name,
        sem.semester_name,
        sem.year,
        CONCAT(i.first_name, ' ', i.last_name) AS instructor_name,
        COUNT(DISTINCT e.enrollment_id) AS enrolled_students,
        AVG(g.score) AS avg_score,
        MIN(g.score) AS min_score,
        MAX(g.score) AS max_score
    FROM sections s
    JOIN courses c      ON c.course_id = s.course_id
    JOIN semesters sem  ON sem.semester_id = s.semester_id
    LEFT JOIN instructors i ON i.instructor_id = s.instructor_id
    LEFT JOIN enrollments e ON e.section_id = s.section_id
    LEFT JOIN grades g       ON g.enrollment_id = e.enrollment_id
    WHERE s.section_id = p_section_id
    GROUP BY
        s.section_id, c.course_code, c.course_name,
        sem.semester_name, sem.year, instructor_name;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_update_student_email` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_update_student_email`(IN p_student_id INT, IN p_new_email VARCHAR(255))
BEGIN
    /*
      Student email güncelle + güncel kaydı geri döndür
      UPDATE + SELECT içerir
    */
    UPDATE students
       SET email = p_new_email
     WHERE student_id = p_student_id;

    SELECT *
      FROM students
     WHERE student_id = p_student_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `view_high_performing_courses`
--

/*!50001 DROP VIEW IF EXISTS `view_high_performing_courses`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_high_performing_courses` AS select `c`.`course_name` AS `course_name`,avg(`g`.`score`) AS `average_score` from (((`courses` `c` join `sections` `s` on((`c`.`course_id` = `s`.`course_id`))) join `enrollments` `e` on((`s`.`section_id` = `e`.`section_id`))) join `grades` `g` on((`e`.`enrollment_id` = `g`.`enrollment_id`))) group by `c`.`course_name` having (avg(`g`.`score`) > 80) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `view_student_contacts`
--

/*!50001 DROP VIEW IF EXISTS `view_student_contacts`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_student_contacts` AS select `s`.`first_name` AS `first_name`,`s`.`last_name` AS `last_name`,`s`.`email` AS `email`,(select `u`.`username` from `users` `u` where (`u`.`user_id` = `s`.`user_id`)) AS `username` from `students` `s` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_section_performance`
--

/*!50001 DROP VIEW IF EXISTS `vw_section_performance`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_section_performance` AS select `sec`.`section_id` AS `section_id`,`c`.`course_code` AS `course_code`,`c`.`course_name` AS `course_name`,`sem`.`semester_name` AS `semester_name`,`sem`.`year` AS `year`,concat(`i`.`first_name`,' ',`i`.`last_name`) AS `instructor_name`,count(distinct `e`.`enrollment_id`) AS `enrolled_students`,avg(`g`.`score`) AS `avg_score`,min(`g`.`score`) AS `min_score`,max(`g`.`score`) AS `max_score` from (((((`sections` `sec` join `courses` `c` on((`c`.`course_id` = `sec`.`course_id`))) join `semesters` `sem` on((`sem`.`semester_id` = `sec`.`semester_id`))) left join `instructors` `i` on((`i`.`instructor_id` = `sec`.`instructor_id`))) left join `enrollments` `e` on((`e`.`section_id` = `sec`.`section_id`))) left join `grades` `g` on((`g`.`enrollment_id` = `e`.`enrollment_id`))) group by `sec`.`section_id`,`c`.`course_code`,`c`.`course_name`,`sem`.`semester_name`,`sem`.`year`,`instructor_name` having (avg(`g`.`score`) is not null) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_student_transcript`
--

/*!50001 DROP VIEW IF EXISTS `vw_student_transcript`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_student_transcript` AS select `st`.`student_id` AS `student_id`,concat(`st`.`first_name`,' ',`st`.`last_name`) AS `student_name`,`st`.`email` AS `student_email`,`sem`.`semester_name` AS `semester_name`,`sem`.`year` AS `year`,`c`.`course_code` AS `course_code`,`c`.`course_name` AS `course_name`,`c`.`credits` AS `credits`,`c`.`department` AS `department`,`sec`.`section_id` AS `section_id`,`sec`.`section_number` AS `section_number`,`sec`.`schedule` AS `schedule`,`sec`.`room` AS `room`,concat(`i`.`first_name`,' ',`i`.`last_name`) AS `instructor_name`,`g`.`assessment_type` AS `assessment_type`,`g`.`score` AS `score`,`g`.`max_score` AS `max_score`,`g`.`weight` AS `weight`,`fn_letter_grade`(`g`.`score`) AS `letter_grade`,(select avg(`g2`.`score`) from (`enrollments` `e2` join `grades` `g2` on((`g2`.`enrollment_id` = `e2`.`enrollment_id`))) where (`e2`.`section_id` = `sec`.`section_id`)) AS `section_avg_score` from ((((((`students` `st` join `enrollments` `e` on((`e`.`student_id` = `st`.`student_id`))) join `sections` `sec` on((`sec`.`section_id` = `e`.`section_id`))) join `courses` `c` on((`c`.`course_id` = `sec`.`course_id`))) join `semesters` `sem` on((`sem`.`semester_id` = `sec`.`semester_id`))) left join `instructors` `i` on((`i`.`instructor_id` = `sec`.`instructor_id`))) left join `grades` `g` on((`g`.`enrollment_id` = `e`.`enrollment_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-05 18:35:13
