-- ============================================================
-- Схема для сырых данных
-- ============================================================
CREATE SCHEMA IF NOT EXISTS raw;

-- ============================================================
-- 1. Клиенты
-- ============================================================
CREATE TABLE raw.raw_client (
    client_id TEXT,
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
    src_system TEXT NOT NULL DEFAULT 'client_service',
    load_dttm TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (client_id, load_dttm)
);

COMMENT ON TABLE raw.raw_client IS 'Сырые данные по клиентам';
COMMENT ON COLUMN raw.raw_client.client_id IS 'ID клиента';
COMMENT ON COLUMN raw.raw_client.name IS 'ФИО клиента';
COMMENT ON COLUMN raw.raw_client.birthdate IS 'Дата рождения клиента';
COMMENT ON COLUMN raw.raw_client.gender IS 'Пол клиента';
COMMENT ON COLUMN raw.raw_client.phone_number IS 'Номер телефона клиента';
COMMENT ON COLUMN raw.raw_client.email IS 'Электронная почта клиента';
COMMENT ON COLUMN raw.raw_client.registration_dttm IS 'Дата регистрации клиента';
COMMENT ON COLUMN raw.raw_client.address_country IS 'Страна проживания';
COMMENT ON COLUMN raw.raw_client.address_region IS 'Регион';
COMMENT ON COLUMN raw.raw_client.address_city IS 'Город';
COMMENT ON COLUMN raw.raw_client.address_street IS 'Название улицы';
COMMENT ON COLUMN raw.raw_client.address_house IS 'Номер дома';
COMMENT ON COLUMN raw.raw_client.address_postal_code IS 'Почтовый индекс';
COMMENT ON COLUMN raw.raw_client.src_system IS 'Наименование системы-источника';
COMMENT ON COLUMN raw.raw_client.load_dttm IS 'Время загрузки записи с источника';

-- Индексы для поиска
CREATE INDEX idx_raw_client_load_dttm ON raw.raw_client(load_dttm);


-- ============================================================
-- 2. Продукты
-- ============================================================
CREATE TABLE raw.raw_product (
    product_id TEXT,
    product_name TEXT,
    description TEXT,
    category_id INT,
    weight_kg INT,
    product_length INT,
    product_width INT,
    product_height INT,
    sku TEXT,
    price_value INT,
    price_currency TEXT,
    src_system TEXT NOT NULL DEFAULT 'product_service',
    load_dttm TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (product_id, load_dttm)
);

COMMENT ON TABLE raw.raw_product IS 'Сырые данные по продуктам';
COMMENT ON COLUMN raw.raw_product.product_id IS 'ID продукта';
COMMENT ON COLUMN raw.raw_product.product_name IS 'Наименование продукта';
COMMENT ON COLUMN raw.raw_product.description IS 'Описание продукта';
COMMENT ON COLUMN raw.raw_product.category_id IS 'Ссылка на категорию';
COMMENT ON COLUMN raw.raw_product.weight_kg IS 'Вес единицы товара в кг';
COMMENT ON COLUMN raw.raw_product.product_length IS 'Длина упаковки';
COMMENT ON COLUMN raw.raw_product.product_width IS 'Ширина упаковки';
COMMENT ON COLUMN raw.raw_product.product_height IS 'Высота упаковки';
COMMENT ON COLUMN raw.raw_product.sku IS 'Номер единицы складского учёта';
COMMENT ON COLUMN raw.raw_product.price_value IS 'Цена продукта';
COMMENT ON COLUMN raw.raw_product.price_currency IS 'Ссылка на валюту цены';
COMMENT ON COLUMN raw.raw_product.src_system IS 'Наименование системы-источника';
COMMENT ON COLUMN raw.raw_product.load_dttm IS 'Время загрузки записи с источника';

CREATE INDEX idx_raw_product_load_dttm ON raw.raw_product(load_dttm);


-- ============================================================
-- 3. Категории продуктов
-- ============================================================
CREATE TABLE raw.raw_category (
    category_id INT,
    category_name TEXT,
    description TEXT,
    src_system TEXT NOT NULL DEFAULT 'product_service',
    load_dttm TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (category_id, load_dttm)
);

