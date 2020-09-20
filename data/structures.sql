DROP TABLE IF EXISTS stocks;
CREATE TABLE IF NOT EXISTS stocks(
    signature         VARCHAR(8) PRIMARY KEY NOT NULL,
    name              VARCHAR(30) NOT NULL,
    currency          CHAR(3) NOT NULL DEFAULT 'SEK',
    dividend_per_year INT NOT NULL DEFAULT 1,
    dividend_forecast FLOAT NOT NULL DEFAULT 0.0);

DROP TABLE IF EXISTS stock_bloomberg;
CREATE TABLE IF NOT EXISTS stock_bloomberg(
stock VARCHAR(8) REFERENCES stocks(signature),
bloomberg_signature VARCHAR(20)UNIQUE NOT NULL,
PRIMARY KEY(stock, bloomberg_signature));

DROP TABLE IF EXISTS stock_avanza;
CREATE TABLE IF NOT EXISTS stock_avanza(
stock VARCHAR(8) REFERENCES stocks(signature),
stock_id INT NOT NULL,
stock_name VARCHAR(32)NOT NULL,
is_stock INT NOT NULL DEFAULT 1,
PRIMARY KEY(stock, stock_id, stock_name, is_stock));

DROP TABLE IF EXISTS prices;
CREATE TABLE IF NOT EXISTS prices(
stock VARCHAR(8) REFERENCES stocks(signature),
price_date DATE NOT NULL,
price FLOAT NOT NULL DEFAULT 0.0,
UNIQUE(stock, price_date));

DROP TABLE IF EXISTS stock_identifier;
CREATE TABLE IF NOT EXISTS stock_identifier(
stock VARCHAR(8) REFERENCES stocks(signature),
identifier VARCHAR(32)UNIQUE NOT NULL,
PRIMARY KEY(stock, identifier));

DROP TABLE IF EXISTS transactions;
CREATE TABLE IF NOT EXISTS transactions(
    trans_date DATE NOT NULL,
    trans_type VARCHAR(10) NOT NULL,
stock VARCHAR(8) REFERENCES stocks(signature),
units FLOAT NOT NULL DEFAULT 0.0,
price FLOAT NOT NULL DEFAULT 0.0,
fees FLOAT NOT NULL DEFAULT 0.0,
split_ratio FLOAT DEFAULT 1.0,
UNIQUE(trans_date, trans_type, stock, units, price, fees, split_ratio));

DROP TABLE IF EXISTS split_ratio;
CREATE TABLE IF NOT EXISTS split_ratio(
stock VARCHAR(8) REFERENCES stocks(signature),
ratio FLOAT NOT NULL DEFAULT 1.0);

