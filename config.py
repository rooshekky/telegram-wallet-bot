import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8637194920:AAF2rIXKDvsF5NZYKSoVl2CFAVjWmuhD-aQ")
OWNER_ID = int(os.getenv("5255390662"))

ETH_RPC = os.getenv("ETH_RPC")
POLYGON_RPC = os.getenv("POLYGON_RPC")
BSC_RPC = os.getenv("BSC_RPC")
