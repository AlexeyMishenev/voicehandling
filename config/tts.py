#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from gtts import gTTS
from playsound import playsound


def say(text, *, lang='en'):
    res_path = "../result.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(res_path)
    playsound(res_path)
    os.remove(res_path)
