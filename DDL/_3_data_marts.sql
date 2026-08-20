-- ============================================================
-- Схема для прикладных витрин (Mart Layer)
-- ============================================================
CREATE SCHEMA IF NOT EXISTS mart;
COMMENT ON SCHEMA mart IS 'Слой прикладных витрин данных';

-- ============================================================
-- Витрина: mart_agg_client_order
-- Описание: Сводные данные по заказам - какой клиент, 
--           на какой пункт выдачи делал заказы.
-- Источник: core.fact_order_position + core.dim_client + 
--           core.dim_pick_up_point + core.dim_currency
-- ============================================================
CREATE OR REPLACE VIEW mart.mart_agg_client_order AS
SELECT 
    fop.order_id,
    fop.status,
    fop.track_number,
    count(1) as positions_count,
    fop.total_price_value,
    dc.currency_code AS total_price_currency_code,
    dc.currency_name AS total_price_currency_name,
    fop.creation_dttm,
    fop.update_dttm,
    -- Данные клиента (из dim_client)
    c.client_id,
    c.name AS client_name,
    c.birthdate AS client_birthdate,
    c.gender AS client_gender,
    c.phone_number AS client_phone_number,
    c.email AS client_email,
    c.registration_dttm AS client_registration_dttm,
    c.address_country AS client_address_country,
    c.address_region AS client_address_region,
    c.address_city AS client_address_city,
    c.address_street AS client_address_street,
    c.address_house AS client_address_house,
    c.address_postal_code AS client_address_postal_code,
    -- Данные пункта выдачи (из dim_pick_up_point)
    pp.point_id AS pick_up_point_id,
    pp.open_date AS point_open_date,
    pp.address_country AS point_address_country,
    pp.address_region AS point_address_region,
    pp.address_city AS point_address_city,
    pp.address_street AS point_address_street,
    pp.address_house AS point_address_house,
    pp.address_postal_code AS point_address_postal_code
FROM core.fact_order_position fop
-- Присоединяем клиента (только текущую версию)
LEFT JOIN core.dim_client c 
    ON fop.client_sk = c.client_sk 
    AND c.is_current = TRUE
-- Присоединяем пункт выдачи (только текущую версию)
LEFT JOIN core.dim_pick_up_point pp 
    ON fop.pick_up_point_sk = pp.point_sk 
    AND pp.is_current = TRUE
-- Присоединяем валюту
LEFT JOIN core.dim_currency dc 
    ON fop.total_price_currency_sk = dc.currency_sk
-- Берем только актуальные версии факта (последний статус)
WHERE fop.effective_to_dttm = '9999-12-31 23:59:59+03'::TIMESTAMPTZ
group by
	fop.order_id
    , fop.status
    , fop.track_number
    , fop.total_price_value
    , fop.creation_dttm
    , fop.update_dttm
	, dc.currency_code
	, dc.currency_name
	, c.client_id
    , c.name
    , c.birthdate
    , c.gender
    , c.phone_number
    , c.email
    , c.registration_dttm
    , c.address_country
    , c.address_region
    , c.address_city
    , c.address_street
    , c.address_house
    , c.address_postal_code
    -- Данные пункта выдачи (из dim_pick_up_point)
    , pp.point_id
    , pp.open_date
    , pp.address_country
    , pp.address_region
    , pp.address_city
    , pp.address_street
    , pp.address_house
    , pp.address_postal_code;

COMMENT ON VIEW mart.mart_agg_client_order IS 
'Сводные данные по заказам - информация о клиенте, пункте выдачи и самом заказе';
COMMENT ON COLUMN mart.mart_agg_client_order.order_id IS 'ID заказа';
COMMENT ON COLUMN mart.mart_agg_client_order.client_id IS 'ID клиента';
COMMENT ON COLUMN mart.mart_agg_client_order.client_name IS 'ФИО клиента';
COMMENT ON COLUMN mart.mart_agg_client_order.status IS 'Статус заказа';
COMMENT ON COLUMN mart.mart_agg_client_order.total_price_value IS 'Итоговая цена';
COMMENT ON COLUMN mart.mart_agg_client_order.pick_up_point_id IS 'ID пункта выдачи';
COMMENT ON COLUMN mart.mart_agg_client_order.point_open_date IS 'Дата открытия пункта выдачи';

-- ============================================================
-- Витрина: mart_product_consumer
-- Описание: Данные о том, какие клиенты (пол, возраст, регион) 
--           покупают тот или иной товар.
-- Источник: core.fact_order_position + core.dim_product + 
--           core.dim_client
-- ============================================================
CREATE OR REPLACE VIEW mart.mart_product_consumer AS
SELECT 
    -- Данные продукта (из dim_product)
    p.product_id,
    p.product_name,
    p.description AS product_description,
    p.category_id AS product_category_id,
    p.category_name AS product_category_name,
    p.sku AS product_sku,
    p.price_value AS product_price_value,
    p.price_currency_code AS product_price_currency_code,
    p.price_currency_name AS product_price_currency_name,
    -- Данные клиента (из dim_client)
    c.client_id,
    c.name AS client_name,
    c.birthdate AS client_birthdate,
    date_part('year', age(c.birthdate)) as client_age,
    c.gender AS client_gender,
    c.phone_number AS client_phone_number,
    c.email AS client_email,
    c.registration_dttm AS client_registration_dttm,
    c.address_country AS client_address_country,
    c.address_region AS client_address_region,
    c.address_city AS client_address_city,
    c.address_street AS client_address_street,
    c.address_house AS client_address_house,
    c.address_postal_code AS client_address_postal_code
FROM core.fact_order_position fop
-- Присоединяем продукт (только текущую версию)
JOIN core.dim_product p 
    ON fop.product_sk = p.product_sk 
    AND p.is_current = TRUE
-- Присоединяем клиента (только текущую версию)
JOIN core.dim_client c 
    ON fop.client_sk = c.client_sk 
    AND c.is_current = TRUE
-- Берем только актуальные версии факта (последний статус)
WHERE fop.effective_to_dttm = '9999-12-31 23:59:59+03'::TIMESTAMPTZ;

COMMENT ON VIEW mart.mart_product_consumer IS 
'Данные о спросе - какие клиенты покупают какие товары с агрегацией';
COMMENT ON COLUMN mart.mart_product_consumer.product_id IS 'ID продукта';
COMMENT ON COLUMN mart.mart_product_consumer.product_name IS 'Наименование продукта';
COMMENT ON COLUMN mart.mart_product_consumer.client_id IS 'ID клиента';
COMMENT ON COLUMN mart.mart_product_consumer.client_name IS 'ФИО клиента';
