"""
   This module sets up a logging object that can be used for log.info()
   and log.debug() messages. It serves to provide -vvv verbose functionality
   for the users of this application.
"""
import logging

def get_logger(verbosity):
    """
       Create a new logger object, based on the verbosity level passed in
       (an integer from 0 to 3), and return it to the caller.
       For using in sub-modules, other than main, see this post:
       https://stackoverflow.com/questions/7621897/python-logging-module-globally
       For main(), you have to wait until the options are parsed with
       ArgumentParser(), so you have to define the 'log' object thusly:
           from .logger import get_logger
           main()
               options = parse_args()
               global log
               log = get_logger(options.verbosity)
               log.info('hello world')
    """
    log = logging.getLogger('root')
    format = "%(levelname)s:%(filename)s:%(funcName)s(): %(message)s"
    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    level = min(verbosity, 3)
    logging.basicConfig(format=format)
    log.setLevel(levels[level])
    return log

def show_msg(msg):
    """
       This is for messages that we always want to show to the user. 
       I just abstracted it to this, to give a place for any extra logic
       we might want in the future.
    """
    print(msg)
