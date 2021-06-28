from flask import Flask, render_template
from cachetools import cached, TTLCache

import pandas as pd
import requests
import os

app = Flask(__name__)
cache = TTLCache(maxsize=100, ttl=60)

@cached(cache)
def create_access_token(client_id, client_secret):
    data = { 'grant_type': 'client_credentials' }
    response = requests.post('https://us.battle.net/oauth/token',
                             data=data,
                             auth=(client_id, client_secret))
    return response.json()['access_token']

def make_requests(endpoint):
    access_token = create_access_token(
        os.environ['client_id'],
        os.environ['client_secret'])
    headers = {"Authorization": "Bearer {}".format(access_token)}

    response = requests.get(
        endpoint,
        headers=headers
    ).json()

    return response

@cached(cache)
def get_cards(card_class):
    url =  'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&class={}&manaCost=[7,8,9,10]' \
               '&rarity=legendary&pageSize=10&sort=id:asc'.format(card_class)

    return make_requests(url)

@cached(cache)
def get_individual_metadata(type):
    url = 'https://us.api.blizzard.com/hearthstone/metadata/{}?locale=en_US'.format(type)

    metadata = make_requests(url)
    data = {}

    for each_type in metadata:
        data[each_type['id']] = each_type['name']

    return data

@app.route('/')
def hello_world():
    return 'Hello!!'

@app.route('/<card_name>')
def generate_display_data(card_name):
    try:
        data = get_cards(card_name)['cards']
        sets = get_individual_metadata('sets')
        classes = get_individual_metadata('classes')
        types = get_individual_metadata('types')
        rarity = get_individual_metadata('rarities')

        table = []

        for each in data:
            temp = {i: each[i] for i in ('id', 'image', 'name')}
            temp.update({'Type': types.get(each['cardTypeId']), 'Rarity': rarity.get(each['rarityId']),
                         'Set': sets.get(each['cardSetId']), 'Class': classes.get(each['classId'])})
            table.append(temp)

        df= pd.DataFrame(table)
        return render_template('card_info.html',
                               tables=[df.to_html(classes='data', index=False)],
                               header="true"
                               )
    except KeyError as e:
        return 'Invalid Auth. Please check your Client ID and secret'

if __name__ == '__main__':

    app.run(host='0.0.0.0')
