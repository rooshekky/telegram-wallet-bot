import os
import json
import base58
import requests
from nacl.signing import SigningKey
from config import SOL_RPC

SOL_WALLET_FILE = "sol_wallet.json"


def create_sol_wallet():

    key = SigningKey.generate()

    private = base58.b58encode(key._seed).decode()

    public = base58.b58encode(key.verify_key.encode()).decode()

    data = {
        "address": public,
        "private": private
    }

    json.dump(data, open(SOL_WALLET_FILE, "w"))

    return public


def load_sol_wallet():

    if not os.path.exists(SOL_WALLET_FILE):
        return None

    data = json.load(open(SOL_WALLET_FILE))

    return data["address"], data["private"]


def get_sol_balance(address):

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [address]
    }

    r = requests.post(SOL_RPC, json=payload)

    lamports = r.json()["result"]["value"]

    return lamports / 1_000_000_000