COMMENT ON TABLE raw.raw_category IS 'Сырые данные по категориям продуктов';
COMMENT ON COLUMN raw.raw_category.category_id IS 'ID категории';
COMMENT ON COLUMN raw.raw_category.category_name IS 'Наименование категории';
COMMENT ON COLUMN raw.raw_category.description IS 'Описание категории';
COMMENT ON COLUMN raw.raw_category.src_system IS 'Наименование системы-источника';
COMMENT ON COLUMN raw.raw_category.load_dttm IS 'Время загрузки записи с источника';

CREATE INDEX idx_raw_category_load_dttm ON raw.raw_category(load_dttm);


-- ============================================================
-- 4. Валюты
-- ============================================================
CREATE TABLE raw.raw_currency (
    currency_code TEXT,
    currency_name TEXT,
    src_system TEXT NOT NULL DEFAULT 'product_service',
    load_dttm TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (currency_code, load_dttm)
);

COMMENT ON TABLE raw.raw_currency IS 'Сырые данные по валютам';
COMMENT ON COLUMN raw.raw_currency.currency_code IS 'Буквенный код валюты';
COMMENT ON COLUMN raw.raw_currency.currency_name IS 'Наименование валюты';
COMMENT ON COLUMN raw.raw_currency.src_system IS 'Наименование системы-источника';
COMMENT ON COLUMN raw.raw_currency.load_dttm IS 'Время загрузки записи с источника';

-- CREATE INDEX idx_raw_currency_load_dttm ON raw.raw_currency(load_dttm);


-- ============================================================
-- 5. Складские остатки
-- ============================================================
CREATE TABLE raw.raw_stock (
    product_id TEXT,
    last_update TIMESTAMPTZ,
    quantity INT,
    src_system TEXT NOT NULL DEFAULT 'product_service',
    load_dttm TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (product_id, last_update, load_dttm)
);

COMMENT ON TABLE raw.raw_stock IS 'Сырые данные по складским остаткам';
COMMENT ON COLUMN raw.raw_stock.product_id IS 'Ссылка на продукт';
COMMENT ON COLUMN raw.raw_stock.last_update IS 'Время последнего обновления остатка';
COMMENT ON COLUMN raw.raw_stock.quantity IS 'Остаток, единиц продукции';
COMMENT ON COLUMN raw.raw_stock.src_system IS 'Наименование системы-источника';
COMMENT ON COLUMN raw.raw_stock.load_dttm IS 'Время загрузки записи с источника';

CREATE INDEX idx_raw_stock_product ON raw.raw_stock(product_id);
CREATE INDEX idx_raw_stock_load_dttm ON raw.raw_stock(load_dttm);


-- ============================================================
-- 6. Поставки
-- ============================================================
CREATE TABLE raw.raw_supply (
    supply_id TEXT,
    supply_datetime TIMESTAMPTZ,
    src_system TEXT NOT NULL DEFAULT 'product_service',
    load_dttm TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (supply_id, load_dttm)
);

COMMENT ON TABLE raw.raw_supply IS 'Сырые данные по поставкам';
COMMENT ON COLUMN raw.raw_supply.supply_id IS 'ID поставки';
COMMENT ON COLUMN raw.raw_supply.supply_datetime IS 'Время поставки';
COMMENT ON COLUMN raw.raw_supply.src_system IS 'Наименование системы-источника';
COMMENT ON COLUMN raw.raw_supply.load_dttm IS 'Время загрузки записи с источника';

-- CREATE INDEX idx_raw_supply_datetime ON raw.raw_supply(supply_datetime);
-- CREATE INDEX idx_raw_supply_load_dttm ON raw.raw_supply(load_dttm);


-- ============================================================
-- 7. Позиции поставок
-- ============================================================
CREATE TABLE raw.raw_supply_item (
    supply_id TEXT,
    product_id TEXT,
    quantity INT,
    batch_number TEXT,
    src_system TEXT NOT NULL DEFAULT 'product_service',
    load_dttm TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (supply_id, product_id, load_dttm)
);

