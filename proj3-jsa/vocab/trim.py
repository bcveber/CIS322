"""
Trim trailing whitespace from all lines in a file.

Usage: python3 trim.py input_file >output_file

"""

import argparse
import sys
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)


def command_line_args():
    """Returns namespace with settings from command line"""
    log.debug("-> Command line args")
    parser = argparse.ArgumentParser(description="Trim trailing whitespace")
    parser.add_argument("-D", "--debug", dest="DEBUG",
                        action="store_const", const=True,
                        help="Turn on debugging and verbose logging")
    parser.add_argument("input_file", help="Input text to trim",
                        nargs="?",
                        type=argparse.FileType('r'),
                        default=sys.stdin)
    cli_args = parser.parse_args()
    log.debug("<- Command line args: {}".format(cli_args))
    return cli_args


def trim_lines(infile):
    """
    Trim and print each line.
    """
    for line in infile:
        trimmed = line.rstrip()
        print(trimmed)


if __name__ == "__main__":
    cli_args = command_line_args()
    infile = cli_args.input_file
    trim_lines(infile)
