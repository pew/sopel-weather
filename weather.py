"""openweathermap.org module for sopel"""
import datetime

import requests
import sopel
from sopel.config.types import NO_DEFAULT, StaticSection, ValidatedAttribute


class WeatherSection(StaticSection):
    """config section for sopel"""

    api_key = ValidatedAttribute("api_key", default=NO_DEFAULT)


def setup(bot):
    """setup bot"""
    bot.config.define_section("weather", WeatherSection)


def configure(config):
    """define / setup bot configuration and api key"""
    config.define_section("weather", WeatherSection)
    config.weather.configure_setting(
        "api_key", "Please set an openweathermap.org api key"
    )


def get_weather(location, weather_type=None, api_key=None):
    """get current weather or forecast"""
    payload = {"q": location, "units": "metric", "APPID": api_key}

    if weather_type == "daily":
        req = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast/daily?cnt=3",
            params=payload,
        )
    else:
        req = requests.get(
            "https://api.openweathermap.org/data/2.5/weather", params=payload
        )
    if req.status_code == 404:
        response = req.json()
        raise ConnectionError(response["message"])
    if req.status_code != 200:
        raise ConnectionError("error code: ", req.status_code)
    response = req.json()
    return response


@sopel.module.commands("weather")
def weather(bot, trigger):
    """current weather trigger"""
    if not trigger.group(2):
        return bot.reply("please provide a location.")
    query = trigger.group(2)

    try:
        current_weather = get_weather(query, api_key=bot.config.weather.api_key)
    except ConnectionError as err:
        return bot.say(str(err))
    else:
        return bot.say(
            "Weather for: {}, {} | cur. temp: {}°C | min. temp: {}°C | max. temp: {}°C | {}".format(
                current_weather["name"],
                current_weather["sys"]["country"],
                current_weather["main"]["temp"],
                current_weather["main"]["temp_min"],
                current_weather["main"]["temp_max"],
                current_weather["weather"][0]["description"],
            )
        )


@sopel.module.commands("forecast")
def forecast(bot, trigger):
    """forecast weather trigger"""
    if not trigger.group(2):
        return bot.reply("please provide a location.")
    query = trigger.group(2)

    try:
        forecast_weather = get_weather(query, "daily", bot.config.weather.api_key)
    except ConnectionError as err:
        return bot.say(str(err))
    else:
        for day in forecast_weather["list"]:
            timestamp = datetime.datetime.fromtimestamp(day["dt"]).strftime("%Y-%m-%d")

            bot.say(
                "Forecast for: {}, {} | {}: avg. temp: {}°C | min. temp: {}°C | max. temp: {}°C".format(
                    forecast_weather["city"]["name"],
                    forecast_weather["city"]["country"],
                    timestamp,
                    day["temp"]["day"],
                    day["temp"]["max"],
                    day["temp"]["min"],
                )
            )
