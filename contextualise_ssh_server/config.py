# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy, logging-format-interpolation
# pylint: disable=missing-docstring, trailing-whitespace, trailing-newlines, too-few-public-methods

import logging
import sys
from pathlib import Path
from configparser import ConfigParser
from configparser import ExtendedInterpolation
from contextualise_ssh_server.parse_args import args

logger = logging.getLogger(__name__)

CONFIG = ConfigParser(interpolation=ExtendedInterpolation())
CONFIG.optionxform = lambda option: option

def set_defaults():
    CONFIG.read_dict ({'main': {
        'config'      :  args.config,
        'loglevel'    :  args.loglevel,
        'logfile'     :  args.logfile,
        'verbose'     :  args.verbose,
        'debug'       :  args.debug,
        }})


def load_config():
    """Reload configuration from disk.

    Config locations, by priority (first one wins)
    """
    files = []


    files += [
        Path(F'/etc/{args.basename}.conf'),
        Path(F'./{args.basename}.conf'),
        Path(F'{args.dirname}/{args.basename}.conf')
    ]

    try:
        files += [Path(args.config)]
    except FileNotFoundError:
        pass
    except TypeError:
        pass

    read_a_config = False
    for f in files:
        try:
            if f.exists():
                logger.info("Using this config file: {}".format(f))
                CONFIG.read(f)
                read_a_config = True
                break
        except PermissionError:
            pass
    if not read_a_config:
        filelist = [str(f) for f in files]
        filestring = "\n    ".join(filelist)
        logger.warning(F"Warning: Could not read any config file from \n"\
                F"    {filestring}")
        # sys.exit(4)


def test_config():
    try:
        delme = CONFIG['main']['logfile']
        delme = CONFIG['main']['loglevel']
        delme = CONFIG['main']['verbose']
    except KeyError as e:
        logging.error(F"Cannot find required config entry: {e}")
        sys.exit(3)

set_defaults()
load_config()
test_config()

