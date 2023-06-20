import requests
from bs4 import BeautifulSoup

# Send a GET request to the website
url = 'http://192.168.0.104:3000/lua/hosts_stats.lua'
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all h1 elements
h1_elements = soup.find_all('h1')
print(h1_elements)

# Find the parent element
parent_element = soup.find('body')
print(parent_element)

# Find elements with a specific class within the parent element
child_elements = parent_element.find_all('div ')






# for anchor in first10:
#     print(anchor.text) # 

# print(r.url)
# print(r.status_code)

# print(r)