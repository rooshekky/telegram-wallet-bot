import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

ETH_RPC = os.getenv("ETH_RPC")
POLYGON_RPC = os.getenv("POLYGON_RPC")
BSC_RPC = os.getenv("BSC_RPC")
SOL_RPC = os.getenv("SOL_RPC")
