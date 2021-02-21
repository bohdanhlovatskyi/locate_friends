import requests
import urllib
import folium
import json
import tweepy
from folium.plugins import MarkerCluster
from typing import Dict, List, Tuple


def get_friends_list(user_screen_name: str, bearer_token: str):
    '''
    '''

    BASE_URL = "https://api.twitter.com/"
    URL = f'{BASE_URL}1.1/friends/list.json'
    search_headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    search_params = {
        'screen_name': f'@{user_screen_name}',
        'count': 50
    }

    response = requests.get(URL,
                            headers=search_headers,
                            params=search_params)

    return response.json()

def get_location(adress: str, adresses: Dict[str, Tuple[str]]={}) -> List[str]:
    '''
    Gets location of specific adress (city, state) from openstreetmap
    '''

    try:
        return adresses[adress]
    except KeyError:
        url = 'https://nominatim.openstreetmap.org/search/' + \
                urllib.parse.quote(adress) +'?format=json'
        response = requests.get(url).json()
        try:
            coords = response[0]["lat"], response[0]["lon"]
        except IndexError:
            adresses[adress] = None
            return None

        adresses[adress] = coords

    return adresses[adress]

def get_friends_locations(user_screen_name, bearer_token) -> str:
    '''
    Gets user name from twitter, returns name of file with created html map.
    '''

    data = get_friends_list(user_screen_name, bearer_token)
    try:
        info_on_users = [(user['name'], user['location']) for user in data['users']]
    except KeyError:
        return None
    points_to_put_on_map = [(name, get_location(address)) for name, address in info_on_users]
    points_to_put_on_map = [(name, tuple(map(float, coordinates))) for name, coordinates in points_to_put_on_map if coordinates]

    locations_map = folium.Map(tiles='stamenterrain')
    friends = MarkerCluster()
    for name, coordinates in points_to_put_on_map:
        folium.Marker(coordinates, popup=name, icon=folium.Icon(color='red')).add_to(friends)
    friends.add_to(locations_map)

    return locations_map # folium Map instance
