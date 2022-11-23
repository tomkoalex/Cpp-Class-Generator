import sys
import argparse
from qt_interface import MyWidget
from class_constructor import ClassConstructor

def qt_interface():
    widget = MyWidget()


def command_line():
    parser = argparse.ArgumentParser(description='C++ Class Generator')
    parser.add_argument('--creator', action='store', type=str, required=False, default='')
    parser.add_argument('--includes', type=str, required=False, default='')
    parser.add_argument('--base_classes', type=str, required=False, default='')
    parser.add_argument('--namespace', action='store', type=str, required=False, default='')
    parser.add_argument('--names', type=str, required=True, default='NewClass')
    parser.add_argument('--copy_constructor', action='store_true', required=False)
    parser.add_argument('--copy_assignment', action='store_true', required=False)
    parser.add_argument('--move_constructor', action='store_true', required=False)
    parser.add_argument('--move_assignment', action='store_true', required=False)
    parser.add_argument('--final', action='store_true',  required=False)
    parser.add_argument('--destructor', action='store_true', required=False)
    args = parser.parse_args()
    print(args)
    class_constructor = ClassConstructor(args.creator,
                                         args.includes,
                                         args.namespace,
                                         args.base_classes,
                                         args.names,
                                         args.copy_constructor,
                                         args.copy_assignment,
                                         args.move_constructor,
                                         args.move_assignment,
                                         args.final,
                                         args.destructor)
    class_constructor.to_file('h')
    class_constructor.to_file('cpp')


if __name__ == "__main__":
    if len(sys.argv) == 1:
        qt_interface()
    else:
        command_line()
