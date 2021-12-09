from work_with_files import clear_folder, close_files, get_cmd, get_sign, delete_prefix, get_prefix
import os
from ctrl import Ctrl

times = []
debug_folder = "debug_output"


def if_folder_not_exists_create(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def create_inner_folder(outer_folder: str, inner_folder: str):
    debug_type = inner_folder # name of inner folder is same as a debug type
    inner_folder = f"{outer_folder}/{debug_type}" # path relative to project root
    if_folder_not_exists_create(inner_folder)
    return [inner_folder, debug_type]


def preparing_folder_operations(folder_name):
    if_folder_not_exists_create(folder_name)
    clear_folder(folder_name)


class OriginalTime:
    sec_begin_2000: float
    date_time: str

    def __init__(self, sec_begin_2000, date_time):
        self.sec_begin_2000 = sec_begin_2000
        self.date_time = date_time


def find_date(date):
    date_str = ""
    for dat in times:
        if dat.sec_begin_2000 == date:
            date_str = dat.datetime
            break
    return date_str


def print_original_times_with_converted_times(date_times: dict):
    files = {}
    inner_folder, debug_type = create_inner_folder(debug_folder, "original")

    for key in date_times.keys():
        cmd_name = delete_prefix(key)
        prefix = get_prefix(key)

        expanded_cmd_prefix = ""

        if prefix == "c":
            expanded_cmd_prefix = "command"
        elif prefix == "s":
            expanded_cmd_prefix = "signal"

        if key not in files.keys():
            file_name = f"{inner_folder}/{debug_type}_{expanded_cmd_prefix}_{cmd_name}.debug"
            files[key] = open(file_name, "w", encoding="utf-8")
            files[key].write(f"{cmd_name}\n")

        for date_time in date_times[key]:
            files[key].write(f"{date_time.sec_begin_2000:.3f} | {date_time.date_time}\n")

    close_files(files)


def write_sorted_times(container: dict, cmd_prefix: str):
    files = {}
    inner_folder, debug_type = create_inner_folder(debug_folder, "sorted")

    for key in container.keys():
        if key not in files.keys():
            cmd_name = delete_prefix(key)
            file_name = f"{inner_folder}/{debug_type}_{cmd_prefix}_{cmd_name}.debug"
            files[key] = open(file_name, "w")
            files[key].write(f"{cmd_name}\n")

        for cmd in container[key]:
            files[key].write(f"{cmd}\n")

    close_files(files)


def accumulate_times(input_container: dict, output_container: dict):
    for key in input_container.keys():
        if key not in output_container.keys():
            output_container[key] = input_container[key]
        else:
            output_container[key] += input_container[key]


def accumulate_some_word(input_container: dict, output_container: dict):
    key = frozenset({'c_word_6', 's_word_5'})
    key_cmd = get_cmd(key)

    if key_cmd not in output_container.keys():
        output_container[key_cmd] = []

    if key in input_container.keys():
        for time in input_container[key].commands:
            if key_cmd not in output_container.keys():
                output_container[key_cmd] = [time]
            else:
                output_container[key_cmd].append(time)


def accumulate_times_from_files(input_files: list, signals: dict, commands: dict):
    for input_file in input_files:
        accumulate_times(input_file.commands, commands)
        accumulate_times(input_file.signals, signals)
        accumulate_some_word(input_file.paired_times, commands)


def sort_times_in_container(container):
    if isinstance(container, dict):
        for times in container.values():
            times.sort()
        for times in container:
            times.sort()


def print_sorted_times(input_files: list):
    signals = {}
    commands = {}

    accumulate_times_from_files(input_files, signals, commands)

    write_sorted_times(commands, "command")
    write_sorted_times(signals, "signal")


def approximately_equal(checking, number):
    return number - 0.05 <= checking <= number + 0.05


def check_several(checking: list, number):
    for ch in checking:
        if approximately_equal(ch, number):
            return True


class AllTimes:
    all_signals: list
    all_commands: list

    def __init__(self, signals, commands):
        self.all_signals = signals
        self.all_commands = commands

    def append(self, signals, commands):
        self.all_signals += signals
        self.all_commands += commands


def print_lens_of_signals_and_commands(input_files: dict):
    l_all_times = {}

    for input_file in input_files.values():
        paired_times = input_file.paired_times
        for key in paired_times.keys():
            signals = paired_times[key].signals
            commands = paired_times[key].commands
            if key not in l_all_times.keys():
                l_all_times[key] = AllTimes(signals, commands)
            else:
                l_all_times[key].append(signals, commands)

    for key in l_all_times.keys():
        print("sign:",
              f"{get_sign(key):30}",
              "cmd:",
              f"{get_cmd(key):30}",
              "signals:", len(l_all_times[key].all_signals),
              "commands:", len(l_all_times[key].all_commands))


def print_deltas_and_times(debug_deltas: dict):
    files = {}
    inner_folder, debug_type = create_inner_folder(debug_folder, "deltas")

    for key in debug_deltas.keys():
        if key not in files.keys():
            signal = delete_prefix(get_sign(key))
            command = delete_prefix(get_cmd(key))
            filename = f"{debug_folder}/{debug_type}/{debug_type}_{signal}_{command}.debug"
            files[key] = open(filename, "w")

        output_string = f"sign: {signal:12} cmd: {command:10} deltas"
        print(f"\n{output_string}")
        files[key].write(f"{output_string}\n")
        for debug_delta in debug_deltas[key]:
            print(debug_delta)
            files[key].write(f"{debug_delta}\n")

    close_files(files)


def print_debug_output(ctrl: Ctrl):
    preparing_folder_operations(debug_folder)
    print_deltas_and_times(ctrl.debug_deltas)
    print_lens_of_signals_and_commands(ctrl.input_files)
    print_original_times_with_converted_times(ctrl.date_times)
    print_sorted_times(ctrl.input_files.values())

