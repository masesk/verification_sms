# verification_sms
Verification SMS sent from Google Voice account to a given phone number. Useful for unique user account creation.

## Requirements
1. Python3 (with Venv)
2. ChromeDriver (Chromium)
3. Gmail Account (w/o 2FA)
4. Google Voice Account activated. [Sign up and activate and account here](https://voice.google.com/)
5. selenium
6. webdriver_manager


## Limitations
1. One SMS process handler. If busy, error will be thrown.
2. Synchronized calls.

## Setup

To install on pip, simply do 
```
pip install -e .
```

## Use
```
from verification_sms import VerificationSMS

vm = VerificationSMS()

# email - Google Voice activated account email
# password - Google Voice activated account password
# phone - Phone number to receive the verification code
# vcode - Verification code sent to phone number

vm.send_message(email, password, phone, vcode)
```

## Example
Check `example/flask` for a working application that implements the functionality on a blog account from the official Flask tutorial.

Follow `example/README.md` to properly run the Flask example.