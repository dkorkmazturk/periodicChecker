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

#import smtplib
#from email import message
#
#def sendInfoMail(website):
#    SENDER = "sender_mail"
#    RECEIVER = "receiver_mail"
#
#    msg = message.Message()
#    msg.add_header('from', SENDER)
#    msg.add_header('to', RECEIVER)
#    msg.add_header('subject', 'A website that being tracked has been updated!')
#    msg.set_payload('A change has been observed at ' + website + ' on ' + time.ctime() + '\n')
#
#    mailServer = smtplib.SMTP_SSL("smtp_server")
#    mailServer.login(SENDER, "passwd")
#    mailServer.send_message(msg, SENDER, RECEIVER)
#    mailServer.quit()

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

        if len(argv) > 3 and argv[3] == "-q":
            quiet = True
        else:
            quiet = False

        return website, period, quiet

    except IndexError:
        sys.stderr.write("USAGE: periodicChecker.py <website> <period(s|m|h)> (-q)")
        sys.exit(1)
    except ValueError:
        sys.stderr.write("ERROR: Enter period in integer format. Example: 10s(same as just 10), 10m, 10h")
        sys.exit(1)

def main(website, period, quiet):
    oldmd5 = 0

    if quiet:
        print("INFO: Quiet mode has activated. Only the observed changes are going to print message.")

    try:
        while(True):
            temp_file, headers = urllib.request.urlretrieve(website)
            newmd5 = hashlib.md5(open(temp_file, 'rb').read()).hexdigest()
            os.remove(temp_file)
            
            if oldmd5 != 0:
                if newmd5 != oldmd5:
                    print("\033[5;30;42mA change has been observed at \033[5;30;43m" + website + "\033[0;30;46m (" + time.ctime() + ")\033[0m")
                    #sendInfoMail(website)
                elif not quiet:
                    print("\033[0;31mThere is no change has been observed at \033[1;33m" + website + " \033[0;36m(" + time.ctime() + ")\033[0m")

            oldmd5 = newmd5
            time.sleep(period)

    except KeyboardInterrupt:
        if os.path.isfile(temp_file):
            os.remove(temp_file)
        sys.exit(0)
    except ValueError:
        sys.stderr.write("ERROR: Invalid website: " + website)
        sys.exit(1)
    except urllib.error.URLError:
        sys.stderr.write("ERROR: Failed to connect to " + website)
        sys.exit(1)

if __name__ == "__main__":
    main(*processArgs(sys.argv))
