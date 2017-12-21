#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from modules import funcs


class ModuleTemplate:
    def __init__(self, str_command: str) -> None:
        self.__str_command = str_command
        funcs[str_command] = self.run
        pass

    def run(self) -> dict:
        '''Main work function
        :return: dict {'text': out text on screen, 'voice':out voice text via tts}
        '''
        raise NotImplementedError("Should have implemented this")
