import os
import json
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from web3 import Web3
from eth_account import Account

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
RPC_URL = os.getenv("RPC_URL")

web3 = Web3(Web3.HTTPProvider(RPC_URL))

WALLET_FILE = "wallet.json"
KEY_FILE = "key.key"

# ERC20 ABI minimal
ERC20_ABI = [
    {
        "constant":True,
        "inputs":[{"name":"_owner","type":"address"}],
        "name":"balanceOf",
        "outputs":[{"name":"balance","type":"uint256"}],
        "type":"function",
    }
]

USDT_ADDRESS = Web3.to_checksum_address("0xdAC17F958D2ee523a2206206994597C13D831ec7")

# encryption
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE,"wb") as f:
        f.write(Fernet.generate_key())

cipher = Fernet(open(KEY_FILE,"rb").read())

def is_owner(update):
    return update.effective_user.id == OWNER_ID

def create_wallet():

    acct = Account.create()

    encrypted = cipher.encrypt(acct.key.hex().encode())

    data = {
        "address":acct.address,
        "private":encrypted.decode()
    }

    json.dump(data,open(WALLET_FILE,"w"))

    return acct.address

def load_wallet():

    if not os.path.exists(WALLET_FILE):
        return None

    data=json.load(open(WALLET_FILE))

    private=cipher.decrypt(data["private"].encode()).decode()

    return data["address"],private


def menu():

    keyboard=[
        [
            InlineKeyboardButton("📬 Address",callback_data="address"),
            InlineKeyboardButton("💰 Balance",callback_data="balance")
        ],
        [
            InlineKeyboardButton("💵 USDT",callback_data="usdt"),
            InlineKeyboardButton("📤 Send",callback_data="send")
        ],
        [
            InlineKeyboardButton("🧾 TX Lookup",callback_data="tx")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        return

    await update.message.reply_text(
        "🚀 Ultra Crypto Wallet",
        reply_markup=menu()
    )


async def button(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query=update.callback_query
    await query.answer()

    wallet=load_wallet()

    if not wallet and query.data!="create":
        await query.edit_message_text("Create wallet first with /create")
        return

    address,private = wallet if wallet else (None,None)

    if query.data=="address":

        await query.edit_message_text(f"📬 Address:\n{address}")

    elif query.data=="balance":

        balance=web3.eth.get_balance(address)
        eth=web3.from_wei(balance,"ether")

        await query.edit_message_text(f"💰 Balance:\n{eth} ETH")

    elif query.data=="usdt":

        contract=web3.eth.contract(address=USDT_ADDRESS,abi=ERC20_ABI)

        bal=contract.functions.balanceOf(address).call()

        await query.edit_message_text(f"💵 USDT:\n{bal/1e6}")

    elif query.data=="send":

        await query.edit_message_text(
            "Send command:\n/send ADDRESS AMOUNT"
        )

    elif query.data=="tx":

        await query.edit_message_text(
            "Lookup transaction:\n/tx HASH"
        )


async def create(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        return

    if os.path.exists(WALLET_FILE):

        await update.message.reply_text("Wallet already exists")

        return

    addr=create_wallet()

    await update.message.reply_text(f"Wallet created:\n{addr}")


async def send(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        return

    wallet=load_wallet()

    if not wallet:
        await update.message.reply_text("Create wallet first")
        return

    try:

        to=context.args[0]
        amount=float(context.args[1])

    except:

        await update.message.reply_text("Usage: /send ADDRESS AMOUNT")
        return

    address,private=wallet

    nonce=web3.eth.get_transaction_count(address)

    tx={
        "nonce":nonce,
        "to":to,
        "value":web3.to_wei(amount,"ether"),
        "gas":21000,
        "gasPrice":web3.to_wei("20","gwei"),
    }

    signed=web3.eth.account.sign_transaction(tx,private)

    tx_hash=web3.eth.send_raw_transaction(signed.rawTransaction)

    await update.message.reply_text(f"TX Sent:\n{tx_hash.hex()}")


async def tx(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        return

    if not context.args:
        await update.message.reply_text("Usage: /tx HASH")
        return

    tx=web3.eth.get_transaction(context.args[0])

    await update.message.reply_text(str(tx))


app=ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("create",create))
app.add_handler(CommandHandler("send",send))
app.add_handler(CommandHandler("tx",tx))
app.add_handler(CallbackQueryHandler(button))

print("Ultra Wallet Bot Running")

app.run_polling()
