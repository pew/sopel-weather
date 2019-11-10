import datetime

import requests
import sopel


API_KEY = "insert_api_key_here"


def weather(wt, location):
    payload = {"q": location, "units": "metric", "APPID": API_KEY}
    req = requests.get(
        "https://api.openweathermap.org/data/2.5/{}".format(wt), params=payload
    )
    if wt == "daily":
        req = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast/daily?cnt=3",
            params=payload,
        )
    if req.status_code != 200:
        return "error code: ", req.status_code
    response = req.json()
    return response


@sopel.module.commands("weather")
def w(bot, trigger):
    if not trigger.group(2):
        return bot.reply("please provide a location.")
    query = trigger.group(2)

    current_weather = weather("weather", query)
    bot.say(
        "Weather for: {} | current temperature: {}°C | min. temperature: {}°C | max. temperature {}°C | {}".format(
            current_weather["name"],
            current_weather["main"]["temp"],
            current_weather["main"]["temp_min"],
            current_weather["main"]["temp_max"],
            current_weather["weather"][0]["description"],
        )
    )


@sopel.module.commands("forecast")
def f(bot, trigger):
    if not trigger.group(2):
        return bot.reply("please provide a location.")
    query = trigger.group(2)

    forecast_weather = weather("daily", query)

    for day in forecast_weather["list"]:
        dt = datetime.datetime.fromtimestamp(day["dt"]).strftime("%Y-%m-%d")

        bot.say(
            "Weather for: {}, {} | {}: {}°C | min. temperature: {}°C | max. temperature {}°C".format(
                forecast_weather["city"]["name"],
                forecast_weather["city"]["country"],
                dt,
                day["temp"]["day"],
                day["temp"]["max"],
                day["temp"]["min"],
            )
        )
