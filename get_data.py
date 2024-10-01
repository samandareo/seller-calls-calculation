import requests
import json
import datetime

url = 'https://company.amocrm.ru/api/v4/' # Replace company with your real amocrm name

headers = {
    'Authorization': 'Bearer token' # Replace auth token
}
today = datetime.datetime.now().date()
from_time = datetime.datetime.combine(today, datetime.time.min)
to_time = datetime.datetime.combine(today, datetime.time(hour=20))

params = {
    'filter[note_type]' : 'call_out',
    'filter[updated_at][from]' : int(from_time.timestamp()),
    # 'filter[updated_at][to]' : int(to_time.timestamp()),
    'limit': 250
}

seller_name = {
    'id': 1111,
    'name': '',
    'calls' : 0,
    'bound' : 0,
    'unbound' : 0
}


def make_request(url, url_method, params,headers):
    response = requests.get(url + url_method, headers=headers, params=params)
    return response

def reset_info():
    seller_name['calls'] = 0

def calculate_calls(seller_1, data):
    reset_info()
    for entity in data['_embedded']['notes']:
        if entity['responsible_user_id'] == seller_1['id']:
            seller_1['calls'] += 1
            if entity['params'].get('duration', 0) == 0:
                seller_1['unbound'] += 1
            else:
                seller_1['bound'] += 1

def result():
    sellers = []

    # If you have a lot of seller, you sort them with calls count or something

    result = f'{sellers[0]["name"]}\n📞: {sellers[0]["calls"]}\n✅: {sellers[0]["bound"]}\n🚫: {sellers[0]["unbound"]}\n\n{sellers[1]["name"]}\n📞: {sellers[1]["calls"]}\n✅: {sellers[1]["bound"]}\n🚫: {sellers[1]["unbound"]}\n\n{sellers[2]["name"]}\n📞: {sellers[2]["calls"]}\n✅: {sellers[2]["bound"]}\n🚫: {sellers[2]["unbound"]}\n\n'

    return result


def main():
    response = make_request(url, 'leads/notes', params, headers)

    if response.status_code == 200:
        data = response.json()
        calculate_calls(seller_name, data)
        print(result())
    elif response.status_code == 204:
        reset_info()
        print('No content')
        print('Error', response.status_code, response.text)
