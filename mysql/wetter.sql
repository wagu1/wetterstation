CREATE TABLE `indoor` (
	`id`          int(11)    NOT NULL AUTO_INCREMENT,
	`time`        timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`temperature` float(4,2) NOT NULL,
	`pressure`    float(6,2) NOT NULL,
	`humidity`    float(3,1) NOT NULL,
	PRIMARY KEY (`id`)
	) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8

CREATE TABLE `outdoor` (
	`id`          int(11)    NOT NULL AUTO_INCREMENT,
	`time`        timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`temperature` float(4,2) NOT NULL,
	`pressure`    float(6,2) NOT NULL,
	`humidity`    float(3,1) NOT NULL,
	PRIMARY KEY (`id`)
	) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
