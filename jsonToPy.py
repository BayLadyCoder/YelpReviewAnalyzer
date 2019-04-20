import json

with open('api/orders.json') as f:
    orders = json.load(f)

# for order in orders:
#     print(order)
#     print(order['name'])
