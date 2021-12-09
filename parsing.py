import os
from datetime import datetime as dt
import json
import re

from ctrl import Ctrl
from debug import OriginalTime
from work_with_files import InputFile, get_sorted_list

config_name = "config.json"


class Pair:
    signal: str
    command: str

    def __init__(self, pair: list[2]):
        self.signal = pair[0]
        self.command = pair[1]


class PairedTimes:
    signals: list
    commands: list
    deltas: list

    def __init__(self, pair: list, input_file: InputFile):
        self.signals = input_file.signals[pair[0]]
        self.commands = input_file.commands[pair[1]]
        self.deltas = []

    def sort(self):
        self.signals.sort()
        self.commands.sort()


def get_files(ctrl: Ctrl, folder_name: str):
    last_dir = os.path.abspath(".")
    os.chdir(folder_name)
    files = os.listdir()
    for file in files:
        if "log" in file:
            ctrl.input_files[file] = InputFile(file)
    os.chdir(last_dir)


def load_config(ctrl: Ctrl):
    config = open(config_name, "r", encoding="utf-8")
    data = json.load(config)
    folder_name = data["folder"]
    ctrl.command_dictionary = data["commands"]
    ctrl.signal_dictionary = data["signals"]
    get_files(ctrl, folder_name)
    get_files(ctrl, folder_name + "/channels")

    for pair in data["pairs"]:
        ctrl.pairs.append(frozenset(pair))


def get_sec_begin_2000_from_line(line: str) -> OriginalTime:
    date_and_time = line.split("[")[1].split("]")[0]
    date = dt.strptime(date_and_time, '%d.%m.%y %H:%M:%S.%f')
    date_2000 = dt(2000, 1, 1)

    time_in_square_brackets = (date - date_2000).total_seconds()

    return OriginalTime(time_in_square_brackets, date_and_time)


def check_if_pair_parsed(pair: frozenset, input_file: InputFile):
    for signal_key in input_file.signals.keys():
        for command_key in input_file.commands.keys():
            if pair == frozenset([signal_key, command_key]):
                return True


def get_pairs_from_text(text: list, input_file: InputFile, ctrl: Ctrl):
    parse(text, input_file.signals, ctrl.signal_dictionary, ctrl.date_times)
    parse(text, input_file.commands, ctrl.command_dictionary, ctrl.date_times)

    for pair in ctrl.pairs:
        if check_if_pair_parsed(pair, input_file):
            pair_list = get_sorted_list(pair)
            input_file.paired_times[pair] = PairedTimes(pair_list, input_file)


def parse(text, container: dict, dictionary: dict, original_times: dict):
    for line in text:
        for key in dictionary.keys():
            if re.search(dictionary[key], line):
                if key not in container.keys():
                    container[key] = []

                date_and_time = get_sec_begin_2000_from_line(line)
                container[key].append(date_and_time.sec_begin_2000)

                if original_times is not None:
                    if key not in original_times.keys():
                        original_times[key] = []
                    original_times[key].append(date_and_time)


def parse_main(ctrl: Ctrl):
    load_config(ctrl)
    input_files = ctrl.input_files.values()

    for input_file in input_files:
        text = input_file.read()
        get_pairs_from_text(text, input_file, ctrl)
