CREATE TABLE `departments` (
  `id` int NOT NULL,
  `department` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `jobs` (
  `id` int NOT NULL,
  `job` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `hired_employees` (
  `id` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `datetime` varchar(255) DEFAULT NULL,
  `department_id` int DEFAULT NULL,
  `job_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
);
