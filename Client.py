from binance.client import Client
import os 
from dotenv import load_dotenv


#os.getenv("API_BINANCE")


API_KEY =  os.getenv("API_KEY") 
API_SECRET =  os.getenv("API_SECRET") 

client = Client(API_KEY, API_SECRET )

