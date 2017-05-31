# Current User Password Age

This script runs as an extension attribute for Jamf Pro. It extracts data from the `dscl` record of the currently logged in user and, based upon one of two timestamps, calculates the age of their password in days.

If errors are encountered that prevent the script from returning a valid result, they are returned as negative integers.

Error code reference:

* __-1:__ Unable to obtain username from _com.apple.system.lastlog_
* __-2:__ Error occurred trying to parse _PasswordPolicyOptions_ or _accountPolicyData_.
* __-3:__ Unable to obtain __passwordLastSetTime__ or __creationTime__ values.

## Extension Attribute Settings

Upload the script to your JSS in your extension attributes. Set the value for `Data Type` to `Integer`. This script has been tested against 10.9, 10.10, and 10.12 clients.

## License

```
JAMF Software Standard License

Copyright (c) 2017, JAMF Software, LLC. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of the JAMF Software, LLC nor the names of its contributors
      may be used to endorse or promote products derived from this software without
      specific prior written permission.

THIS SOFTWARE IS PROVIDED BY JAMF SOFTWARE, LLC "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL JAMF SOFTWARE, LLC BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```