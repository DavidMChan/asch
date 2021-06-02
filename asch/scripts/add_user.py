
import hashlib
import datetime
import pymongo
import getpass
import sys

from asch.config import Config

# Connect to the mongo DB
_db = pymongo.MongoClient(Config.get_or_else('database', 'CONNECTION_STRING', None)).asch

username = input('Username: ')
password_1 = getpass.getpass(prompt='Password: ', stream=None)
password_2 = getpass.getpass(prompt='Re-Enter Password: ', stream=None)

if password_1.strip() != password_2.strip():
    print('Error: Passwords do not match')
    sys.exit(1)

salt = datetime.datetime.utcnow().isoformat()
password_hash = hashlib.sha512((password_1.strip() + salt).encode('utf8')).hexdigest()

if _db.users.find_one({'username': username}) is not None:
    result = input('User already exists... Update password? [y/N] ')
    if result.strip() not in ('y', 'Y', 'yes'):
        print('Error: User already exists.')
        sys.exit(1)


# Insert the new user document

_db.users.insert_one({
    'username': username.strip(),
    'password_hash': password_hash,
    'salt': salt,
    'tokens': {}
})
