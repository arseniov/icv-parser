import requests
from urllib.parse import quote

def check_seeders_and_leechers(magnet_link):
    # URL-encode the magnet link
    encoded_magnet_link = quote(magnet_link, safe='')

    api_url = f"https://checker.openwebtorrent.com/check?magnet={encoded_magnet_link}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        # Extract only the first numerical values for Seeders and Leechers
        seeds = data.get("seeds", 0)
        peers = data.get("peers", 0)

        return seeds, peers
    else:
        return None
