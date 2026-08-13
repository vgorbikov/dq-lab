from services.product_service import ProductService

ps = ProductService()
product = ps.new_product()
print(ps.stocks)

ps.new_supply(items=[(product, 3)])
print(ps.stocks)

ps.new_shipment(items=[(product, 2)])
print(ps.stocks)
