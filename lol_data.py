import requests
import json
def get_summoner_lol_data(api_key, summoner_name, region):
    lol_url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    headers = {'X-Riot-Token': api_key}

    response = requests.get(lol_url, headers=headers)

    if response.status_code == 200:
        summoner_data = response.json()
        return summoner_data
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_match_ids(api_key, puuid, region, queue_type=None, start_time=None, end_time=None, count=50):
    region_mappings = {
        'na1': 'americas',
        'br1': 'americas',
        'lan': 'americas',
        'las': 'americas',
        'kr': 'asia',
        'jp': 'asia',
        'eune': 'europe',
        'euw1': 'europe',
        'tr1': 'europe',
        'ru': 'europe',
        'oce': 'sea',
        'ph2': 'sea',
        'sg2': 'sea',
        'th2': 'sea',
        'tw2': 'sea',
        'vn2': 'sea',
    }

    queue_type_mappings = {
        'ranked_solo_duo': 420,
        'ranked_flex': 440,
        'blind_pick': 430,
        'draft_pick': 400,
        'clash': 700
    }

    region = region.lower()
    routing_value = region_mappings.get(region, region)

    # Convert user-friendly queue type to numeric queue ID
    queue_id = queue_type_mappings.get(queue_type.lower())

    if queue_id is None:
        print("Invalid queue type. Please enter a valid queue type: ranked_solo_duo, ranked_flex, blind_pick, draft_pick, clash")
        return None

    matchlist_url = f'https://{routing_value}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
    headers = {'X-Riot-Token': api_key}

    params = {'startTime': start_time, 'endTime': end_time, 'count': count, 'queue': queue_id}

    try:
        response = requests.get(matchlist_url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching match IDs: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Exception during match ID retrieval: {e}")
        return None


def get_match_data(api_key, match_id, region):
    routing_value = get_routing_value(region)

    match_url = f'https://{routing_value}.api.riotgames.com/lol/match/v5/matches/{match_id}'

    headers = {'X-Riot-Token': api_key}

    try:
        response = requests.get(match_url, headers=headers)

        if response.status_code == 200:
            match_data = response.json()
            if 'info' in match_data and 'gameMode' in match_data['info'] and match_data['info']['gameMode'].lower() == 'classic':
                # Extract champion info from the match data and add it to each participant
                for participant in match_data['info']['participants']:
                    champion_id = participant.get('championId')
                    if champion_id:
                        champion_info = {"id": champion_id, "name": participant.get("championName", "Unknown")}
                        participant['championInfo'] = champion_info

                return match_data
            else:
                print(f"Skipping match ID {match_id} as it is not a classic game.")
                return None
        else:
            print(f"Error fetching match data for match ID {match_id}: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Exception during match data retrieval: {e}")
        return None


def calculate_win_percentage_per_role(matches, summoner_puuid):
    # Filter out None values from matches
    valid_matches = [match for match in matches if match is not None]

    # Check if there are valid matches to calculate win percentage
    if valid_matches:
        overall_wins = 0
        overall_matches_with_wins = 0

        role_wins = {role: 0 for role in ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"]}
        role_matches_with_wins = {role: 0 for role in ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"]}

        for match in valid_matches:
            if 'info' in match and 'participants' in match['info']:
                for participant in match['info']['participants']:
                    champion_info = participant.get('championInfo', {})
                    champion_name = champion_info.get('name', 'Unknown')
                    print(f"Champion Name: {champion_name}, Champion ID: {champion_info.get('id')}")
                    if 'individualPosition' in participant:
                        role = participant['individualPosition']
                        # Check if the role is valid
                        if role in role_wins:
                            # Check if the summoner is the participant and if they won
                            if participant['puuid'] == summoner_puuid:
                                overall_matches_with_wins += 1
                                role_matches_with_wins[role] += 1
                                if participant.get('win', False):
                                    overall_wins += 1
                                    role_wins[role] += 1

        overall_win_percentage = (overall_wins / overall_matches_with_wins) * 100 if overall_matches_with_wins > 0 else 0
        print(f"Overall Win Percentage: {overall_win_percentage:.2f}% (Total Matches: {overall_matches_with_wins})")

        win_percentages = {"Overall": {"Win Percentage": overall_win_percentage, "Total Matches": overall_matches_with_wins}}

        for role in ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"]:
            role_win_percentage = (role_wins[role] / role_matches_with_wins[role]) * 100 if role_matches_with_wins[role] > 0 else 0
            print(f"Win Percentage for {role.capitalize()} role: {role_win_percentage:.2f}% (Total Matches: {role_matches_with_wins[role]})")
            win_percentages[role.capitalize()] = {"Win Percentage": role_win_percentage, "Total Matches": role_matches_with_wins[role]}

        return win_percentages
    else:
        print("No valid match data available.")

def get_routing_value(region):
    region_mappings = {
        'na1': 'americas',
        'br1': 'americas',
        'lan': 'americas',
        'las': 'americas',
        'kr': 'asia',
        'jp': 'asia',
        'eune': 'europe',
        'euw1': 'europe',
        'tr1': 'europe',
        'ru': 'europe',
        'oce': 'sea',
        'ph2': 'sea',
        'sg2': 'sea',
        'th2': 'sea',
        'tw2': 'sea',
        'vn2': 'sea',
    }

    return region_mappings.get(region.lower(), region.lower())



def get_item_name(item_id):
    item_data_url = "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/item.json"
    response = requests.get(item_data_url)
    item_data = json.loads(response.text)

    if 'data' in item_data and str(item_id) in item_data['data']:
        return item_data['data'][str(item_id)]['name']
    else:
        return f"Unknown Item {item_id}"