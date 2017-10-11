#!/usr/bin/python3

#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2017 Dogukan Korkmazturk <d.korkmazturk@gmail.com>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.

import sys
import os
import signal
import urllib.request
import hashlib
import time

def processArgs(argv):
    try:
        website = argv[1]

        if argv[2].endswith("s"):
            period = int(argv[2][0:-1])
        elif argv[2].endswith("m"):
            period = int(argv[2][0:-1]) * 60
        elif argv[2].endswith("h"):
            period = int(argv[2][0:-1]) * 3600
        else:
            period = int(argv[2])

        return website, period

    except IndexError:
        print("Usage: periodicChecker.py <website> <period(s|m|h)>")
        sys.exit(1)
    except ValueError:
        print("Enter period in integer format. Example: 10s(same as just 10), 10m, 10h")
        sys.exit(1)

def main(website, period):
    oldmd5 = 0

    try:
        while(True):
            temp_file, headers = urllib.request.urlretrieve(website)
            newmd5 = hashlib.md5(open(temp_file, 'rb').read()).hexdigest()
            os.remove(temp_file)
            
            if oldmd5 != 0:
                if newmd5 != oldmd5:
                    print("\033[5;30;42mA change has been observed at \033[5;30;43m" + website + "\033[0;30;46m (" + time.ctime() + ")\033[0m")
                else:
                    print("\033[0;31mThere is no change has been observed at \033[1;33m" + website + " \033[0;36m(" + time.ctime() + ")\033[0m")

            oldmd5 = newmd5
            time.sleep(period)

    except KeyboardInterrupt:
        if os.path.isfile(temp_file):
            os.remove(temp_file)
        sys.exit(0)
    except ValueError:
        print("Invalid website: " + website)
        sys.exit(1)
    except urllib.error.URLError:
        print("Failed to connect to " + website)
        sys.exit(1)

if __name__ == "__main__":
    website, period = processArgs(sys.argv)
    main(website, period)
