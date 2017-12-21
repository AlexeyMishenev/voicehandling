#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import os
import re

from config import tts
from config.colored_text import colored_text as clr
from config.json_config import config
from modules import funcs
from record import record_to_file


def arg_parse():
    parser = argparse.ArgumentParser("Voice handling project on OrangePi")
    parser.add_argument("--rec", help="need to record",
                        action="store_true")
    arguments = parser.parse_args()
    return arguments


def recognize(home_path: str):
    print("Trying to recognition...")
    bashCommand = "pocketsphinx_batch -argfile argsEnB > /dev/null 2>&1"
    os.system(bashCommand)

    with open(os.path.join(home_path, 'out.hyp'), 'r') as myfile:
        inputCommand = myfile.read()

    print('\nHyp: {}'.format(inputCommand))

    # old version
    # if '(' not in inputCommand:
    #     print('Some troubles happened while recognition')
    #     exit(0)

    # index = inputCommand.index('(')
    # command = inputCommand[:index - 1]

    # new version with regex
    match = re.search(r'(?P<command>.*)\s\(input1\s(?P<input1>.*)\)', inputCommand)

    if not match:
        print('Some troubles happened while recognition')
        exit(0)

    command = match.group('command')
    # input1 = match.group('input1')

    print("Result: {}\n".format(command))
    # os.remove(os.path.join(home_path, 'out.hyp'))

    run_command(command)


def run_command(command):
    result = funcs[command]()
    if 'text' in result and result['text']:
        print(clr.color(result['text']))
    if 'voice' in result and result['voice']:
        tts.say(result['voice'], lang=config.get('lang'))


def main(args):
    if args.rec:
        print("Say your command now")
        record_to_file(os.path.join('recognizing', 'input', 'input.wav'))
    recognize('recognizing')


if __name__ == '__main__':
    args = arg_parse()
    main(args)
