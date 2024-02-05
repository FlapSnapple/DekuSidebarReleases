import os
import json
import requests #pip3 install requests
from datetime import datetime
from config import (
	cache_dir,
	deku_api_endpoint,
    deku_api_key,
	deku_results_per_page
)

# Get the current date in yyyy-mm-dd format
date_str = datetime.now().strftime('%Y-%m-%d')

# Define the directory and filename
directory = cache_dir
raw_filename = f'{directory}/{date_str}_raw.json'

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Check if a file for today already exists, this way we only fetch new data once per day
if not os.path.exists(raw_filename):
	# Define the API endpoint
	base_deku_url = f'{deku_api_endpoint}games?filter=upcoming-releases&api_key={deku_api_key}'

	# Initialize the offset and temporary data array
	offset = 0
	data_array = []

	# Loop until all results are loaded
	while True:
		# Add the offset parameter to the API endpoint
		url_with_offset = f'{base_deku_url}&offset={offset}'

		# Send a GET request to the API
		response = requests.get(url_with_offset)

		# Check if the request was successful
		if response.status_code == 200:
			# Parse the JSON data from the response
			data = response.json()

			# Append the game information to the temporary array
			data_array.extend(data['games'])

			# Increment the offset for the next request
			offset += deku_results_per_page

			# Break the loop if all results have been loaded
			if offset >= data['total']:
				break
		else:
			print('Error: Failed to retrieve data from Deku Deals API')
			break

	# Write the data to a JSON file
	with open(raw_filename, 'a') as f:
		json.dump(data_array, f)

	print(f'Success: Wrote {len(data_array)} games to {raw_filename}')
else:
	print(f'Info: {raw_filename} already exists, skipping the API request to Deku Deals.')
