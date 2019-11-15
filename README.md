# sopel weather

get current weather and three day forecast for a location.

## requirements & installation

* have a sopel bot running
* get an api key from [OpenWeather](https://openweathermap.org/)
* `requests` library (`pip install -r requirements.txt`)

add this configuration block to your `~/.sopel/default.cfg` file with your api key:

```
[weather]
api_key = my-api-ey-from-open-Weather
```

## usage

current weather for a given location:

```
.weather berlin
```

three day forecast for a given location:

```
.forecast berlin
```
