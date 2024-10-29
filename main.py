from pathlib import Path
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    EXCHANGE = os.getenv('EXCHANGE', 'binance')
    TRADING_PAIR = os.getenv('TRADING_PAIR', 'USDT/USDC')
    LEVERAGE = int(os.getenv('LEVERAGE', '3'))
    POSITION_SIZE = float(os.getenv('POSITION_SIZE', '10'))
    LONG_ENTRY_THRESHOLD = float(os.getenv('LONG_ENTRY_THRESHOLD', '0.9993'))
    SHORT_ENTRY_THRESHOLD = float(os.getenv('SHORT_ENTRY_THRESHOLD', '1.0001'))
    EXIT_THRESHOLD = float(os.getenv('EXIT_THRESHOLD', '1.0000'))
    SLEEP_TIME = int(os.getenv('SLEEP_TIME', '1'))

