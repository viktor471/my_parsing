import typing
import os


def close_files(files):
    if isinstance(files, list):
        for file in files:
            file.close()
    if isinstance(files, dict):
        for file in files.values():
            file.close()


def delete_prefix(string: str):
    return string.partition("_")[2]


def get_prefix(string: str):
    return string.partition("_")[0]


def get_sorted_list(container):
    pair_list = list(container)
    pair_list.sort(reverse=True)
    return pair_list


def get_sign(pair: frozenset):
    return get_sorted_list(pair)[0]


def get_cmd(pair: frozenset):
    return get_sorted_list(pair)[1]


def clear_folder(path: str):
    files = os.listdir(path)
    for file in files:
        file_path = path + "/" + file
        if os.path.isfile(file_path):
            os.remove(file_path)
        if os.path.isdir(file_path):
            clear_folder(file_path)


class OutputFile:
    deltas: list
    file: typing.TextIO

    def __init__(self, file_key):
        if not os.path.exists("output"):
            os.mkdir("output")
        self.file = open("output/" + file_key + ".log", "w")
        self.deltas = []

    def write_output(self):
        for delta in self.deltas:
            self.file.write(f"{delta:.3f}\n")
            self.file.flush()

    def __del__(self):
        self.file.close()


class InputFile:
    signals: dict
    commands: dict
    paired_times: dict
    file: typing.TextIO

    def __init__(self, file: str):
        self.file = open(file, "r", encoding="utf-8")
        self.signals = {}
        self.commands = {}
        self.paired_times = {}

    def __del__(self):
        self.file.close()

    def read(self) -> list:
        return self.file.readlines()


def generate_output_files_with_directions(output_files, input_files, separate=True):
    for input_file_key in input_files.keys():
        direction = input_file_key.split("_")[0]
        input_file = input_files[input_file_key]
        for pair in input_file.paired_times.keys():
            command = delete_prefix(get_cmd(pair))
            signal = delete_prefix(get_sign(pair))
            if separate:
                file_name = direction + "_" + command + "_" + signal
                key = frozenset(list(pair) + [direction])
            else:
                file_name = command + "_" + signal
                key = pair
            if key not in output_files.keys():
                output_files[key] = OutputFile(file_name)

            output_files[key].deltas += input_file.paired_times[pair].deltas


def write_output(output_files: dict):
    for output_file in output_files.values():
        output_file.write_output()


def create_output_files(output_files: dict, input_files: dict, separate=True):
    clear_folder("output")
    generate_output_files_with_directions(output_files, input_files, separate)
    write_output(output_files)



