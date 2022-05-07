from cmath import log
import math
from Client import client
from config import symbol

symbol_info = client.get_symbol_info(symbol)
baseAsset = symbol_info['baseAsset']
quoteAsset = symbol_info['quoteAsset']


wallet = { 'baseAsset':client.get_asset_balance(asset=baseAsset) ,  "quoteAsset" : client.get_asset_balance(asset=quoteAsset) }

orders = client.get_open_orders()


def round_up(n, decimals):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def  fix_decimals_price (price ):  
  tickSize =   tickSize = float(symbol_info['filters'][0]['tickSize'])   
  return round_up(   n=price  ,  decimals=  round(-  log( tickSize ,10).real)) 
def  fix_decimals_quantity (price, quantity  ):  
  minquantity = float(symbol_info['filters'][2]['minQty'])
  minNotational = float ( symbol_info['filters'][3]['minNotional'])
  stepSize = float( symbol_info['filters'][2]['stepSize'])
  min_quantity_takinNotational = max( minquantity ,  float( minNotational) / price )
  return  round_up( n =  max ( quantity , min_quantity_takinNotational )  ,  decimals=  round(-  log( stepSize ,10).real))
