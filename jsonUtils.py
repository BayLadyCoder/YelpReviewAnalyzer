import json
import os


def dictToJSOND3(dict):
    with open('./static/bubble.json', 'w') as file:
        json.dump(dict, file)

def dictToJSONdata(dict):
    with open(dict['fileName'] + '.json', 'w') as file:
        json.dump(dict['data'], file)

def JSONtoDict(fileName):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, fileName + ".json")
    return json.load(open(json_url))

