import requests

API_KEY = '8013b162-6b42-4997-9691-77b7074026e0'
SERVER_ADDRESS = "https://geocode-maps.yandex.ru/1.x/"


def geocode(address):
    params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"
    }
    response = requests.get(SERVER_ADDRESS, params=params)
    response.raise_for_status()
    return response.json()


def get_ll_span(address):
    json_data = geocode(address)
    envelope = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"]["Envelope"]

    lower_corner = list(map(float, envelope["lowerCorner"].split()))
    upper_corner = list(map(float, envelope["upperCorner"].split()))

    lon = (lower_corner[0] + upper_corner[0]) / 2
    lat = (lower_corner[1] + upper_corner[1]) / 2

    lon_span = upper_corner[0] - lower_corner[0]
    lat_span = upper_corner[1] - lower_corner[1]

    return f"{lon},{lat}", f"{lon_span},{lat_span}"
