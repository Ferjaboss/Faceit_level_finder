import requests
import re 
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
        faceit_elo = get_faceit_level(steam_id64, faceit_api_key)

        if faceit_elo is not None:
            faceit_level = determine_faceit_level(faceit_elo)
            results.append((name, faceit_level))
        else:
            results.append((name, "Unknown"))

    return results
status_output = """
# userid name uniqueid connected ping loss state rate
# 1510 3 "avalone - debil" STEAM_1:1:504624495 09:26 108 0 active 196608
# 1518 5 "lolllu87" STEAM_1:1:768319784 04:40 112 0 active 196608
# 1491 6 "Spaghouta" STEAM_1:0:593847016 17:54 115 0 active 196608
# 1512 7 "Вор в загонах" STEAM_1:1:770271183 09:20 104 0 active 786432
# 776 8 "1v1" STEAM_1:1:792259059  4:52:38 58 0 active 786432
# 1492 9 "ligmaballs" STEAM_1:1:163819997 17:20 55 0 active 786432
# 1438 10 "kilmongerR?" STEAM_1:1:483405641 36:25 111 0 active 786432
# 1520 11 "Marlen"" STEAM_1:1:485136882 02:38 62 0 active 196608
# 1378 12 "Taboo" STEAM_1:1:497344131  1:01:18 97 0 active 786432
# 1495 13 "Грубый ниоткуда" STEAM_1:1:431180069 10:25 105 0 active 196608
"""

faceit_api_key = "d7e53670-ffad-45cf-a8b7-08067f257c8e"

# Extract Steam IDs and Faceit levels from the example status command output
results = extract_steam_ids_and_faceit_levels(status_output, faceit_api_key)

# Print the results in a table format
print("{:<20} {:<15}".format("Name", "Faceit Level"))
print("-" * 35)
for name, faceit_level in results:
    print("{:<20} {:<15}".format(name, faceit_level))