import enum

from ctrl import Ctrl


class word_7(enum.Enum):
    Both = 1
    Rise = 2
    Descent = 3


def fill_deltas(snd_times: list, rcv_times: list, deltas: list, debug_deltas = None) -> None:
    sup = 0
    inf = 0
    end = False
    upper_limit = 25
    for t_send in snd_times:
        if end:
            break
        while sup < len(rcv_times):
            t_recv = rcv_times[sup]
            if t_recv <= t_send:
                if sup + 1 == len(rcv_times):
                    if rcv_times[inf] <= t_send:
                        delta = t_send - rcv_times[inf]
                        if delta < upper_limit:
                            deltas.append(delta)
                            if debug_deltas is not None:
                                debug_deltas.append(f'{t_send:>.3f} | {rcv_times[inf]:>.3f} | {delta:.3f}')
                            end = True
                            break
                sup = sup + 1
            else:
                if rcv_times[inf] <= t_send:
                    delta = t_send - rcv_times[inf]
                    if delta > upper_limit:
                        inf = inf + 1
                        continue
                    deltas.append(delta)
                    if debug_deltas is not None:
                        debug_deltas.append(f'{t_send:>.3f} | {rcv_times[inf]:>.3f} | {delta:.3f}')
                inf = sup
                break


def calc_deltas(paired_times: dict, debug_deltas=None):
    for key in paired_times.keys():
        if key not in debug_deltas.keys():
            debug_deltas[key] = []
        fill_deltas(paired_times[key].signals, paired_times[key].commands, paired_times[key].deltas, debug_deltas[key])


def find_last_less_then(commands: list, border: float):
    last = 0.0

    if commands[0] > border:
        last = commands.pop(0)

    while commands:
        cmd = commands[0]
        if cmd > border:
            break
        else:
            del commands[0]
            last = cmd

    return last


def find_first_large_then(container: list, value: float):
    for element in container:
        if element > value:
            return element


def value_between(check_value: float, min_value: float, max_value: float):
    return min_value <= check_value <= max_value


def find_all_times_between_two_other(container: list, min_value: float, max_value: float):
    return [ element for element in container if not value_between(element, min_value, max_value) ]


def clear_some_word_commands(some_other_word_list: list, word_3_list: list, mode_some_word_list: list, some_word=word_7.Both):

    output_list = []

    cp_some_other_word_list = some_other_word_list.copy()
    cp_word_3_list = word_3_list.copy()

    some_other_word = cp_some_other_word_list[0]
    word_3 = cp_word_3_list[0]
    if some_other_word <= mode_some_word_list[0] and word_3 <= mode_some_word_list[0]:
        del cp_some_other_word_list[0]
        del cp_word_3_list[0]
        output_list.append(max(some_other_word, word_3))

    for t in mode_some_word_list:

        there_is_new_word_3 = False
        there_is_new_some_other_word = False

        while cp_word_3_list:
            cmd = cp_word_3_list[0]
            if cmd > t:
                break
            else:
                del cp_word_3_list[0]
                word_3 = cmd
                there_is_new_word_3 = True

        while cp_some_other_word_list:
            cmd = cp_some_other_word_list[0]
            if cmd > t:
                break
            else:
                del cp_some_other_word_list[0]
                some_other_word = cmd
                there_is_new_some_other_word = True

        both = some_word == word_7.Both
        rise = some_word == word_7.Rise
        descent = some_word == word_7.Descent

        if both or rise:
            if there_is_new_some_other_word and there_is_new_word_3:
                new_element = max(some_other_word, word_3)
                output_list.append(new_element)

        if both or descent:
            if not there_is_new_some_other_word and there_is_new_word_3:
                output_list.append(word_3)

    return output_list


def clear_co12_co26(co26: list, co12: list):
    sup = 0
    inf = 0
    inc = 0
    remove_index = []
    while inc < len(co26):
        while sup < len(co12) and co26[inc] >= co12[sup]:
            if sup != inf:
                remove_index.append(sup)

            sup = sup + 1
        if sup < len(co12):
            if co26[inc] < co12[sup]:
                if len(remove_index) == 1:
                    if inc + 1 < len(co26):
                        del co26[inc + 1]
                        if sup < len(co12):
                            del co12[sup]
                            del co12[remove_index[0] - 1]
                            sup = sup - 1  # Перестройка индексов

                else:
                    if len(remove_index) == 2:
                        del co12[remove_index[1]]
                        del co12[remove_index[0] - 1]
                        if inc + 1 < len(co26):
                            del co26[inc + 1]
                        sup = sup - 2  # Перестройка индексов
                    else:
                        sup = sup - 1
                        del co12[sup]
                        del co26[inc]
                        inc = inc - 1

                inf = sup
            remove_index.clear()
        else:
            if len(remove_index) == 2:
                del co12[remove_index[1]]
            if len(remove_index) > 0:
                del co12[remove_index[0] - 1]
            if inc + 1 < len(co26):
                del co26[inc + 1]

        inc = inc + 1


def process_times(paired_times: dict, some_word=word_7.Both):
    for times in paired_times.values():
        times.sort()

    pair = frozenset(["s_word_5", "c_CO12"])
    if pair in paired_times.keys():
        times = paired_times[pair]
        clear_co12_co26(times.signals, times.commands)

    s_some_word = "s_word_5"
    c_some_other_word = "c_word_8"
    c_word_3 = "c_word_9"
    first_pair = frozenset([s_some_word, c_some_other_word])
    second_pair = frozenset([s_some_word, c_word_3])
    if first_pair in paired_times.keys() and second_pair in paired_times.keys():
        some_other_word_list = paired_times[first_pair].commands
        word_3_list = paired_times[second_pair].commands
        mode_some_word_list = paired_times[first_pair].signals

        paired_times.pop(first_pair)
        times = paired_times.pop(second_pair)
        times.commands = clear_some_word_commands(some_other_word_list, word_3_list, mode_some_word_list, some_word=some_word)

        paired_times[frozenset([s_some_word, "c_word_6"])] = times

    for times in paired_times.values():
        times.sort()


def calc_deltas_for_every_file(ctrl: Ctrl, some_word=word_7.Both):
    for input_file in ctrl.input_files.values():
        process_times(input_file.paired_times, some_word=some_word)
        calc_deltas(input_file.paired_times, ctrl.debug_deltas)
