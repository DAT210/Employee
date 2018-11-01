DROP DATABASE IF EXISTS employee;

CREATE DATABASE employee;

USE employee;

/* tables */

CREATE TABLE access_level (
    access_lvl INT NOT NULL UNIQUE,
    access_code VARCHAR(80),
    PRIMARY KEY (access_lvl)
);

CREATE TABLE employee_group (
    group_id INT NOT NULL UNIQUE,
    group_name VARCHAR(80),
    PRIMARY KEY (group_id)
);

CREATE TABLE employee (
    emp_id INT AUTO_INCREMENT,
    emp_name VARCHAR(200),
    group_id INT,
    PRIMARY KEY (emp_id),
    FOREIGN KEY (group_id) REFERENCES employee_group(group_id)
);

CREATE TABLE users (
    emp_id INT,
    username VARCHAR(20) NOT NULL UNIQUE,
    pass VARCHAR(600),
    access_lvl INT,
    PRIMARY KEY (username),
    FOREIGN KEY (access_lvl) REFERENCES access_level(access_lvl),
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
);

CREATE TABLE `timesheet` (
  `emp_id` int(11) NOT NULL,
  `work_date` date NOT NULL,
  `work_start` time NOT NULL,
  `work_finish` time NOT NULL,
  `clock_in` time DEFAULT NULL,
  `clock_out` time DEFAULT NULL,
  PRIMARY KEY (`emp_id`,`work_date`),
  FOREIGN KEY (`emp_id`) REFERENCES `employee` (`emp_id`)
);

/* populate */

INSERT INTO access_level (access_lvl, access_code) VALUES
(1, "admin"),
(2, "user");

INSERT INTO employee_group (group_id, group_name) VALUES
(0, "admin"),
(1, "HR"),
(2, "Food Preparation"),
(3, "Delivery"),
(4, "Serving");

INSERT INTO employee (emp_name, group_id) VALUES
("HR Admin", 1),
("HR User", 1),
("Food Prep Admin", 2),
("Food Prep User", 2),
("Delivery User", 3),
("Serving User", 4),
("Admin", 0);

INSERT INTO users (emp_id, username, pass, access_lvl) VALUES
(1, "hr_admin", "pass", 1),
(2, "hr_user", "pass", 2),
(3, "menu_admin", "pass", 1),
(4, "menu_user", "pass", 2),
(5, "delivery_user", "pass", 2),
(6, "serving_user", "pass", 2),
(7, "admin", "admin", 1);

INSERT INTO `timesheet` VALUES 
(6,'2018-10-31','13:00:00','21:00:00',NULL,NULL),
(5,'2018-10-31','08:00:00','16:00:00','12:16:38','12:16:45'),
(4,'2018-10-31','06:00:00','12:00:00','05:59:45','12:00:01');