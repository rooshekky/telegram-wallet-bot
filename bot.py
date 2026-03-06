from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from config import BOT_TOKEN, OWNER_ID
from wallet import create_wallet, load_wallet
from evm_chains import CHAINS, get_balances
from solana_chain import create_sol_wallet, load_sol_wallet, get_sol_balance


def is_owner(update):

    return update.effective_user.id == OWNER_ID


def main_menu():

    keyboard = [
        [
            InlineKeyboardButton("EVM Address", callback_data="address"),
            InlineKeyboardButton("EVM Balances", callback_data="balances")
        ],
        [
            InlineKeyboardButton("SOL Address", callback_data="sol_address"),
            InlineKeyboardButton("SOL Balance", callback_data="sol_balance")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        return

    await update.message.reply_text(
        "Multi-Chain Wallet Bot",
        reply_markup=main_menu()
    )


async def create(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        return

    address = create_wallet()

    await update.message.reply_text(f"EVM wallet created:\n{address}")


async def create_sol(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        return

    address = create_sol_wallet()

    await update.message.reply_text(f"SOL wallet created:\n{address}")


async def send(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        return

    wallet = load_wallet()

    if not wallet:
        await update.message.reply_text("Create EVM wallet first")
        return

    try:

        chain = context.args[0]
        to = context.args[1]
        amount = float(context.args[2])

    except:

        await update.message.reply_text("Usage:\n/send chain address amount")
        return

    web3 = CHAINS.get(chain)

    if not web3:

        await update.message.reply_text("Invalid chain")
        return

    address, private = wallet

    nonce = web3.eth.get_transaction_count(address)

    tx = {
        "nonce": nonce,
        "to": to,
        "value": web3.to_wei(amount, "ether"),
        "gas": 21000,
        "gasPrice": web3.eth.gas_price
    }

    signed = web3.eth.account.sign_transaction(tx, private)

    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)

    await update.message.reply_text(f"TX sent:\n{tx_hash.hex()}")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "address":

        wallet = load_wallet()

        if not wallet:
            await query.edit_message_text("Create EVM wallet with /create")
            return

        address, _ = wallet

        await query.edit_message_text(address)

    elif query.data == "balances":

        wallet = load_wallet()

        if not wallet:
            await query.edit_message_text("Create EVM wallet with /create")
            return

        address, _ = wallet

        balances = get_balances(address)

        msg = "\n".join([f"{k}: {v}" for k, v in balances.items()])

        await query.edit_message_text(msg)

    elif query.data == "sol_address":

        wallet = load_sol_wallet()

        if not wallet:
            await query.edit_message_text("Create SOL wallet with /create_sol")
            return

        address, _ = wallet

        await query.edit_message_text(address)

    elif query.data == "sol_balance":

        wallet = load_sol_wallet()

        if not wallet:
            await query.edit_message_text("Create SOL wallet with /create_sol")
            return

        address, _ = wallet

        balance = get_sol_balance(address)

        await query.edit_message_text(f"{balance} SOL")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("create", create))
app.add_handler(CommandHandler("create_sol", create_sol))
app.add_handler(CommandHandler("send", send))
app.add_handler(CallbackQueryHandler(button))

print("Wallet bot running")

app.run_polling()
