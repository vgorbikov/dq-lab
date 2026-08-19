INSERT INTO core.fact_order_position (
	order_id 
	, client_sk 
	, client_id
	, pick_up_point_sk 
	, pick_up_point_id
	, product_sk 
	, product_id
	, total_price_currency_sk 
	, total_price_currency_code
	, position_quantity 
	, status 
	, track_number 
	, total_price_value 
	, creation_dttm 
	, update_dttm 
	, effective_from_dttm 
	, effective_to_dttm 
	, "version"
)
SELECT 
    ord.order_id 
    , cli.client_sk 
	, cli.client_id
    , poi.point_sk as pick_up_point_sk 
	, poi.point_id as pick_up_point_id
    , prod.product_sk 
	, prod.product_id
    , cur.currency_sk as total_price_currency_sk
	, cur.currency_code as total_price_currency_code
    , op.quantity as position_quantity
    , ord.status 
    , ord.track_number 
    , ord.total_price_value 
    , ord.creation_dttm 
    , ord.update_dttm 
    , ord.load_dttm as effective_from_dttm 
    , coalesce(lead(ord.load_dttm) over (partition by ord.order_id, op.product_id order by ord.load_dttm asc), '9999-12-31 23:59:59'::timestamptz) as effective_to_dttm 
	, 1 as version
FROM raw.raw_order_position op
join raw.raw_order ord 
on 1=1
	and op.order_id = ord.order_id 
	and op.load_dttm = ord.load_dttm
join core.dim_client cli
on 1=1
	and ord.client_id = cli.client_id
	and ord.load_dttm >= cli.effective_from_dttm 
	and ord.load_dttm < cli.effective_to_dttm
join core.dim_pick_up_point poi
on 1=1
	and ord.pick_up_point_id = poi.point_id
	and ord.load_dttm >= poi.effective_from_dttm 
	and ord.load_dttm < poi.effective_to_dttm
join core.dim_product prod 
on 1=1
	and op.product_id = prod.product_id
	and ord.load_dttm >= prod.effective_from_dttm 
	and ord.load_dttm < prod.effective_to_dttm
join core.dim_currency cur 
on 1=1
	and cur.currency_code = ord.total_price_currency;

INSERT INTO core.fact_shipment_position (
	shipment_id
	, product_sk 
	, product_id
	, quantity 
	, shipment_datetime 
	, "version" 
)
SELECT 
    s.shipment_id
	, p.product_sk 
	, p.product_id
	, si.quantity 
	, s.shipment_datetime 
	, 1 as version
FROM raw.raw_shipment s
join raw.raw_shipment_item si
on 1=1
	and s.shipment_id = si.shipment_id 
	and s.load_dttm = si.load_dttm 
join core.dim_product p 
on 1=1
	and p.product_id = si.product_id 
	and s.load_dttm >= p.effective_from_dttm 
	and s.load_dttm  < p.effective_to_dttm;

INSERT INTO core.fact_supply_position (
	supply_id
	, product_sk 
	, product_id
	, quantity 
	, batch_number
	, supply_datetime 
	, "version" 
)
SELECT 
    s.supply_id
	, p.product_sk 
	, p.product_id
	, si.quantity 
	, si.batch_number
	, s.supply_datetime  
	, 1 as version
FROM raw.raw_supply s
join raw.raw_supply_item si
on 1=1
	and s.supply_id = si.supply_id 
	and s.load_dttm = si.load_dttm 
join core.dim_product p 
on 1=1
	and p.product_id = si.product_id 
	and s.load_dttm >= p.effective_from_dttm 
	and s.load_dttm  < p.effective_to_dttm;

INSERT INTO core.fact_stock_snapshot (
	product_sk 
	, product_id
	, snapshot_dttm
	, quantity
	, "version" 
)
SELECT 
    p.product_sk 
	, p.product_id
	, st.load_dttm as snapshot_dttm
	, st.quantity
	, 1 as version
FROM raw.raw_stock st 
join core.dim_product p
on 1=1
	and p.product_id = st.product_id;
