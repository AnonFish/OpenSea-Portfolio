import streamlit as st
import requests, json
from web3 import Web3
import pandas as pd
import cryptocompare

portfolioValue = 0.0

st.sidebar.header("Endpoints")
endpoint_choices = ['Assets', 'Portfolio']
endpoint = st.sidebar.selectbox("Choose an Endpoint", endpoint_choices)

st.title(f"OpenSea Tool - {endpoint}")


def render_asset(asset):
    if asset['name'] is not None:
        st.subheader(asset['name'])
    else:
        st.subheader(f"{asset['collection']['name']} #{asset['token_id']}")

    if asset['description'] is not None:
        st.write(asset['description'])
    else:
        st.write(asset['collection']['description'])

    if asset['image_url'].endswith('mp4') or asset['image_url'].endswith('mov'):
        st.video(asset['image_url'])
    elif asset['image_url'].endswith('svg'):
        svg = requests.get(asset['image_url']).content.decode()
        st.image(svg)
    elif asset['image_url']:
        st.image(asset['image_url'])


if endpoint == 'Assets':

    try:

        st.sidebar.header('Filters')
        owner = st.sidebar.text_input("Owner")
        collection = st.sidebar.text_input("Collection")
        params = {'owner': owner}
        if collection:
            params['collection'] = collection

        r = requests.get('https://api.opensea.io/api/v1/assets', params=params)

        assets = r.json()['assets']
        for asset in assets:
            render_asset(asset)

        st.subheader("Raw JSON Data")
        st.write(r.json())

    except:

        st.write("Enter OpenSea Address!")

if endpoint == 'Portfolio':

    try:
        st.sidebar.header('Filters')
        portfolio = st.sidebar.text_input("OpenSea Address")

        params = {'asset_owner': portfolio}
        r = requests.get('https://api.opensea.io/api/v1/collections', params=params)
        rNew = {'collections': r.json()}

        collections = rNew['collections']

        st.subheader("Valuation")

        for collection in collections:
            Name = (collection["primary_asset_contracts"][0]["name"])
            Floor = (collection["stats"]["floor_price"])
            Owned = (collection["owned_asset_count"])
            totalValue = float(Floor) * float(Owned)
            st.write(Name)
            st.write("Floor: ", Floor, "Owned:", Owned, "Total Value:", totalValue, "ETH")
            portfolioValue = float(portfolioValue + totalValue)

        st.subheader("Portfolio Value")

        btc = (cryptocompare.get_price('ETH', currency='USD'))
        btcPrice = float(btc["ETH"]["USD"])

        st.write("Total Value", round(portfolioValue, 2), "ETH")
        st.write("USD Value", round((portfolioValue * btcPrice), 2), "USD")

    except:

        st.write("Enter OpenSea Address!")
