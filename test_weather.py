from unittest.mock import patch, Mock
from weather_tool import weather

def test_invalid_city():
    with patch("weather_tool.requests.get") as mock_get:
        response = Mock()
        response.json.return_value = {} 
        mock_get.return_value = response

        result = weather("thiscitydoesnotexist12345")
    assert result == "Could not find the city thiscitydoesnotexist12345"

def test_weather_with_mock():
    with patch("weather_tool.requests.get") as mock_get:

        location_response = Mock()
        location_response.json.return_value = {
            "results": [
                {
                 "latitude": 35.6762,
                  "longitude": 139.6503   
                }
            ]
        }


        weather_response = Mock()
        weather_response.json.return_value ={
            "current": {
                "temperature_2m": 25
            }
        }

        mock_get.side_effect = [location_response, weather_response]
        result = weather("Tokyo")

    assert result == "The weather in Tokyo is 25°C"