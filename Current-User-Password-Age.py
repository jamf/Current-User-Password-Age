#!/usr/bin/python2.7
import datetime
import plistlib
import subprocess

# Obtain username from last logged in user
user = plistlib.readPlistFromString(subprocess.check_output(['/usr/bin/syslog', '-F', 'xml', '-k', 'Facility', 'com.apple.system.lastlog', '-k', 'Sender', 'loginwindow']))[-1]['ut_user']

# Use 'dcsl' to read 'PasswordPolicyOptions' data
# This first method works on 10.9 or earlier clients, or 10.10 clients that migrated from earlier versions
output = subprocess.check_output(['/usr/bin/dscl', '.', '-read', '/Users/' + user, 'PasswordPolicyOptions'])
try:
    plist = plistlib.readPlistFromString('\n'.join(output.split()[1:]))
    
    # When read from 'PasswordPolicyOptions' the date is a 'datetime' object
    lastSetDate = plist['passwordLastSetTime'].date()
except Exception:
    # If 'passwordLastSetTime' does not exist the data will be found in 'accountPolicyData'
    # This is expected on 10.10 or newer clients that were not migrated
    output = subprocess.check_output(['/usr/bin/dscl', '.', '-read', '/Users/' + user, 'accountPolicyData'])
    try:
        # The syntax below strips the first line from 'output' which is not valid XML
        plist = plistlib.readPlistFromString('\n'.join(output.split()[1:]))
        
        # When read from 'accountPolicyData' the date is in a floating point/real number timestamp format
        lastSetDate = datetime.datetime.utcfromtimestamp(plist['passwordLastSetTime']).date()
    except Exception:
        try:
            # If 'passwordLastSetTime' does not exist fall back to the account creation timestamp
            lastSetDate = datetime.datetime.utcfromtimestamp(plist['creationTime']).date()
        except Exception:
            # If unable to determine any usable timestamp from the above, exit with a 'No Value' result
            print("<result>No Value</result>")
            raise SystemExit

# 'datetime' supports addition and subtraction between 'datetime.date' objects
# We use this here to obtain the number of days from today and the 'lastSetDate'
today = datetime.datetime.utcnow().date()
passwordAge = (today - lastSetDate).days

# Output the result for the extension attribute
print("<result>{0}</result>".format(passwordAge))
