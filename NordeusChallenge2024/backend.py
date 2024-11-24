from dataclasses import field

import requests
from config import URL

def load_map(data):
    from map import Field
    grid = []
    for line in data.strip().split('\n'):
        row = [Field(int(height)) for height in line.split()]
        grid.append(row)
    return grid

def get_new_map():
    response = requests.get(URL)
    if response.status_code == 200:
        grid = load_map(response.text)
        return grid
    else:
        return None
