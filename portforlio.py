import requests

def prices():

    url="https://api.coingecko.com/api/v3/simple/price"

    params={
    "ids":"ethereum,binancecoin,matic-network,solana",
    "vs_currencies":"usd"
    }

    return requests.get(url,params=params).json()
