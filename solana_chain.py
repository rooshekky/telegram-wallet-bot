import requests,base58,json,os
from nacl.signing import SigningKey
from config import SOL_RPC

FILE="sol_wallet.json"

def create_wallet():

    key=SigningKey.generate()

    private=base58.b58encode(key._seed).decode()

    public=base58.b58encode(key.verify_key.encode()).decode()

    data={"address":public,"private":private}

    json.dump(data,open(FILE,"w"))

    return public

def load_wallet():

    if not os.path.exists(FILE):
        return None

    data=json.load(open(FILE))

    return data["address"],data["private"]

def get_balance(address):

    payload={
    "jsonrpc":"2.0",
    "id":1,
    "method":"getBalance",
    "params":[address]
    }

    r=requests.post(SOL_RPC,json=payload)

    lamports=r.json()["result"]["value"]

    return lamports/1000000000
