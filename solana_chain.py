import os
import json
import base58
from solana.rpc.api import Client
from solders.keypair import Keypair
from config import SOL_RPC

SOL_WALLET_FILE = "sol_wallet.json"

client = Client(SOL_RPC)


def create_sol_wallet():

    kp = Keypair()

    private_key = base58.b58encode(bytes(kp)).decode()

    data = {
        "address": str(kp.pubkey()),
        "private": private_key
    }

    json.dump(data, open(SOL_WALLET_FILE, "w"))

    return data["address"]


def load_sol_wallet():

    if not os.path.exists(SOL_WALLET_FILE):
        return None

    data = json.load(open(SOL_WALLET_FILE))

    return data["address"], data["private"]


def get_sol_balance(address):

    balance = client.get_balance(address)

    return balance.value / 1_000_000_000
