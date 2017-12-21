#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import colorama
from colorama import Style, Fore, Back

colorama.init(wrap=False)
colorama.init(autoreset=True)
sys.stdout = colorama.AnsiToWin32(sys.stdout).stream


class ColoredText:
    def __init__(self) -> None:
        self.__values = {'rst': Style.RESET_ALL, 'bold': Style.BRIGHT, 'thick': Style.DIM,
                         'fblack': Fore.BLACK, 'fred': Fore.RED, 'fgreen': Fore.GREEN,
                         'fyellow': Fore.YELLOW, 'fblue': Fore.BLUE, 'fmagenta': Fore.MAGENTA,
                         'fcyan': Fore.CYAN, 'fwhite': Fore.WHITE,
                         'bblack': Back.BLACK, 'bred': Back.RED, 'bgreen': Back.GREEN,
                         'byellow': Back.YELLOW, 'bblue': Back.BLUE, 'bmagenta': Back.MAGENTA,
                         'bcyan': Back.CYAN, 'bwhite': Back.WHITE
                         }

        self.__nonevalues = {i: '' for i in self.__values.keys()}

    def color(self, source: str):
        """
        This function make text colored
        :param source: input string
        :return: colored text
        """
        return source.format(**self.__values)

    def nocolor(self, source: str):
        """
        This function make colored text plain
        :param source: input string
        :return: plain text
        """
        return source.format(**self.__nonevalues)


colored_text = ColoredText()
