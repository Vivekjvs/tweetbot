import requests
import tweepy
import time
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

CONSUMER_KEY = 'HcLnk3t9qeY9Bp0hEbImiyCj0'
CONSUMER_SECRET = '3yP4BpQ3kuIQzaYDwgUngHBEob8wUC0OqixoRaGBSXbzNBAEu9'
ACCESS_KEY = '1241626753333788673-JDkvFV3HimT3nodtsk1DnJKNU6uxP0'
ACCESS_SECRET = 'dJQbRfQtoueBZDjK5F0Tcwp4iUAA3EKjmp9WERG5J2XKG'

def re_tweet():
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
    api = tweepy.API(auth)


    FILE_NAME = '/home/vivek/Desktop/git/tweetbot/last_seen_id.txt'

    def retrieve_last_seen_id(file_name):
        f_read = open(file_name,'r')
        last_seen_id = int(f_read.read().strip())
        f_read.close()
        return last_seen_id

    def store_last_seen_id(last_seen_id,file_name):
        f_write = open(file_name,'w')
        f_write.write(str(last_seen_id))
        f_write.close()
        return
        
    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    mentions = api.mentions_timeline(last_seen_id,tweet_mode='extended')

    for mention in reversed(mentions):
        text = mention.full_text
        index = Zalgorithm.match(text) + 12
        place_name = text[index:]
        print(str(mention.id) + '-' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id,FILE_NAME)
        print("Responding")
        weather = geo_location(place_name)

        api.update_status('@'+ mention.user.screen_name + ' ' +'temperature '+ str(weather['temperature'])+'\n'+str(weather['location']) , mention.id     )



while True:
    time.sleep(15)
    re_tweet()