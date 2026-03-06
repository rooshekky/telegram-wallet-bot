import json
import os
from eth_account import Account
from cryptography.fernet import Fernet

WALLET_FILE = "wallet.json"
KEY_FILE = "wallet.key"

if not os.path.exists(KEY_FILE):

    with open(KEY_FILE, "wb") as f:
        f.write(Fernet.generate_key())

cipher = Fernet(open(KEY_FILE, "rb").read())


def create_wallet():

    acct = Account.create()

    encrypted = cipher.encrypt(acct.key.hex().encode())

    data = {
        "address": acct.address,
        "private": encrypted.decode()
    }

    json.dump(data, open(WALLET_FILE, "w"))

    return acct.address


def load_wallet():

    if not os.path.exists(WALLET_FILE):
        return None

    data = json.load(open(WALLET_FILE))

    private = cipher.decrypt(data["private"].encode()).decode()

    return data["address"], private
