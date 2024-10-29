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

# logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name):
    # Créer le dossier logs s'il n'existe pas
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Handler pour fichier
    file_handler = RotatingFileHandler(
        'logs/trading_bot.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))

    # Handler pour console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# trading_bot.py
from config import Config
from logger import setup_logger
import ccxt
from decimal import Decimal
import time

logger = setup_logger('trading_bot')

class StablecoinTradingBot:
    def __init__(self):
        self.config = Config()
        self.exchange = getattr(ccxt, self.config.EXCHANGE)({
            'apiKey': self.config.API_KEY,
            'secret': self.config.API_SECRET,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        self.position = None
        self.logger = logger

    def setup_leverage(self):
        try:
            self.exchange.set_leverage(self.config.LEVERAGE, self.config.TRADING_PAIR)
            self.logger.info(f"Leverage set to {self.config.LEVERAGE}")
        except Exception as e:
            self.logger.error(f"Error setting leverage: {e}")
            raise

    def get_current_price(self):
        try:
            ticker = self.exchange.fetch_ticker(self.config.TRADING_PAIR)
            price = Decimal(str(ticker['last']))
            self.logger.debug(f"Current price: {price}")
            return price
        except Exception as e:
            self.logger.error(f"Error fetching price: {e}")
            raise

    def execute_trade(self, trade_type, amount):
        try:
            if trade_type == 'open_long':
                order = self.exchange.create_market_buy_order(
                    self.config.TRADING_PAIR, 
                    amount
                )
                self.position = 'long'
            elif trade_type == 'close_long':
                order = self.exchange.create_market_sell_order(
                    self.config.TRADING_PAIR, 
                    amount
                )
                self.position = None
            elif trade_type == 'open_short':
                order = self.exchange.create_market_sell_order(
                    self.config.TRADING_PAIR, 
                    amount
                )
                self.position = 'short'
            elif trade_type == 'close_short':
                order = self.exchange.create_market_buy_order(
                    self.config.TRADING_PAIR, 
                    amount
                )
                self.position = None

            self.logger.info(f"Executed {trade_type}: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Error executing {trade_type}: {e}")
            raise

    def run(self):
        self.logger.info("Starting trading bot...")
        self.setup_leverage()
        
        while True:
            try:
                current_price = self.get_current_price()
                
                if self.position is None:
                    if current_price <= Decimal(str(self.config.LONG_ENTRY_THRESHOLD)):
                        self.execute_trade('open_long', self.config.POSITION_SIZE)
                    elif current_price >= Decimal(str(self.config.SHORT_ENTRY_THRESHOLD)):
                        self.execute_trade('open_short', self.config.POSITION_SIZE)
                
                elif self.position == 'long' and current_price >= Decimal(str(self.config.EXIT_THRESHOLD)):
                    self.execute_trade('close_long', self.config.POSITION_SIZE)
                
                elif self.position == 'short' and current_price <= Decimal(str(self.config.EXIT_THRESHOLD)):
                    self.execute_trade('close_short', self.config.POSITION_SIZE)
                
                time.sleep(self.config.SLEEP_TIME)
            
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                time.sleep(10)  # Attendre avant de réessayer



