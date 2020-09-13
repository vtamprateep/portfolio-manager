/* CREATE TABLES IN DATABASE */

CREATE TABLE securities_holding (
    symbol  VARCHAR(10) PRIMARY KEY,
    description VARCHAR(200) DEFAULT null,
    asset_type  VARCHAR(20) DEFAULT null,
    main_type   VARCHAR(20) DEFAULT null,
    quantity    INTEGER DEFAULT 0,
    target  INTEGER DEFAULT 0
);

CREATE TABLE securities_prices (
    symbol  VARCHAR(10),
    datetime    DATE,
    open    REAL,
    high    REAL,
    low     REAL,
    close   REAL,
    CONSTRAINT fk_symbol FOREIGN KEY (symbol) REFERENCES securities_holding(symbol)
);

/* POPULATE SECURITIES_HOLDING TABLE */

