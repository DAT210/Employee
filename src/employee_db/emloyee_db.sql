DROP DATABASE IF EXISTS employee;

CREATE DATABASE emloyee;

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
    FOREIGN KEY (access_lvl) REFERENCES access_level(access_lvl)
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
("Admin", 0)

INSERT INTO users (emp_id, username, pass, access_lvl) VALUES
(1, "hr_admin", "pass", 1),
(2, "hr_user", "pass", 2),
(3, "menu_admin", "pass", 1),
(4, "menu_user", "pass", 2),
(5, "delivery_user", "pass", 2),
(6, "serving_user", "pass", 2),
(7, "admin", "admin", 0)