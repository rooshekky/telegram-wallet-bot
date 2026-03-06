import json
import os
from eth_account import Account

FILE = "wallet.json"

def create_wallet():

    acct = Account.create()

    data = {
        "address": acct.address,
        "private": acct.key.hex()
    }

    json.dump(data, open(FILE,"w"))

    return data["address"]

def load_wallet():

    if not os.path.exists(FILE):
        return None

    data=json.load(open(FILE))

    return data["address"],data["private"]