COMMENT ON TABLE raw.raw_supply_item IS 'Сырые данные по позициям поставок';
COMMENT ON COLUMN raw.raw_supply_item.supply_id IS 'Ссылка на поставку';
COMMENT ON COLUMN raw.raw_supply_item.product_id IS 'Ссылка на продукт';
COMMENT ON COLUMN raw.raw_supply_item.quantity IS 'Количество единиц продукции';
COMMENT ON COLUMN raw.raw_supply_item.batch_number IS 'Номер партии';
COMMENT ON COLUMN raw.raw_supply_item.src_system IS 'Наименование системы-источника';
COMMENT ON COLUMN raw.raw_supply_item.load_dttm IS 'Время загрузки записи с источника';

-- CREATE INDEX idx_raw_supply_item_product ON raw.raw_supply_item(product_id);
-- CREATE INDEX idx_raw_supply_item_load_dttm ON raw.raw_supply_item(load_dttm);


-- ============================================================
-- 8. Отгрузки
-- ============================================================
CREATE TABLE raw.raw_shipment (
    shipment_id TEXT,
    shipment_datetime TIMESTAMPTZ,
    src_system TEXT NOT NULL DEFAULT 'product_service',
    load_dttm TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (shipment_id, load_dttm)
);

COMMENT ON TABLE raw.raw_shipment IS 'Сырые данные по отгрузкам';
COMMENT ON COLUMN raw.raw_shipment.shipment_id IS 'ID отгрузки';
COMMENT ON COLUMN raw.raw_shipment.shipment_datetime IS 'Время отгрузки';
COMMENT ON COLUMN raw.raw_shipment.src_system IS 'Наименование системы-источника';
COMMENT ON COLUMN raw.raw_shipment.load_dttm IS 'Время загрузки записи с источника';

-- CREATE INDEX idx_raw_shipment_datetime ON raw.raw_shipment(shipment_datetime);
-- CREATE INDEX idx_raw_shipment_load_dttm ON raw.raw_shipment(load_dttm);


-- ============================================================
-- 9. Позиции отгрузок
-- ============================================================
CREATE TABLE raw.raw_shipment_item (
    shipment_id TEXT,
    product_id TEXT,
    quantity INT,
    src_system TEXT NOT NULL DEFAULT 'product_service',
    load_dttm TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (shipment_id, product_id, load_dttm)
);

COMMENT ON TABLE raw.raw_shipment_item IS 'Сырые данные по позициям отгрузок';
COMMENT ON COLUMN raw.raw_shipment_item.shipment_id IS 'Ссылка на отгрузку';
COMMENT ON COLUMN raw.raw_shipment_item.product_id IS 'Ссылка на продукт';
COMMENT ON COLUMN raw.raw_shipment_item.quantity IS 'Количество единиц товара';
COMMENT ON COLUMN raw.raw_shipment_item.src_system IS 'Наименование системы-источника';
COMMENT ON COLUMN raw.raw_shipment_item.load_dttm IS 'Время загрузки записи с источника';

-- CREATE INDEX idx_raw_shipment_item_product ON raw.raw_shipment_item(product_id);
-- CREATE INDEX idx_raw_shipment_item_load_dttm ON raw.raw_shipment_item(load_dttm);


-- ============================================================
-- 10. Заказы
-- ============================================================
CREATE TABLE raw.raw_order (
    order_id TEXT,
    client_id TEXT,
    pick_up_point_id TEXT,
    status TEXT,
    track_number TEXT,
    total_price_value INT,
    total_price_currency TEXT,
    creation_dttm TIMESTAMPTZ,
    update_dttm TIMESTAMPTZ,
    src_system TEXT NOT NULL DEFAULT 'order_service',
    load_dttm TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (order_id, load_dttm)
);

