# main.py 

import sys
if sys.version_info<(3,6):
    print("Requires Python 3.6 or later, the current version is "
        + sys.version)
    raise Requires36
import argparse

from flask import Flask, request, session

from bozen.butil import pr, prn

import config
import allpages
from allpages import app
import templateglobal
import models

# pages of app:
import login
import front
import blog
import mess
import account

# do this last:
import adminsite

#---------------------------------------------------------------------

#@app.route("/")
#def hello():
#    return "Hello World!"

#---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="""\
Start the web app
""")
    parser.add_argument("-d", "--debug",
        help="Run in debugging mode",
        action="store_true")
    parser.add_argument("-p", "--port",
        help="Port number to use",
        type=int,
        default=config.PORT)
    parser.add_argument("-v", "--verbose",
        help="Make output more verbose",
        action="store_true")
    commandLineArgs = parser.parse_args()
    prn("commandLineArgs=%r" % (commandLineArgs,))
    host = "127.0.0.1" if commandLineArgs.debug else "0.0.0.0"

    app.run(host=host, 
        port=commandLineArgs.port, 
        debug=commandLineArgs.debug)

if __name__ == '__main__':
    print("Starting web app...")
    main()
    
#end
