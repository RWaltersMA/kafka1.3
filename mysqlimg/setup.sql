CREATE DATABASE Stocks;
USE Stocks;

CREATE TABLE StockData (company_symbol VARCHAR(10), company_name VARCHAR(100),price DECIMAL(6,2), tx_time TIMESTAMP);

CREATE USER 'mysqluser'@'%' IDENTIFIED BY 'pass@word1';
ALTER USER 'mysqluser'@'%' IDENTIFIED WITH mysql_native_password BY 'pass@word1';

GRANT ALL PRIVILEGES ON *.* TO 'mysqluser'@'%';