COMMENT ON TABLE raw.raw_order IS 'Сырые данные по заказам';
COMMENT ON COLUMN raw.raw_order.order_id IS 'ID заказа';
COMMENT ON COLUMN raw.raw_order.client_id IS 'Ссылка на клиента';
COMMENT ON COLUMN raw.raw_order.pick_up_point_id IS 'Ссылка на пункт выдачи';
COMMENT ON COLUMN raw.raw_order.status IS 'Статус заказа';
COMMENT ON COLUMN raw.raw_order.track_number IS 'Трек-номер заказа';
COMMENT ON COLUMN raw.raw_order.total_price_value IS 'Итоговая цена';
COMMENT ON COLUMN raw.raw_order.total_price_currency IS 'Ссылка на валюту';
COMMENT ON COLUMN raw.raw_order.creation_dttm IS 'Время создания заказа';
COMMENT ON COLUMN raw.raw_order.update_dttm IS 'Время последнего обновления заказа';
COMMENT ON COLUMN raw.raw_order.src_system IS 'Наименование системы-источника';
COMMENT ON COLUMN raw.raw_order.load_dttm IS 'Время загрузки записи с источника';

CREATE INDEX idx_raw_order_client ON raw.raw_order(client_id);
CREATE INDEX idx_raw_order_id ON raw.raw_order(order_id);
CREATE INDEX idx_raw_order_status ON raw.raw_order(status);
CREATE INDEX idx_raw_order_load_dttm ON raw.raw_order(load_dttm);


-- ============================================================
-- 11. Позиции заказов
-- ============================================================
CREATE TABLE raw.raw_order_position (
    order_id TEXT,
    product_id TEXT,
    quantity INT,
    src_system TEXT NOT NULL DEFAULT 'order_service',
    load_dttm TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (order_id, product_id, load_dttm)
);

COMMENT ON TABLE raw.raw_order_position IS 'Сырые данные по позициям заказов';
COMMENT ON COLUMN raw.raw_order_position.order_id IS 'Ссылка на заказ';
COMMENT ON COLUMN raw.raw_order_position.product_id IS 'Ссылка на продукт';
COMMENT ON COLUMN raw.raw_order_position.quantity IS 'Количество единиц товара';
COMMENT ON COLUMN raw.raw_order_position.src_system IS 'Наименование системы-источника';
COMMENT ON COLUMN raw.raw_order_position.load_dttm IS 'Время загрузки записи с источника';

CREATE INDEX idx_raw_order_position_product ON raw.raw_order_position(product_id);
CREATE INDEX idx_raw_order_position_load_dttm ON raw.raw_order_position(load_dttm);
CREATE INDEX idx_raw_order_position_order_id ON raw.raw_order_position(order_id);


-- ============================================================
-- 12. Пункты выдачи
-- ============================================================
CREATE TABLE raw.raw_pick_up_point (
    point_id TEXT,
    open_date DATE,
    address_country TEXT,
    address_region TEXT,
    address_city TEXT,
    address_street TEXT,
    address_house TEXT,
    address_postal_code TEXT,
    src_system TEXT NOT NULL DEFAULT 'order_service',
    load_dttm TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (point_id, load_dttm)
);

COMMENT ON TABLE raw.raw_pick_up_point IS 'Сырые данные по пунктам выдачи';
COMMENT ON COLUMN raw.raw_pick_up_point.point_id IS 'ID пункта выдачи';
COMMENT ON COLUMN raw.raw_pick_up_point.open_date IS 'Дата открытия пункта выдачи';
COMMENT ON COLUMN raw.raw_pick_up_point.address_country IS 'Страна';
COMMENT ON COLUMN raw.raw_pick_up_point.address_region IS 'Регион';
COMMENT ON COLUMN raw.raw_pick_up_point.address_city IS 'Город';
COMMENT ON COLUMN raw.raw_pick_up_point.address_street IS 'Название улицы';
COMMENT ON COLUMN raw.raw_pick_up_point.address_house IS 'Номер дома';
COMMENT ON COLUMN raw.raw_pick_up_point.address_postal_code IS 'Почтовый индекс';
COMMENT ON COLUMN raw.raw_pick_up_point.src_system IS 'Наименование системы-источника';
COMMENT ON COLUMN raw.raw_pick_up_point.load_dttm IS 'Время загрузки записи с источника';

-- CREATE INDEX idx_raw_pick_up_point_city ON raw.raw_pick_up_point(address_city);
-- CREATE INDEX idx_raw_pick_up_point_load_dttm ON raw.raw_pick_up_point(load_dttm);