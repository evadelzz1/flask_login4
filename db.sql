create database flask_login4;

use flask_login4;

drop table if exists users;

create table users (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(50) NOT NULL,
  email varchar(50) NOT NULL,
  password varchar(60) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email (email)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;