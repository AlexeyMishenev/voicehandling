#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
import time
from datetime import datetime

from modules import funcs
from config.json_config import *


class ModuleTemplate:
    def __init__(self, str_command: str) -> None:
        self.__str_command = str_command
        funcs[str_command] = self.run

        self.__now = datetime.fromtimestamp(time.time())
        self.__lang = config.get('lang')
        # locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8' if self.__lang == 'ru' else 'en_US.UTF-8')


    def run(self) -> dict:
        '''Main work function
        :return: dict {'text': out text on screen, 'voice':out voice text via tts}
        '''
        raise NotImplementedError("Should have implemented this")
