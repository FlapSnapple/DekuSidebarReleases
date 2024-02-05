import os
import json
from datetime import datetime
from config import cache_dir

# Get the current date in yyyy-mm-dd format
date_str = datetime.now().strftime('%Y-%m-%d')

# Define the directory and filename
directory = cache_dir
raw_filename = f'{directory}/{date_str}_raw.json'
cleaned_filename = f'{directory}/{date_str}_cleaned.txt'

# If cleaned_filename already exists, delete it
if os.path.exists(cleaned_filename):
	os.remove(cleaned_filename)

# Read the contents of the raw file
with open(raw_filename, 'r') as f:
	raw_data = json.load(f)

# Sort the games first by release_date, then by name
raw_data.sort(key=lambda x: (x['release_date'], x['name']))

# Initialize an empty list to store the cleaned up game data
cleaned_data = []

# Iterate over the games in the raw data and format it to be sidebar compatible
for game in raw_data:
	# Get the name of the game
	name = game['name']

	# Get the release date of the game and format it
	release_date = datetime.strptime(game['release_date'], '%Y-%m-%d').strftime('%b %d')

	# Check if the publisher includes "Nintendo"
	if 'Nintendo' in game['publishers']:
		# Append "**" to the front and end of the game name
		name = f"**{name}**"

	# Add the name and release date to the games_data list
	cleaned_data.append(f"{name} | {release_date}")

# Write the cleaned_data to a txt file
with open(cleaned_filename, 'w', encoding='utf-8') as f:
	f.write('\n'.join(cleaned_data))

print(f'Success: Wrote {len(cleaned_data)} games to {cleaned_filename}')
