import requests
from colorama import Fore

while True:
    print(Fore.BLUE + 'Enter a city: ', end='')
    city = input()

    query = {'query': city, 'access_key': '1ca7680656f01632db2c543226b44484', 'units': 'f'}
    weather = requests.get('http://api.weatherstack.com/current', params=query)

    data_types = [
        'observation_time', 'temperature', 'weather_descriptions',
        'wind_speed', 'wind_degree', 'wind_direction', 'pressure',
        'precip', 'humidity', 'cloudcover', 'feelslike', 'uv_index',
        'visibility'
    ]

    data_loop = True

    while data_loop:
        print(Fore.BLUE + 'Enter a data type ("help" for possible data types, "new_city" to enter a new city): ', end='')
        data = input()

        if data == 'help':
            print(Fore.YELLOW + 'Possible data types are:')
            print(Fore.WHITE + '\n'.join(data_types))
        elif data == 'new_city':
            break
        elif data in data_types:
            print(Fore.WHITE)
            print(weather.json()['current'][data], end="\n")
        else:
            print(Fore.YELLOW + "Invalid data type provided")