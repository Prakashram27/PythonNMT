import os

file_path = '/home/hp/demo/nyc_weather.csv'

if os.path.isfile(file_path):
    print("File exists")
else:
    print("File does not exist or the path is incorrect")