import json
from os import path
import sys

import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')

# # Required positional argument
# parser.add_argument('pos_arg', type=int,
#                     help='A required integer positional argument')

# # Optional positional argument
# parser.add_argument('opt_pos_arg', type=int, nargs='?',
#                     help='An optional integer positional argument')

# Optional argument
parser.add_argument('-country', type=str,
                    help='give the country code')

# Switch
parser.add_argument('-created_at', type=str,
                    help='crawle data created at before the given date')

args = parser.parse_args()

print(args.country)
