"""Parse commandline options"""

import argparse
import os
import sys


def parseOptions():
    """Parse commandline options"""

    folder_of_executable = os.path.split(sys.argv[0])[0]
    basename = os.path.basename(sys.argv[0]).rstrip('.py')
    dirname  = os.path.dirname(__file__)

    # config_file = os.environ['HOME']+F'/.config/{basename}.conf'
    config_file = F'/etc/contextualise_ssh_server.conf'
    config_file = F'contextualise_ssh_server.conf'
    log_file    = folder_of_executable + F'/{basename}.log'
    log_file    = ""

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--verbose",    "-v",   action="count", default=0, help="Verbosity")
    parser.add_argument("--debug",      "-d",   action="count", default=0, help="Logmode debug")
    parser.add_argument("--config",     "-c",   default=config_file,
            help="config file")
    parser.add_argument("--basename",           default=basename)
    parser.add_argument("--dirname",            default=dirname)
    parser.add_argument("--logfile",            default=log_file, help="logfile")
    parser.add_argument("--loglevel",           default=os.environ.get("LOG", "WARNING").upper(),
                                                help="Debugging Level")
    parser.add_argument(dest="access_token",    default=None, nargs="?",
                                                help="An access token (without 'Bearer ')",)
    parser.add_argument("--base",       "-b",   action="store_true", default=False)
    parser.add_argument("--no-sudo",            default=True, action="store_false", dest="sudo",
            help="Map user to a special user, assuming that it's the one able to sudo")
    parser.add_argument("--user",               default="cloudadm")
    return parser


# reparse args on import
args = parseOptions().parse_args()
