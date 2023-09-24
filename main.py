import requests
import re 
import time
import customtkinter as tk
from prettytable import PrettyTable 
from tkinter import ttk

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
        return "Unknown / Doesn't play Faceit"
    
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

def extract_and_display_faceit_levels():
    status_data = input_text.get("1.0", tk.END)  # Get input from the text box
    results = extract_steam_ids_and_faceit_levels(status_data, faceit_api_key)

    # Clear the Treeview
    for row in result_tree.get_children():
        result_tree.delete(row)

    # Insert the results into the Treeview
    for name, faceit_level in results:
        result_tree.insert("", "end", values=(name, faceit_level))

def remove_placeholder(event):
    current_text = input_text.get("1.0", tk.END).strip()
    if current_text == placeholder_text:
        input_text.delete("1.0", tk.END)

# Create the main GUI window
root = tk.CTk()  # Use tk.CTk() for custom tkinter
root.title("Steam ID to Faceit Level")
root.geometry("500x600")

# Create an input text box for the status_output variable with larger size
input_text = tk.CTkTextbox(root, wrap=tk.WORD, width=500, height=280)  # Adjust height and width as needed
input_text.pack(expand=tk.YES, fill=tk.BOTH)

# Placeholder text
placeholder_text = "Type 'status' in the CS:GO console and paste the result here."

# Add the placeholder text to the input text box
input_text.insert(tk.END, placeholder_text)

# Bind the remove_placeholder function to the input text box when it gains focus
input_text.bind("<FocusIn>", remove_placeholder)

# Create a button to extract and display Faceit levels using CTkButton
extract_button = tk.CTkButton(root, text="Extract Faceit Levels", command=extract_and_display_faceit_levels)
extract_button.pack()

# Create a Treeview for displaying the results as a table
result_tree = ttk.Treeview(root, columns=("Name", "Faceit Level"), show="headings")
result_tree.heading("Name", text="Name")
result_tree.heading("Faceit Level", text="Faceit Level")
result_tree.pack(expand=tk.YES, fill=tk.BOTH)

# Faceit API key
faceit_api_key = "d7e53670-ffad-45cf-a8b7-08067f257c8e"

# Start the GUI main loop
root.mainloop()
