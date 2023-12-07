import requests

def get_summoner_val_data(api_key, summoner_name, region):
    tft_url = f'https://{region}.api.riotgames.com/val/summoner/v4/summoners/by-name/{summoner_name}'
    headers = {'X-Riot-Token': api_key}

    response = requests.get(tft_url, headers=headers)

    if response.status_code == 200:
        summoner_data = response.json()
        return summoner_data
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
