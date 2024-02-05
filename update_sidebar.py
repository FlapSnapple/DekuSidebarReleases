import praw #pip3 install praw
from datetime import datetime

from config import (
	cache_dir,
	subreddit,
	new_reddit_widget_name,
	old_reddit_section_heading,
	release_table_header,
	release_table_alignment,
	games_to_display,
	release_table_footer_nintendo,
	release_table_footer_dekudeals,
	client_id,
	client_secret,
	user_agent,
	username,
	password
)

# Authenticate to Reddit
reddit = praw.Reddit(
	client_id=client_id,
	client_secret=client_secret,
	user_agent=user_agent,
	username=username,
	password=password
)

# Get the current date in yyyy-mm-dd format
date_str = datetime.now().strftime('%Y-%m-%d')

# Define the directory and filename
directory = cache_dir
raw_filename = f'{directory}/{date_str}_raw.json'
cleaned_filename = f'{directory}/{date_str}_cleaned.txt'

# Read the contents of the cleaned file
with open(cleaned_filename, 'r', encoding='utf-8') as f:
	cleaned_data = f.read()

	# Trim the data if it exceeds the defined length
	cleaned_data_lines = cleaned_data.split('\n')
	if len(cleaned_data_lines) > games_to_display:
		cleaned_data = '\n'.join(cleaned_data_lines[:games_to_display])
		cleaned_data_new_reddit = f"{release_table_header}\n{release_table_alignment}\n{cleaned_data}\n{release_table_footer_dekudeals}"
		cleaned_data_old_reddit = f"{release_table_header}\n{release_table_alignment}\n{cleaned_data}\n"

# Search for "Upcoming Releases" widget on new Reddit
for widget in reddit.subreddit(subreddit).widgets.sidebar:
	if widget.shortName == new_reddit_widget_name:
		# Found the widget on new Reddit
		# print('Found "Upcoming Releases" widget on new Reddit')
		if widget.text != cleaned_data_new_reddit:
			widget.mod.update(text=cleaned_data_new_reddit)
			print('Success: Updated "Upcoming Releases" widget on new Reddit')
		else:
			print('Info: Sidebar widget is already up to date on new Reddit')
		break
		
# Search for "Upcoming Releases" section on old Reddit
for line in reddit.subreddit(subreddit).wiki['config/sidebar'].content_md.split('\n'):
	if line.strip() == old_reddit_section_heading:
		# Found the section on old Reddit
		print('Info: Found "Upcoming Releases" section on old Reddit')
		break
