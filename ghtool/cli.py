'''
This module contains method for console entry point
'''
from ghtool import init_parser, MAP_CMD_TO_CLASS
import sys

def main():
    '''
    This method parses input arguments and returns
    result (text) of specific command execution or
    displays help.
    '''
    parser = init_parser()
    cnt_argvs = len(sys.argv)
    if cnt_argvs == 1:
        parser.print_help()
    elif cnt_argvs == 2:
        command = sys.argv[1]
        if any(command in s for s in list(MAP_CMD_TO_CLASS.keys())):
            parser.parse_args([command, '-h'])
        else:
            parser.parse_args()
    else:
        args = parser.parse_args()
        MAP_CMD_TO_CLASS[args.cmd](args).execute()

if __name__ == "__main__":
    main()
