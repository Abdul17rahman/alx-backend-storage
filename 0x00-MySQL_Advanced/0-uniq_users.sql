-- Script that creates users table.
CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) UNIQUE,
	name VARCHAR(255)	
);
