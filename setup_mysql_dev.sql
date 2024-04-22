-- Create or use the database hbnb_dev_db
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create or use the user hbnb_dev with the password hbnb_dev_pwd
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant privileges to the user hbnb_dev on the database hbnb_dev_db
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant SELECT privilege on the performance_schema database
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

CREATE TABLE IF NOT EXISTS hbnb_dev_db.states (
    id VARCHAR(60) PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS hbnb_dev_db.cities (
    id VARCHAR(60) PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);