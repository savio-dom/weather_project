import requests

def weather(city: str)-> str:
    print(f'the weather tool was used for {city}')

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params ={
        "name": city,
        "count": 1,

    }

    try:

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "results" not in data: 
            return f'Could not find the city {city}'

        latitude = data["results"][0]["latitude"]
        longitude = data["results"][0]["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m"
    }

        weather_response = requests.get(weather_url, params= weather_params,timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        temp = weather_data["current"]["temperature_2m"]
        return(f'The weather in {city} is {temp}°C')
    
    except requests.exceptions.Timeout:
        return "The weather service took too long to respond"
    
    except requests.exceptions.HTTPError:
        return "The weather service returned an HTTP error"

    except requests.exceptions.RequestException:
        return "Could not connect to the weather service"
