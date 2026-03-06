import os
from flask import Flask, render_template, request, session, redirect
import qrcode

from database import init_db
from auth import verify_telegram
from portfolio import prices
from wallet import load_wallet
from evm_chains import get_balances
from solana_chain import load_wallet as load_sol, get_balance

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "wallet-secret")

init_db()


@app.route("/")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    evm = load_wallet()
    sol = load_sol()

    balances = {}
    total = 0

    price = prices()

    if evm:

        address, _ = evm

        evm_bal = get_balances(address)

        eth = evm_bal.get("eth", 0)
        matic = evm_bal.get("polygon", 0)
        bnb = evm_bal.get("bsc", 0)

        balances["ETH"] = eth
        balances["MATIC"] = matic
        balances["BNB"] = bnb

        total += eth * price["ethereum"]["usd"]
        total += matic * price["matic-network"]["usd"]
        total += bnb * price["binancecoin"]["usd"]

    if sol:

        sol_address, _ = sol

        sol_balance = get_balance(sol_address)

        balances["SOL"] = sol_balance

        total += sol_balance * price["solana"]["usd"]

    return render_template(
        "dashboard.html",
        balances=balances,
        total=round(total, 2)
    )


@app.route("/login")
def login():

    return render_template("login.html")


@app.route("/auth")
def auth():

    data = request.args.to_dict()

    if verify_telegram(data):

        session["user"] = data["id"]

        return redirect("/")

    return "Telegram authentication failed"


@app.route("/receive")
def receive():

    if "user" not in session:
        return redirect("/login")

    evm = load_wallet()
    sol = load_sol()

    evm_address = None
    sol_address = None

    if evm:
        evm_address = evm[0]

        img = qrcode.make(evm_address)

        img.save("static/evm_qr.png")

    if sol:
        sol_address = sol[0]

        img = qrcode.make(sol_address)

        img.save("static/sol_qr.png")

    return render_template(
        "receive.html",
        evm=evm_address,
        sol=sol_address
    )


@app.route("/send")
def send():

    if "user" not in session:
        return redirect("/login")

    return render_template("send.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 3000))

    app.run(
        host="0.0.0.0",
        port=port
    )
