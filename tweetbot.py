import requests
import tweepy
import json
import Zalgorithm

t = {
    'units': 'si', 
    'exclude': ['minutely', 'hourly', 'daily', 'alerts']
}
l = {
    'access_token':'pk.eyJ1Ijoic2F0dmlrNzg5IiwiYSI6ImNrMzl0emJjbzAyMHozbWxkcHI4bzlrcW4ifQ.yBkLL6eRbv0hBa1LWv89gw'
}

def geo_location(location): 
    map_api = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json"
    response = requests.get(map_api, headers={'Accept': 'application/json'},params=l)
    try:
        data = response.json()
        place = data['features'][0]['place_name']
        [longitude,latitude] = data['features'][0]['center']
    except:
        return {'err_message': 'Unknown'}
    else:
        url = f"https://api.darksky.net/forecast/a52d1bcabf62cdc867362eda5c803439/{latitude},{longitude}"
        res = requests.get(url, headers={'Accept': 'application/json'},params=t)
        return {'temperature':res.json()['currently']['temperature'],'location':place}

CONSUMER_KEY = 'txre1Rwayk5oiiMoFDHVxKUDH'
CONSUMER_SECRET = '8ZVq46XkuxghebOvhEX9yrul69s8JdjEp7uqbxP6GsbhJfKTq4'
ACCESS_KEY = '1241626753333788673-BrinIszBpzqRb2l9MQdvZ4TVTxuQlb'
ACCESS_SECRET = '1CY2RBO3ZowkpQNQg7RomwJ6E2Xjq3vhlc6HKPG4Q61cT'

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api = tweepy.API(auth)

res = api.search(q='viveks_dev', since_id='1241771148032880640')
with open('data.json') as file:
    data = json.load(file)
for i in res:
    obj = i._json
    reply_id= obj["in_reply_to_status_id_str"]
    if reply_id == "1241771148032880640"and not(obj['id_str'] in data['saved_id']):
        try:
            data['saved_id'].append(obj['id_str'])
            text = obj['text']
            index = Zalgorithm.matching(text,'location')[0] + 8
            weather = get_temperature(text[index:])
            tweet = f"@{obj['user']['screen_name']} temperature {str(weather['temperature'])}"+ '\n' +weather['location']
            print(tweet)
            # api.update_status(tweet)
        except:
            print('err')
        else:
            with open('data.json','w') as file:
                json.dump(data,file)

