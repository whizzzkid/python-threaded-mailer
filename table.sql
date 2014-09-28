CREATE DATABASE IF NOT EXISTS `mailer`;
USE `mailer`

CREATE TABLE IF NOT EXISTS `mailing_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `mail` varchar(256) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `sent_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `thread` varchar(32) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `mail` (`mail`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10001 ;
