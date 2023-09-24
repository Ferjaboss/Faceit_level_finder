# SteamID to Faceit Level Converter

## Project Description

The SteamID to Faceit Level Converter is a Python application that simplifies the process of finding the Faceit levels of CS:GO players encountered in matchmaking. This project uses the FACEIT API and the STEAM API to fetch data from the internet. When you input the `status` command returned data from your CS:GO game, Python automatically parses the data and extracts all the players' SteamID64 from their SteamID. It then calls the Faceit API to fetch their Faceit levels. The results are displayed in an easy-to-read table format.

## Features

- Fetches Faceit levels of CS:GO players using their SteamID64.
- Provides a simple and efficient way to check the Faceit levels of your opponents in matchmaking.

## Installation

1. Clone this repository or download the ZIP file.

2. Install the required libraries by running:
   pip install requests
   pip install customtkinter
   pip install tk
## Usage
Run main.py to launch the SteamID to Faceit Level Converter.

Input the status command returned data from your CS:GO game into the provided input box.

Click the "Extract Faceit Levels" button to retrieve the Faceit levels of the encountered players.

The results will be displayed in a table format, showing the player names and their corresponding Faceit levels.

Future Plans
The next update for this project aims to make it even more user-friendly. There are two potential paths:

Integration with CS:GO: Integrate this tool directly into the CS:GO interface, allowing users to execute a command in the game to retrieve player Faceit levels seamlessly.
