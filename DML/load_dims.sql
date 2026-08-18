INSERT INTO core.dim_client (
    client_id,
    name,
    birthdate,
    gender,
    phone_number,
    email,
    registration_dttm,
    address_country,
    address_region,
    address_city,
    address_street,
    address_house,
    address_postal_code,
    src_system,
    effective_from_dttm,
    effective_to_dttm,
    "version",
    is_current
)
SELECT 
    client_id
    , "name" 
    , birthdate 
    , gender 
    , phone_number 
    , email 
    , registration_dttm 
    , address_country 
    , address_region 
    , address_city 
    , address_street 
    , address_house 
    , address_postal_code 
    , src_system 
    , load_dttm as effective_from_dttm 
    , coalesce(lead(load_dttm) over (partition by client_id order by load_dttm asc), '9999-12-31 23:59:59'::timestamptz) as effective_to_dttm 
    , 1 as "version"
    , lead(load_dttm) over (partition by client_id order by load_dttm asc) is null as is_current 
FROM raw.raw_client
where 1=1
	and src_system = 'client_service';

INSERT INTO core.dim_currency (
    currency_code 
    , currency_name 
    , src_system 
)
SELECT 
    currency_code 
    , currency_name 
    , src_system 
FROM raw.raw_currency;

INSERT INTO core.dim_pick_up_point (
    point_id 
    , open_date 
    , address_country 
    , address_region 
    , address_city 
    , address_street 
    , address_house 
    , address_postal_code 
    , src_system 
    , effective_from_dttm 
    , effective_to_dttm 
    , is_current 
)
SELECT 
    point_id 
    , open_date 
    , address_country 
    , address_region 
    , address_city 
    , address_street 
    , address_house 
    , address_postal_code 
    , src_system 
    , load_dttm as effective_from_dttm 
    , coalesce(lead(load_dttm) over (partition by point_id order by load_dttm asc), '9999-12-31 23:59:59'::timestamptz) as effective_to_dttm 
    , lead(load_dttm) over (partition by point_id order by load_dttm asc) is null as is_current 
FROM raw.raw_pick_up_point;

INSERT INTO core.dim_product (
    product_id 
    , product_name 
    , description 
    , category_id 
    , category_name 
    , weight_kg 
    , product_length 
    , product_width 
    , product_height 
    , sku 
    , price_value 
    , price_currency_code 
    , price_currency_name 
    , src_system 
    , effective_from_dttm 
    , effective_to_dttm 
    , "version" 
    , is_current 
)
SELECT 
    p.product_id 
    , p.product_name 
    , p.description 
    , p.category_id 
    , c.category_name 
    , p.weight_kg 
    , p.product_length 
    , p.product_width 
    , p.product_height 
    , p.sku 
    , p.price_value 
    , p.price_currency as price_currency_code 
    , cur.currency_name as price_currency_name  
    , p.src_system 
    , p.load_dttm as effective_from_dttm 
    , coalesce(lead(p.load_dttm) over (partition by p.product_id order by p.load_dttm asc), '9999-12-31 23:59:59'::timestamptz) as effective_to_dttm 
    , 1 as version
    , lead(p.load_dttm) over (partition by p.product_id order by p.load_dttm asc) is null as is_current 
FROM raw.raw_product as p
join raw.raw_category as c
on 1=1
	and p.category_id = c.category_id
join raw.raw_currency cur 
on 1=1
	and p.price_currency = cur.currency_code
where 1=1
	and p.src_system = 'product_service';
