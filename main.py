import requests
import re 
import time

def determine_faceit_level(faceit_elo):
    if faceit_elo >= 2001:
        return "10"
    elif faceit_elo >= 1851:
        return "9"
    elif faceit_elo >= 1701:
        return "8"
    elif faceit_elo >= 1551:
        return "7"
    elif faceit_elo >= 1401:
        return "6"
    elif faceit_elo >= 1251:
        return "5"
    elif faceit_elo >= 1101:
        return "4"
    elif faceit_elo >= 951:
        return "3"
    elif faceit_elo >= 801:
        return "2"
    elif faceit_elo >= 1:
        return "1"
    else:
        return "Unknown"
    
def steamid_to_64bit(steamid):
    steam64id = 76561197960265728
    id_split = steamid.split(":")
    steam64id += int(id_split[2]) * 2 
    if id_split[1] == "1":
        steam64id += 1
    return steam64id
        
def get_faceit_level(steam_id64, faceit_api_key):
    # Step 1: Use the Faceit API to get the player's Faceit data
    faceit_api_url = f"https://open.faceit.com/data/v4/players?game=csgo&platform=steam&game_player_id={steam_id64}"
    headers = {
        'Authorization': f'Bearer {faceit_api_key}',
    }
    faceit_response = requests.get(faceit_api_url, headers=headers)
    faceit_data = faceit_response.json()

    if 'games' in faceit_data and 'csgo' in faceit_data['games']:
        # Extract the Faceit level from the 'csgo' game data
        csgo_data = faceit_data['games']['csgo']
        faceit_elo = csgo_data.get('faceit_elo', None)
        return faceit_elo
    
    return None
def extract_steam_ids_and_faceit_levels(status_data, faceit_api_key):
    steam_id_pattern = re.compile(r'"(.+?)"\s+STEAM_([0-1]):([0-1]):(\d+)')
    matches = steam_id_pattern.findall(status_data)

    results = []

    for match in matches:
        name, universe, auth_server, account_id = match
        steam_id = f"STEAM_{universe}:{auth_server}:{account_id}"
        steam_id64 = steamid_to_64bit(steam_id)

        # Throttle requests to the Faceit API to avoid rate limiting
        throttle_requests(100)

        faceit_elo = get_faceit_level(steam_id64, faceit_api_key)

        if faceit_elo is not None:
            faceit_level = determine_faceit_level(faceit_elo)
            results.append((name, faceit_level))
        else:
            results.append((name, "Unknown"))

    return results
def throttle_requests(requests_per_second):
    delay = 1 / requests_per_second
    time.sleep(delay)

status_output = """
# userid name uniqueid connected ping loss state rate
# 3 2 "n1ko" STEAM_1:0:608717496 11:25 92 0 active 786432
# 15 3 "KALIBR" STEAM_1:0:454318149 10:35 62 0 active 786432
# 6 5 "Cool" STEAM_1:0:7673035 11:25 108 0 active 786432
# 7 6 "DRAGUS ∰" STEAM_1:1:592973170 11:25 111 0 active 128000
# 8 7 "Afrodisíaco" STEAM_1:1:740393488 11:25 93 0 active 786432
# 10 9 "Stoble" STEAM_1:1:239746361 11:25 109 0 active 124000
# 11 10 "RAnho peludo" STEAM_1:0:467375649 11:25 99 0 active 786432
# 12 11 "qiosk<3" STEAM_1:0:638446620 11:25 75 0 active 196608
# 13 12 "ок пон" STEAM_1:1:631547287 11:25 60 0 active 196608
# 14 13 "Accept" STEAM_1:1:583201043 11:25 87 0 active 786432
#end
"""

faceit_api_key = "d7e53670-ffad-45cf-a8b7-08067f257c8e"

# Extract Steam IDs and Faceit levels from the example status command output
results = extract_steam_ids_and_faceit_levels(status_output, faceit_api_key)

# Print the results in a table format
print("{:<20} {:<15}".format("Name", "Faceit Level"))
print("-" * 35)
for name, faceit_level in results:
    print("{:<20} {:<15}".format(name, faceit_level))