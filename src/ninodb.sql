/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 5.5.20-log : Database - nino_care
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`nino_care` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `nino_care`;

/*Table structure for table `area` */

DROP TABLE IF EXISTS `area`;

CREATE TABLE `area` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) DEFAULT NULL,
  `area` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `area` */

insert  into `area`(`id`,`pid`,`area`) values 
(4,2,'keezhatur');

/*Table structure for table `ashaworker` */

DROP TABLE IF EXISTS `ashaworker`;

CREATE TABLE `ashaworker` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `l_id` int(11) DEFAULT NULL,
  `panchayath_id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `pin` bigint(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `ph_no` bigint(20) DEFAULT NULL,
  `area` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `ashaworker` */

insert  into `ashaworker`(`id`,`l_id`,`panchayath_id`,`name`,`place`,`post`,`pin`,`email`,`ph_no`,`area`) values 
(3,6,2,'pallavi','taliparamba','kannur',670141,'pallavisasi17@gmail.com',977813665,'3');

/*Table structure for table `child` */

DROP TABLE IF EXISTS `child`;

CREATE TABLE `child` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `child` */

/*Table structure for table `food` */

DROP TABLE IF EXISTS `food`;

CREATE TABLE `food` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `food` varchar(50) DEFAULT NULL,
  `image` varchar(50) DEFAULT NULL,
  `details` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `food` */

insert  into `food`(`id`,`food`,`image`,`details`,`type`) values 
(3,'Dry fruites.','dryfruit.jpg','healthy.','mother');

/*Table structure for table `gov_schemes` */

DROP TABLE IF EXISTS `gov_schemes`;

CREATE TABLE `gov_schemes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `scheme_name` varchar(50) DEFAULT NULL,
  `details` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `gov_schemes` */

insert  into `gov_schemes`(`id`,`scheme_name`,`details`,`date`) values 
(2,'matha yojana','scheme for mothers','2024-08-31');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`id`,`username`,`password`,`type`) values 
(1,'admin','admin','admin'),
(2,'keezhariyoor','keezhariyoor','panchayath');

/*Table structure for table `panchayath` */

DROP TABLE IF EXISTS `panchayath`;

CREATE TABLE `panchayath` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `l_id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `taluk_name` varchar(50) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `ph_no` bigint(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `panchayath` */

insert  into `panchayath`(`id`,`l_id`,`name`,`taluk_name`,`district`,`ph_no`,`email`) values 
(1,2,'keezhariyur1','koyilandy','kozhikode',9778136652,'keezh@gmail.com');

/*Table structure for table `programs` */

DROP TABLE IF EXISTS `programs`;

CREATE TABLE `programs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `panchayath_id` int(11) DEFAULT NULL,
  `program` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `programs` */

insert  into `programs`(`id`,`panchayath_id`,`program`,`date`) values 
(2,2,'Pallavi_k_-43.pdf','2024-09-02');

/*Table structure for table `reports` */

DROP TABLE IF EXISTS `reports`;

CREATE TABLE `reports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `panchayath_id` int(11) DEFAULT NULL,
  `report` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `reports` */

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `l_id` int(11) DEFAULT NULL,
  `panchayath_id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `pin` bigint(20) DEFAULT NULL,
  `area` varchar(50) DEFAULT NULL,
  `ph_no` bigint(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `no_of_child` int(11) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `latitude` varchar(50) DEFAULT NULL,
  `longitude` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `user` */

/*Table structure for table `vaccine` */

DROP TABLE IF EXISTS `vaccine`;

CREATE TABLE `vaccine` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `panchayath_id` int(11) DEFAULT NULL,
  `vaccine_name` varchar(50) DEFAULT NULL,
  `details` text,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `vaccine` */

insert  into `vaccine`(`id`,`panchayath_id`,`vaccine_name`,`details`,`type`) values 
(2,2,'pulse polio','Kids under 5 should take the vaccine\r\n','Child');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
