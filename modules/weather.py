#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from datetime import datetime
import requests

from config.json_config import *
from config.utils import cache_func
from modules.module_template import ModuleTemplate


class Weather(ModuleTemplate):

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

    @cache_func(".cache/weather", config.get('lang'))
    def __weather_request(self):
        s = requests.Session()
        r = s.get("http://api.openweathermap.org/data/2.5/weather",
                  params=self.__weather_params)
        s.close()
        cur_weather = json.loads(r.text)
        return cur_weather

    def run(self) -> dict:
        cur_weather = self.__weather_request()

        tmp_words = {'description': cur_weather['weather'][0]['description'],
                     'v$time': '{} {}'.format(self.__WEEKDAYS[self.__now.weekday()],
                                              self.__now.strftime('%H:%M')),
                     'v$date': self.__now.strftime('%d %B %H:%M'),
                     'v$temperature': cur_weather["main"]["temp"],
                     'v$cloudiness': cur_weather["clouds"]["all"],
                     'v$wind_speed': cur_weather["wind"]["speed"],
                     'v$humidity': cur_weather["main"]["humidity"],
                     'v$pressure': cur_weather["main"]["pressure"],
                     'percentage': '%', 'celsius': '°C', 'tab': self.__spaces}
        self.__words.update(tmp_words)

        screen_out = "{now} {{bold}}{{fyellow}}{city}{{rst}}\n" \
                     "{tab}{{bold}}{{fgreen}}{time}{{rst}}: {v$date}\n" \
                     "{tab}{{bold}}{{fcyan}}{description}{{rst}}\n" \
                     "{tab}{{bold}}{{fgreen}}{temperature}{{rst}}: {v$temperature} {celsius}\n" \
                     "{tab}{{bold}}{{fgreen}}{cloudiness}{{rst}}: {v$cloudiness} {percentage}\n" \
                     "{tab}{{bold}}{{fgreen}}{wind}{{rst}}: {v$wind_speed} {wind_type}\n" \
                     "{tab}{{bold}}{{fgreen}}{humidity}{{rst}}: {v$humidity} {percentage}\n" \
                     "{tab}{{bold}}{{fgreen}}{pressure}{{rst}}: {v$pressure} {pressure_type}\n" \
            .format(**self.__words)
        tts_out = '{now} {city} {on} {v$date} {description}, {temperature} {v$temperature} {celsius}'.format(
            **self.__words)

        res = {'text': screen_out,
               'voice': tts_out}
        return res


weather = Weather("weather")
