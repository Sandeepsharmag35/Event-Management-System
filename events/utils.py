import json
import os

FILE_PATH = 'events/data.json'

def read_json():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, 'r') as file:
        return json.load(file)
    
def write_json(data):
    with open(FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)