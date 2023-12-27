from abc import ABC, abstractmethod

import requests


class WeatherServiceException(Exception):
    pass


class WeatherService(ABC):
    """Определяет контракт для всех сервисов погоды."""

    @abstractmethod
    def get_temperature(self, city):
        pass


class OpenWeatherMapService(WeatherService):
    """Конкретная стратегия для OpenWeatherMap."""

    def __init__(self, api_key):
        self.api_key = api_key

    def get_temperature(self, city):
        try:
            if not city:
                raise WeatherServiceException("City is a required parameter.")

            url = (f"https://api.openweathermap.org/data/2.5/weather?q={city}"
                   f"&appid={self.api_key}&units=metric")
            response = requests.get(url)

            if response.status_code != 200:
                raise WeatherServiceException("Failed to retrieve data.")

            data = response.json()

            if 'main' not in data or 'temp' not in data['main']:
                raise WeatherServiceException("Weather data not found.")

            return round(data['main']['temp'])

        except WeatherServiceException as e:
            raise WeatherServiceException(e)


class WeatherApp:
    """Контекст, который использует стратегию (сервис погоды)."""

    def __init__(self, weather_service):
        self.weather_service = weather_service

    def get_temperature(self, city):
        return self.weather_service.get_temperature(city)


def main():
    try:
        api_key = "YOUR API KEY"
        open_weather_map_service = OpenWeatherMapService(api_key)
        weather_app = WeatherApp(open_weather_map_service)

        city = "London"
        result = weather_app.get_temperature(city)

        print(f"Current temperature in {city}: {result}°C")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
