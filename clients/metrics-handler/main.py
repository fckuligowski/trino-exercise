import argparse
import logging
from .logger import get_logger
from .main_process import main_process

def main():
    # Parse the command line args
    prog = 'metrics-handler'
    options = parse_args(prog)
    # Use --verbose and create a global log object so that 
    # all these functions can just say log.info() or log.debug()
    # without having to pass some object everywhere
    global log
    log = get_logger(options.v)
    # Main processing
    log.info(options)
    main_process(options)

def parse_args(prog):
    """
       Setup all the command line arguments for this program, parse the
       command given by the user, and return an object (options) that
       contains all the parsed command line arguments. Throw an error if the
       user provided invalid syntax for this command.
    """
    desc = 'Metrics Handler for Trino - part of the test for Starburst Data'
    parser = argparse.ArgumentParser(prog, description=desc,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # User Name
    phelp = 'User Id to connect to the XCDE API'
    parser.add_argument('-u', '--user', help=phelp, required=True)
    # Password
    # phelp = 'Password to connect to the XCDE API'
    # parser.add_argument('-p', '--pwd', help=phelp, required=True)
    # Trino API Hostname
    phelp = 'Trino API Hostname'
    def_val = 'localhost'
    parser.add_argument('-a', '--api_host', help=phelp, default=def_val)
    # Trino API Hostname
    phelp = 'Trino API Port'
    def_val = '8080'
    parser.add_argument('-p', '--port', help=phelp, default=def_val)
    # Log Verbosity arg
    logargs = parser.add_argument_group("Logging Verbosity")
    logargs.add_argument('-v', help='Set verbosity level', default=0,
        action='count', dest='v')
    # Parse the arguments given by the user
    options = parser.parse_args()
    return options    
