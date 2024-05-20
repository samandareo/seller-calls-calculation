import requests
import json
import datetime

url = 'https://thewolfsoft.amocrm.ru/api/v4/'

headers = {
    # 5 yillik token, 2029 alishtirish kere
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjZjNTFlNDMwODhiMTQ3NjUxYjY5ZDEyOWJiNmRjMTEyNTMyZDBlNjg4NzkyZTI4MDFkMWIyZWE5ZWQ3ZGUxYjExYWIwODRhZWU1ZmFjMDQzIn0.eyJhdWQiOiI4NjRhNWUyMC02ODJiLTRhMDItYTI4Zi02MDdjMDY1YjU3ZGQiLCJqdGkiOiI2YzUxZTQzMDg4YjE0NzY1MWI2OWQxMjliYjZkYzExMjUzMmQwZTY4ODc5MmUyODAxZDFiMmVhOWVkN2RlMWIxMWFiMDg0YWVlNWZhYzA0MyIsImlhdCI6MTcxNTE2MDQwOCwibmJmIjoxNzE1MTYwNDA4LCJleHAiOjE4NzI4OTI4MDAsInN1YiI6Ijg0ODI4NjEiLCJncmFudF90eXBlIjoiIiwiYWNjb3VudF9pZCI6MzAzNTExNTcsImJhc2VfZG9tYWluIjoiYW1vY3JtLnJ1IiwidmVyc2lvbiI6Miwic2NvcGVzIjpbImNybSIsImZpbGVzIiwiZmlsZXNfZGVsZXRlIiwibm90aWZpY2F0aW9ucyIsInB1c2hfbm90aWZpY2F0aW9ucyJdLCJoYXNoX3V1aWQiOiJjNWMyOWJmNy0wN2EzLTQwNDgtOTliMC1lZTU2Y2QxNmJhOWEifQ.g625yoGoOgeftIJr82pzlV3D0qdfxruuJg65auwRqPbJGupIhDjkV42JjHIW6UxOWOFn0osupFERbEN3wa3IY9aIAWHUqG19vLCDftLF4ZlBcydKxvU8c3jxam8PJR_NhSdyDqWkKYZltYtZo2Q-owbphqeiyB8GZnTVHOfy9VcWfIBpcuu9HBW6LKmMRousPIS8Gv1FgFI0rHBCV-sTfuh-4Pg4CQuBlfQ2KlQZQxLakL-NrnLPFhJrvjtDlXf59-ICKXXoYNWGPnzIHN_mn9DWI1yAJOlQVV-ts-xyGARUD-MH1Jw5kNM5lE3WkXViY3lZPpcJn9_S7QUEpN9uQg'
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

seller_asal = {
    'id': 10936086,
    'name': 'Asal',
    'calls' : 0,
    'bound' : 0,
    'unbound' : 0
}

seller_dilshoda = {
    'id': 11028838,
    'name': 'Dilshoda',
    'calls' : 0,
    'bound' : 0,
    'unbound' : 0
}

seller_azizxon = {
    'id': 9562898,
    'name': 'Azizxon',
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
    seller_dilshoda['calls'] = 0
    seller_dilshoda['bound'] = 0
    seller_dilshoda['unbound'] = 0
    seller_azizxon['calls'] = 0
    seller_azizxon['bound'] = 0
    seller_azizxon['unbound'] = 0

def calculate_calls(seller_1, seller_2, seller_3, data):
    reset_info()
    for entity in data['_embedded']['notes']:
        if entity['responsible_user_id'] == seller_1['id']:
            seller_1['calls'] += 1
            if entity['params'].get('duration', 0) == 0:
                seller_1['unbound'] += 1
            else:
                seller_1['bound'] += 1
        elif entity['responsible_user_id'] == seller_2['id']:
            seller_2['calls'] += 1
            if entity['params'].get('duration', 0) == 0:
                seller_2['unbound'] += 1
            else:
                seller_2['bound'] += 1
        elif entity['responsible_user_id'] == seller_3['id']:
            seller_3['calls'] += 1
            if entity['params'].get('duration', 0) == 0:
                seller_3['unbound'] += 1
            else:
                seller_3['bound'] += 1

def result():
    sellers = []

    if seller_asal['calls'] > seller_azizxon['calls'] and seller_asal['calls'] > seller_dilshoda['calls']:
        sellers.append(seller_asal)
        if seller_azizxon['calls'] > seller_dilshoda['calls']:
            sellers.append(seller_azizxon)
            sellers.append(seller_dilshoda)
        else:
            sellers.append(seller_dilshoda)
            sellers.append(seller_azizxon)
    elif seller_azizxon['calls'] > seller_asal['calls'] and seller_azizxon['calls'] > seller_dilshoda['calls']:
        sellers.append(seller_azizxon)
        if seller_asal['calls'] > seller_dilshoda['calls']:
            sellers.append(seller_asal)
            sellers.append(seller_dilshoda)
        else:
            sellers.append(seller_dilshoda)
            sellers.append(seller_asal)
    else:
        sellers.append(seller_dilshoda)
        if seller_asal['calls'] > seller_azizxon['calls']:
            sellers.append(seller_asal)
            sellers.append(seller_azizxon)
        else:
            sellers.append(seller_azizxon)
            sellers.append(seller_asal)

    result = f'{sellers[0]["name"]}\n📞: {sellers[0]["calls"]}\n✅: {sellers[0]["bound"]}\n🚫: {sellers[0]["unbound"]}\n\n{sellers[1]["name"]}\n📞: {sellers[1]["calls"]}\n✅: {sellers[1]["bound"]}\n🚫: {sellers[1]["unbound"]}\n\n{sellers[2]["name"]}\n📞: {sellers[2]["calls"]}\n✅: {sellers[2]["bound"]}\n🚫: {sellers[2]["unbound"]}\n\n'

    return result


def main():
    response = make_request(url, 'leads/notes', params, headers)

    if response.status_code == 200:
        data = response.json()
        calculate_calls(seller_asal, seller_dilshoda, seller_azizxon, data)
        print(result())
    elif response.status_code == 204:
        reset_info()
        print('No content')
        print('Error', response.status_code, response.text)
