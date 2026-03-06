import os
from dotenv import load_dotenv

load_dotenv()

ETH_RPC = os.getenv("ETH_RPC")
POLYGON_RPC = os.getenv("POLYGON_RPC")
BSC_RPC = os.getenv("BSC_RPC")
SOL_RPC = os.getenv("SOL_RPC")
