#!/usr/bin/python2.7
import datetime
import plistlib
import subprocess
import sys

# Todo: the logic below needs to be cleaned up and easier to follow. Error
# handling needs to be improved for easier troubleshooting.

# Obtain username of the last logged in user
syslog_cmd = ['/usr/bin/syslog', '-F', 'xml', '-k', 'Facility',
              'com.apple.system.lastlog', '-k', 'Sender', 'loginwindow']

try:
    user = plistlib.readPlistFromString(
        subprocess.check_output(syslog_cmd))[-1]['ut_user']
except IndexError:
    # An IndexError may occur if the return from syslog contains no entries for
    # 'com.apple.system.lastlog'.
    print('<result>-1</result>')
    sys.exit(1)

output = subprocess.check_output(
    ['/usr/bin/dscl', '.', '-read', '/Users/' + user, 'PasswordPolicyOptions'])
try:
    plist = plistlib.readPlistFromString('\n'.join(output.split()[1:]))

    # When read from 'PasswordPolicyOptions' the date is a 'datetime' object
    lastSetDate = plist['passwordLastSetTime'].date()
except Exception:
    # If 'passwordLastSetTime' does not exist the data will be found in 'accountPolicyData'
    # This is expected on 10.10 or newer clients that were not migrated
    output = subprocess.check_output(
        ['/usr/bin/dscl', '.', '-read', '/Users/' + user, 'accountPolicyData'])
    try:
        plist = plistlib.readPlistFromString('\n'.join(output.split()[1:]))
    except Exception:
        print("<result>-2</result>")
        sys.exit(2)

    try:
        # When read from 'accountPolicyData' the date is a unix timestamp
        lastSetDate = datetime.datetime.utcfromtimestamp(
            plist['passwordLastSetTime']).date()
    except Exception:
        try:
            # If 'passwordLastSetTime' does not exist fall back to the account
            # creation timestamp
            lastSetDate = datetime.datetime.utcfromtimestamp(
                plist['creationTime']).date()
        except Exception:
            print("<result>-3</result>")
            sys.exit(3)

today = datetime.datetime.utcnow().date()

print("<result>{}</result>".format((today - lastSetDate).days))
sys.exit(0)
