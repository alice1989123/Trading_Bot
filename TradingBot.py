
from ast import Num
import Utils
from statistics import quantiles
from Client import client
import pandas as pd
from sklearn import preprocessing
import numpy as np
from config import symbol , fee



#tickers = client.get_symbol_ticker()
""" base_price = float(list(filter(lambda c : c["symbol"] == symbol, tickers ))[0]['price'])





   



buy_price =  base_price *(1 - 0.01) 


sell_price =   base_price  * (1 + 0.01)



print ( Utils.fix_decimals_quantity ( buy_price , 0) )
 """



#buy = client.create_order( symbol =symbol,side="BUY",  type="LIMIT" , quantity=  fix_decimals_quantity ( buy_price , 0)  , price = fix_decimals_price(buy_price   )  , timeInForce="GTC" )

#client.cancel_order(symbol =symbol ,orderId= 230060233)

#print(buy)

#print(symbol_info['filters'])




  #df.to_csv('./KlineOneMinteBinance')

#klines = getKlines(symbol)


#df= pd.read_csv('./KlineOneMinteBinance' )

#getKlines()

#trades = client.get_recent_trades(symbol='BNBSOL')
#orders = client.get_all_orders(symbol=symbol, limit=10)




