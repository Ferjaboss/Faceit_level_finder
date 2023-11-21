# SteamID to Faceit Level Converter

## Project Description

The SteamID to Faceit Level Converter is a Python application designed to simplify the process of retrieving Faceit levels for CS:GO players encountered in matchmaking. Leveraging the FACEIT API and the STEAM API, the project fetches relevant data from the internet. By inputting the `status` command returned data from your CS:GO game, the Python script automatically parses the information, extracts players' SteamID64 from their SteamID, and queries the Faceit API for their Faceit levels. The results are presented in a user-friendly table format.

## Features

- Retrieves Faceit levels of CS:GO players using their SteamID64.
- Provides a straightforward and efficient way to check the Faceit levels of opponents in matchmaking.

## Installation

1. Clone this repository or download the ZIP file.

2. Install the required libraries by running:
   ```bash
   pip install -r requirements.txt
## Set up the Faceit API key:
Create a file named .env in the root directory of the project.
Open the .env file in a text editor.
Add the following line, replacing your_actual_api_key with your Faceit API key:
FACEIT_API_KEY=your_actual_api_key
