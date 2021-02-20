'''
A module for parsing an json object (file) obtained using the Twitter API (or some other).

Contains a function to provide access to various parts of the json object.
For example, ask the user to enter the dictionary key whose meaning he wants to view.
'''


import json
from typing import List, Dict, Union

def get_file_name() -> Union[List, Dict]:
    '''
    Gets file name from user
    '''

    file_name = input('What is your file name?\n').rstrip()
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)
        return data
    except FileNotFoundError:
        return 'There is no such file in your current working directory'


def redirect(data):
    '''
    Provide access to various parts of the json object. Is used to navigate file from up to down
    '''

    # want_back = input('Do you want to go back? If so, \
# write "b" as many times as you want to go back.\n\
    # Otherwise, press Enter')

    if isinstance(data, dict):
        value_to_redirect = input(f'Specify one of keys: {list(data.keys())}\n').strip()
    # this work with assumption that then all the list will comtain objects

    elif isinstance(data, list) and all([isinstance(elm, dict) for elm in data]):
        value_to_redirect = ''
        # here we assume that json lists contains objects that are the same
        object_keys = f'On this step there is a list of objects in yout json file, \
please specify what category you need to identify what onbject is interesting for \
you\nere is an example of what the object contains: {list(data[0].keys())}'
        print(object_keys)
        value_to_identify = input().strip()
        print(f'We get this category: {value_to_identify}. Please wait.\n')
        print([obj[value_to_identify] for obj in data])
        value = input().strip('\' ')
        for obj in data:
            if obj[value_to_identify] == value:
                value_to_redirect = data.index(obj)
                break
        if not isinstance(value_to_redirect, int):
            print('You specified wrong value')
            value_to_redirect = False

    elif isinstance(data, list) and all([not isinstance(elm, dict) for elm in data]):
        print(f'Here goes your list of values: {data}\n')
        value_to_redirect = False
    # TODO: list with dicts and not dicts

    else:
        print(f'Here is your data: {data}\n')
        print('You reached the bottom of your file\n')
        value_to_redirect = False

    return value_to_redirect


if __name__ == "__main__":
    json_file = get_file_name()
    if json_file:
        json_navigator = json_file
        # path = []
        while True:
            redirect_value = redirect(data)
            # path.append(redirect_value)
            if isinstance(redirect_value, bool):
                break
            json_navigator = json_navigator[redirect_value]

        # print(path)
