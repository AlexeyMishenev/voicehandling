#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import time

import numpy as np
import requests

from config.json_config import *
from config.utils import cache_func, most_common
from modules.module_template import ModuleTemplate


class Forecast(ModuleTemplate):

    def __init__(self, str_command: str) -> None:
        super().__init__(str_command)
        self.__lang = config.get('lang')
        self.__now = datetime.fromtimestamp(time.time())
        self.__weather_params = config.get('weather_params')
        self.__WEEKDAYS = json_config.get('weekdays', section='datatime')
        self.__MONTHS = json_config.get('months', section='datatime')
        self.__words = json_config.get_all(section='weather')
        self.__weather_params['lang'] = self.__lang
        self.__spaces = ' ' * 3

    @cache_func(".cache/forecast", config.get('lang'))
    def __forecast_request(self):
        s = requests.Session()
        r = s.get("http://api.openweathermap.org/data/2.5/forecast",
                  params=self.__weather_params)
        cur_forecast = json.loads(r.text)
        s.close()
        return cur_forecast

    def run(self) -> dict:
        # tomorrow forecast
        cur_forecast = self.__forecast_request()
        n = cur_forecast['cnt']
        cur_forecast = cur_forecast['list']

        next_day = self.__now + timedelta(days=1)
        date_start, date_end = 0, 0
        while str(self.__now.date()) == str(
                datetime.utcfromtimestamp(cur_forecast[date_start]['dt']).date()):
            date_start += 1
            date_end += 1

        while str(next_day.date()) == str(
                datetime.utcfromtimestamp(cur_forecast[date_end]['dt']).date()):
            date_end += 1

        cur_forecast = cur_forecast[date_start:date_end]

        array = {'description': [], 'temperature': [], 'cloudiness': [],
                 'wind_speed': [], 'humidity': [], 'pressure': []}

        for cur_weather in cur_forecast:
            array['description'].append(cur_weather['weather'][0]['description'])
            array['temperature'].append(cur_weather["main"]["temp"])
            array['cloudiness'].append(cur_weather["clouds"]["all"])
            array['wind_speed'].append(cur_weather["wind"]["speed"])
            array['humidity'].append(cur_weather["main"]["humidity"])
            array['pressure'].append(cur_weather["main"]["pressure"])

        tmp_words = {'description': most_common(array['description']),
                     'v$date': datetime.utcfromtimestamp(cur_forecast[date_start]['dt']).strftime(
                         '%A %d %B'),
                     'v$temperature': round(float(np.mean(array['temperature']))),
                     'v$mintemperature': round(min(array['temperature'])),
                     'v$maxtemperature': round(max(array['temperature'])),
                     'v$cloudiness': round(float(np.mean(array['cloudiness'])), 2),
                     'v$wind_speed': round(float(np.mean(array['wind_speed'])), 2),
                     'v$humidity': round(float(np.mean(array['humidity'])), 2),
                     'v$pressure': round(float(np.mean(array['pressure'])), 2),
                     'percentage': '%', 'celsius': '°C', 'tab': self.__spaces}

        self.__words.update(tmp_words)

        screen_out = "{forecast} {{bold}}{{fyellow}}{city}{{rst}}\n" \
                     "{tab}{{bold}}{{fgreen}}{time}{{rst}}: {v$date}\n" \
                     "{tab}{{bold}}{{fcyan}}{avg} {description}{{rst}}\n" \
                     "{tab}{{bold}}{{fgreen}}{temperature}{{rst}}: {v$mintemperature}{celsius} — {v$maxtemperature}{celsius}\n" \
                     "{tab}{{bold}}{{fgreen}}{avg} {temperature}{{rst}}: {v$temperature} {celsius}\n" \
                     "{tab}{{bold}}{{fgreen}}{avg} {cloudiness}{{rst}}: {v$cloudiness} {percentage}\n" \
                     "{tab}{{bold}}{{fgreen}}{avg} {wind}{{rst}}: {v$wind_speed} {wind_type}\n" \
                     "{tab}{{bold}}{{fgreen}}{avg} {humidity}{{rst}}: {v$humidity} {percentage}\n" \
                     "{tab}{{bold}}{{fgreen}}{avg} {pressure}{{rst}}: {v$pressure} {pressure_type}\n" \
            .format(**self.__words)
        tts_out = "{forecast} {city} {on} {v$date}."
        tts_out += "{expected} {description}" if self.__lang == "ru" else "{description} {expected}"
        tts_out += "{temperature} {from} {v$mintemperature} {to} {v$maxtemperature}{celsius}"
        tts_out = tts_out.format(**self.__words)
        res = {'text': screen_out,
               'voice': tts_out}
        return res


forecast = Forecast('forecast')
