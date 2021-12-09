import debug
import check_distribution
import deltas
from deltas import word_7
import parsing
import work_with_files


from ctrl import Ctrl


def main():
    ctrl = Ctrl()
    parsing.parse_main(ctrl)
    deltas.calc_deltas_for_every_file(ctrl, some_word=word_7.Rise)
    debug.print_debug_output(ctrl)
    work_with_files.create_output_files(ctrl.output_files, ctrl.input_files, separate=False)
    check_distribution.check_distributions(False)


if __name__ == "__main__":
    main()
