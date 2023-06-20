import requests
from bs4 import BeautifulSoup
import json

# Send a GET request to the website
url = 'http://192.168.0.104:3000/lua/index.lua'
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the desired data and store it in a dictionary
data = {
    'titles': soup.find('h1').text,
}

# Convert the data to JSON
json_data = json.dumps(data)

# Print the JSON data
print(json_data)