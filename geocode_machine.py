from urllib import parse
import requests
import json
import streamlit as st


st.set_page_config(layout="wide")
GEOCODER_KEY = st.secrets["Geocoder_Key"]


def get_google_geocoder_response(address: str):
    parsed_address = parse.quote_plus(address)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={parsed_address}&key={GEOCODER_KEY}"
    payload = {}
    files = {}
    headers = {
        'Content-Type': 'application/json',
        'Accept-Language': 'en/en'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload, files=files)
        if json.loads(response.text)["status"] != "OK":
            coordinates = "Empty geocoder response"
            precision = "Empty geocoder response"
            formatted_address = "Empty geocoder response"
        else:
            suggested_coordinates = json.loads(response.text)["results"]
            found_points = len(suggested_coordinates)
            coordinates = str(found_points) + " found points" + "\n"
            precision = ""
            formatted_address = ""
            for coordinate in suggested_coordinates:
                lat = coordinate["geometry"]["location"]["lat"]
                lon = coordinate["geometry"]["location"]["lng"]
                precision = precision + coordinate["geometry"]["location_type"] + "\n"
                coordinates = coordinates + str(lat) + "," + str(lon) + "\n"
                formatted_address = formatted_address + coordinate["formatted_address"] + "\n"
        st.code(coordinates)
        st.code(precision)
        st.code(formatted_address)
        st.code(response.text)
    except:
        coordinates = "Got an error, skipped"
        precision = "Got an error, skipped"
        formatted_address = "Got an error, skipped"
        st.code(coordinates)
        st.code(precision)
        st.code(formatted_address)
        st.code("An error occured")
    return


address = st.text_input("Address", value="", max_chars=None, key=None, type="default")
if st.button("Geocode address", type="primary"):
    get_google_geocoder_response(address)
