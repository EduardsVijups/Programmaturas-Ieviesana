import requests
import json

def get_api_response():
    url = "https://api.atvertiedati.lv/v1/prices/fuel/latest?fuel_type=e95"
    headers = {
        'X-Api-Key': 'ad_live_9929adb1_Zt_t64Lh8Z9TCZMRhxNQ3Utwx892h57qRp4JZCtEBtI'
    }


    response = requests.get(url, headers=headers)
    
    data = response.json()


    for item in data['data']['fuel_types']['e95']:
        print(f" Station: {item['station']}, Price: {item['price']}, Date: {item['price_date']}")


def get_api_response_from_file():
    with open('data.json', 'r') as file:
        data = json.load(file)

    for item in data['data']['fuel_types']['e95']:
        print(f" Station: {item['station']}, Price: {item['price']}, Date: {item['price_date']}")


get_api_response_from_file()