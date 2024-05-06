import requests
import json
import datetime

url = 'https://thewolfsoft.amocrm.ru/api/v4/'

headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjQwNzRkZmE4NGMyYzczNTViMWY0MTIyMTAxOTZlOTYzMzY0YTZjNjA4NTA4MjU3NDI0MDI0MThiM2I4N2FhMWE5NjY5OTNiNjA0MDIxODhkIn0.eyJhdWQiOiI4NjRhNWUyMC02ODJiLTRhMDItYTI4Zi02MDdjMDY1YjU3ZGQiLCJqdGkiOiI0MDc0ZGZhODRjMmM3MzU1YjFmNDEyMjEwMTk2ZTk2MzM2NGE2YzYwODUwODI1NzQyNDAyNDE4YjNiODdhYTFhOTY2OTkzYjYwNDAyMTg4ZCIsImlhdCI6MTcxNDk3NzMzNCwibmJmIjoxNzE0OTc3MzM0LCJleHAiOjE3MTUwNjM3MzQsInN1YiI6Ijg0ODI4NjEiLCJncmFudF90eXBlIjoiIiwiYWNjb3VudF9pZCI6MzAzNTExNTcsImJhc2VfZG9tYWluIjoiYW1vY3JtLnJ1IiwidmVyc2lvbiI6Miwic2NvcGVzIjpbInB1c2hfbm90aWZpY2F0aW9ucyIsImZpbGVzIiwiY3JtIiwiZmlsZXNfZGVsZXRlIiwibm90aWZpY2F0aW9ucyJdLCJoYXNoX3V1aWQiOiIwY2E3OGIyNi1jM2JjLTQyOGUtYTA2MS05NTgxM2JmMjdhODIifQ.bdL8ELubGgLzPtAFymUz3SWQuR1PwhBawdpTsDEt26PC4zQ5Z9JekPA-yUxSFpc0V_jrAf3w84iqPfuV1y6Cb6CiKa3-LKuSM39Vwh8UulxPBAQZg4_fgHWXuopXEMnubhA7mRMXbQNVDi9pblFZVGR63gkfnAJItn52QbePfPuwzx12pZtLhX7UuaQoH0OCgz_FDKKd2omgY6p13koqSg1rM7W94oJ7Bt_c1uVcrR7rPhWnOLxDKUExo1H5F-XfeThzncVZQV6dxSa2RwPrmPohtgx0ATD-9qGE0nP0Ws70bGjeLoHQM4dyCJcSpFo5fDx7l8iyfsH2c1Hy69zGzg'
}
today = datetime.datetime.now().date()
from_time = datetime.datetime.combine(today, datetime.time.min)
to_time = datetime.datetime.combine(today, datetime.time(hour=20))

params = {
    'filter[note_type]' : 'call_out',
    'filter[updated_at][from]' : int(from_time.timestamp()),
    'filter[updated_at][to]' : int(to_time.timestamp()),
    'limit': 250
}

seller_asal = {
    'id': 10936086,
    'name': 'Asal',
    'calls' : 0,
    'bound' : 0,
    'unbound' : 0
}

seller_mukhammadali = {
    'id': 10940038,
    'name': 'Muhammad Ali',
    'calls' : 0,
    'bound' : 0,
    'unbound' : 0
}

def make_request(url, url_method, params,headers):
    response = requests.get(url + url_method, headers=headers, params=params)
    return response

def reset_info():
    seller_asal['calls'] = 0
    seller_asal['bound'] = 0
    seller_asal['unbound'] = 0
    seller_mukhammadali['calls'] = 0
    seller_mukhammadali['bound'] = 0
    seller_mukhammadali['unbound'] = 0

def calculate_calls(seller_1, seller_2, data):
    reset_info()
    for entity in data['_embedded']['notes']:
        if entity['responsible_user_id'] == seller_1['id']:
            seller_1['calls'] += 1
            if entity['params'].get('duration', 0) > 0:
                seller_1['bound'] += 1
            elif entity['params'].get('duration', 0) == 0:
                seller_1['unbound'] += 1
        elif entity['responsible_user_id'] == seller_2['id']:
            seller_2['calls'] += 1
            if entity['params'].get('duration', 0) > 0:
                seller_2['bound'] += 1
            elif entity['params'].get('duration', 0) == 0:
                seller_2['unbound'] += 1

def result(seller_1, seller_2):
    return (f'<b>{seller_1["name"]}</b>:\n📞: {seller_1["calls"]}\n✅: {seller_1["bound"]}\n🚫: {seller_1["unbound"]}\n\n<b>{seller_2["name"]}</b>:\n📞: {seller_2["calls"]}\n✅: {seller_2["bound"]}\n🚫: {seller_2["unbound"]}')



def main():
    response = make_request(url, 'leads/notes', params, headers)
    if response.status_code == 200:
        data = response.json()
        calculate_calls(seller_asal, seller_mukhammadali, data)

