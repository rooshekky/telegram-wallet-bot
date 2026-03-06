from flask import Flask,render_template
from wallet import load_wallet
from solana_chain import load_wallet as load_sol,get_balance
from evm_chains import get_balances
from portfolio import prices

app=Flask(__name__)

@app.route("/")
def dashboard():

    evm=load_wallet()

    sol=load_sol()

    price=prices()

    balances={}

    total=0

    if evm:

        address,_=evm

        evmbal=get_balances(address)

        eth=evmbal["eth"]
        matic=evmbal["polygon"]
        bnb=evmbal["bsc"]

        balances["ETH"]=eth
        balances["MATIC"]=matic
        balances["BNB"]=bnb

        total+=eth*price["ethereum"]["usd"]
        total+=matic*price["matic-network"]["usd"]
        total+=bnb*price["binancecoin"]["usd"]

    if sol:

        addr,_=sol

        solbal=get_balance(addr)

        balances["SOL"]=solbal

        total+=solbal*price["solana"]["usd"]

    return render_template(
    "dashboard.html",
    balances=balances,
    total=round(total,2)
    )

@app.route("/send")
def send():

    return render_template("send.html")

@app.route("/receive")
def receive():

    evm=load_wallet()

    sol=load_sol()

    return render_template("receive.html",evm=evm,sol=sol)

app.run(host="0.0.0.0",port=3000)
