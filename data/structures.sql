DROP TABLE IF EXISTS stocks;
CREATE TABLE IF NOT EXISTS stocks (
    signature VARCHAR(8) PRIMARY KEY NOT NULL,
    name VARCHAR(30) NOT NULL,
    exchange VARCHAR(12),
    currency CHAR(3) NOT NULL DEFAULT 'SEK');

DROP TABLE IF EXISTS stock_identifier;
CREATE TABLE IF NOT EXISTS stock_identifier (
    stock VARCHAR(8) REFERENCES stocks(signature),
    identifier VARCHAR(32) NOT NULL,
    PRIMARY KEY (stock, identifier));

DROP TABLE IF EXISTS transactions;
CREATE TABLE IF NOT EXISTS transactions (
    trans_date DATE NOT NULL,
    trans_type VARCHAR(10) NOT NULL,
    stock VARCHAR(8) REFERENCES stocks(signature),
    units FLOAT NOT NULL,
    price FLOAT NOT NULL,
    fees FLOAT NOT NULL DEFAULT 0.0,
    split_ratio FLOAT DEFAULT 1.0,
    UNIQUE (trans_date, trans_type, stock, units, price, fees, split_ratio));

