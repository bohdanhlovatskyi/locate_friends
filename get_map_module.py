import requests
import urllib
import json
import folium
import reverse_geocoder as rg
from typing import Dict, List, Tuple


def get_friends_list(user_screen_name: str, outfile_name: str='result.json'):
    '''
    '''

    with open('secret.txt') as file:
        BEARER_TOKEN = file.readlines()[0]
    BASE_URL = "https://api.twitter.com/"
    URL = f'{BASE_URL}1.1/friends/list.json'
    search_headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }
    search_params = {
        'screen_name': f'{user_screen_name}',
        'count': 50
    }

    response = requests.get(URL,
                            headers=search_headers,
                            params=search_params)
    if response.status_code != 200:
        return f'There is something wrong with authorisation: {response.status_code}'

    with open(outfile_name, 'w') as outfile:
        json.dump(response.text, outfile)

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

def get_friends_locations(path_to_file: str='tw.json') -> str:
    '''
    Gets user name from twitter, returns name of file with created html map.
    '''

    with open(path_to_file) as json_file:
        data = json.load(json_file)

    info_on_users = [(user['name'], user['location']) for user in data['users']]
    points_to_put_on_map = [(elm[0], get_location(elm[1])) for elm in info_on_users]
    points_to_put_on_map = [(point[0], tuple(map(float, point[1]))) for point in points_to_put_on_map if point[1]]

    # TODO: add user location
    locations_map = folium.Map()
    friends = folium.FeatureGroup()
    for name, coordinates in points_to_put_on_map:
        friends.add_child(folium.Marker(coordinates, popup=name, icon=folium.Icon(color='red')))
    friends.add_to(locations_map)

    file_name = 'templates/map.html'
    locations_map.save(file_name)

    return file_name


def main(user_screen_name: str) -> str:
    '''
    Returns file name (location of map)
    '''

    file_name = 'results.json'
    out = get_friends_list(user_screen_name, file_name)
    if out:
        return out

    return get_friends_locations(file_name)
