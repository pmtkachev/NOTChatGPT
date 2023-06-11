"""
Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными.
"""
import json


def write_order_to_json(item, quantity, price, buyer, date):
    order_dict = {'item': item,
                  'quantity': quantity,
                  'price': price,
                  'buyer': buyer,
                  'date': date}
    with open('orders.json') as file:
        orders = json.load(file)
        orders['orders'].append(order_dict)

    with open('orders.json', 'w', ) as file:
        json.dump(orders, file, indent=4, ensure_ascii=False)


# write_order_to_json('Notebook', 1, 45000, 'Anonim', '09.06.2023')
# write_order_to_json('Phone', 2, 5000, 'Anonim', '10.06.2023')
# write_order_to_json('Xerox', 1, 15000, 'Anonim', '12.12.2022')
write_order_to_json('Принтер', 1, 15000, 'Аноним', '12.12.2022')
