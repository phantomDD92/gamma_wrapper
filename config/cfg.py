import logging
import sys
from config.command_line import parse_commandLine_args

# get command line parameters
CML_PARAMETERS = parse_commandLine_args(sys.argv[1:])

# set config parameters
API_URL = "https://wire3.gamma.xyz"
