from web3 import Web3
from config import ETH_RPC, POLYGON_RPC, BSC_RPC

eth = Web3(Web3.HTTPProvider(ETH_RPC))
polygon = Web3(Web3.HTTPProvider(POLYGON_RPC))
bsc = Web3(Web3.HTTPProvider(BSC_RPC))

CHAINS = {
    "eth": eth,
    "polygon": polygon,
    "bsc": bsc
}


def get_balances(address):

    balances = {}

    for name, web3 in CHAINS.items():

        balance = web3.eth.get_balance(address)

        balances[name] = web3.from_wei(balance, "ether")

    return balances
