## verification_sms_flask

This example implements the SMS verification method for a new account creation. Only verified account can login and create a new post.

## Requirements

1. Python3 (with venv)
2. Flask
3. Requirements for `verification_sms`


## Installation

Run the following commands:
```
python3 -m venv venv
```
```
. venv/bin/activate
```

```
pip install -r requirements.txt
```

```
pip install -e ..
```

## Setup & Run
Run the following commands:
Remeber to replace `YOUR_EMAIL_HERE` and `YOUR_PASSWORD_HERE` with you Google Voice email and password.

```
export FLASK_APP=flaskr
```
```
export FLASK_ENV=development
```
```
export GMAIL_ADDRESS=YOUR_EMAIL_HERE
```
```
export GMAIL_PASSWORD=YOUR_PASSWORD_HERE
```
```
flask init-db
```
```
flask run
```

## Use

1. Go to `http://localhost:5000/`
2. From top-right, click `Register`
3. Enter your information, including your phone number.
4. Enter the verfication code from the text message you recieve on your phone.
5. Your account will be created and verified. Any other account not putting the code will not be able to login.
