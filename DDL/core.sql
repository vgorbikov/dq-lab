CREATE SCHEMA IF NOT EXISTS core;

-- 1. dim_client (SCD Type 2) - без изменений
CREATE TABLE core.dim_client (
    client_sk BIGSERIAL PRIMARY KEY,
    client_id TEXT NOT NULL,
    name TEXT,
    birthdate DATE,
    gender TEXT,
    phone_number TEXT,
    email TEXT,
    registration_dttm TIMESTAMPTZ,
    address_country TEXT,
    address_region TEXT,
    address_city TEXT,
    address_street TEXT,
    address_house TEXT,
    address_postal_code TEXT,
    src_system TEXT,
    effective_from_dttm TIMESTAMPTZ NOT NULL,
    effective_to_dttm TIMESTAMPTZ NOT NULL DEFAULT '9999-12-31 23:59:59',
    is_current BOOLEAN DEFAULT TRUE
);

-- 2. dim_product (SCD Type 2) - без изменений
CREATE TABLE core.dim_product (
    product_sk BIGSERIAL PRIMARY KEY,
    product_id TEXT NOT NULL,
    product_name TEXT,
    description TEXT,
    category_id INT,
    category_name TEXT,
    weight_kg INT,
    product_length INT,
    product_width INT,
    product_height INT,
    sku TEXT,
    price_value INT,
    price_currency_code TEXT,
    price_currency_name TEXT,
    src_system TEXT,
    effective_from_dttm TIMESTAMPTZ NOT NULL,
    effective_to_dttm TIMESTAMPTZ NOT NULL DEFAULT '9999-12-31 23:59:59',
    is_current BOOLEAN DEFAULT TRUE
);

-- 3. dim_pick_up_point (SCD Type 2) - без изменений
CREATE TABLE core.dim_pick_up_point (
    point_sk BIGSERIAL PRIMARY KEY,
    point_id TEXT NOT NULL,
    open_date DATE,
    address_country TEXT,
    address_region TEXT,
    address_city TEXT,
    address_street TEXT,
    address_house TEXT,
    address_postal_code TEXT,
    src_system TEXT,
    effective_from_dttm TIMESTAMPTZ NOT NULL,
    effective_to_dttm TIMESTAMPTZ NOT NULL DEFAULT '9999-12-31 23:59:59',
    is_current BOOLEAN DEFAULT TRUE
);

-- 4. dim_currency (без изменений)
CREATE TABLE core.dim_currency (
    currency_sk BIGSERIAL PRIMARY KEY,
    currency_code TEXT NOT NULL UNIQUE,
    currency_name TEXT,
    src_system TEXT
);

-- 5. fact_order_position (без date_sk!)
CREATE TABLE core.fact_order_position (
    order_position_sk BIGSERIAL PRIMARY KEY,
    order_id TEXT NOT NULL,
    client_sk BIGINT REFERENCES core.dim_client(client_sk),
    pick_up_point_sk BIGINT REFERENCES core.dim_pick_up_point(point_sk),
    product_sk BIGINT REFERENCES core.dim_product(product_sk),
    currency_sk BIGINT REFERENCES core.dim_currency(currency_sk),
    position_quantity INT,
    status TEXT,
    track_number TEXT,
    total_price_value INT,
    creation_dttm TIMESTAMPTZ,        
    update_dttm TIMESTAMPTZ,            
    effective_from_dttm TIMESTAMPTZ NOT NULL,
    effective_to_dttm TIMESTAMPTZ NOT NULL DEFAULT '9999-12-31 23:59:59'
);

-- 6. fact_supply_position (без date_sk!)
CREATE TABLE core.fact_supply_position (
    supply_position_sk BIGSERIAL PRIMARY KEY,
    supply_id TEXT NOT NULL,
    product_sk BIGINT REFERENCES core.dim_product(product_sk),
    quantity INT,
    batch_number TEXT,
    supply_datetime TIMESTAMPTZ     
);

-- 7. fact_shipment_position (без date_sk!)
CREATE TABLE core.fact_shipment_position (
    shipment_position_sk BIGSERIAL PRIMARY KEY,
    shipment_id TEXT NOT NULL,
    product_sk BIGINT REFERENCES core.dim_product(product_sk),
    quantity INT,
    shipment_datetime TIMESTAMPTZ 
);

-- 8. fact_stock_snapshot (без date_sk!)
CREATE TABLE core.fact_stock_snapshot (
    product_sk BIGINT REFERENCES core.dim_product(product_sk),
    snapshot_dttm TIMESTAMPTZ,
    quantity INT,
    PRIMARY KEY (product_sk, snapshot_dttm)
);