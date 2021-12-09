
class Ctrl:
    signal_dictionary: dict
    command_dictionary: dict
    pairs: list
    input_files: dict
    output_files: dict
    date_times: dict
    debug_deltas: dict

    def __init__(self):
        self.signal_dictionary = {}
        self.command_dictionary = {}
        self.pairs = []
        self.input_files = {}
        self.output_files = {}
        self.date_times = {}
        self.debug_deltas = {}
