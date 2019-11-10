import datetime

import requests
import sopel


API_KEY = "insert_api_key_here"


def weather(wt, location):
    payload = {"q": location, "units": "metric", "APPID": API_KEY}

    if wt == "daily":
        req = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast/daily?cnt=3",
            params=payload,
        )
    else:
        req = requests.get(
            "https://api.openweathermap.org/data/2.5/{}".format(wt), params=payload
        )
    if req.status_code != 200:
        raise ConnectionError("error code: ", req.status_code)
    response = req.json()
    return response


@sopel.module.commands("weather")
def w(bot, trigger):
    if not trigger.group(2):
        return bot.reply("please provide a location.")
    query = trigger.group(2)

    try:
        current_weather = weather("weather", query)
    except (ConnectionError, TypeError) as err:
        return bot.say(str(err))
    else:
        bot.say(
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
def f(bot, trigger):
    if not trigger.group(2):
        return bot.reply("please provide a location.")
    query = trigger.group(2)

    try:
        forecast_weather = weather("daily", query)
    except (ConnectionError, TypeError) as err:
        return bot.say(str(err))
    else:
        for day in forecast_weather["list"]:
            dt = datetime.datetime.fromtimestamp(day["dt"]).strftime("%Y-%m-%d")

            bot.say(
                "Weather for: {}, {} | {}: avg. temp: {}°C | min. temp: {}°C | max. temp: {}°C".format(
                    forecast_weather["city"]["name"],
                    forecast_weather["city"]["country"],
                    dt,
                    day["temp"]["day"],
                    day["temp"]["max"],
                    day["temp"]["min"],
                )
            )
