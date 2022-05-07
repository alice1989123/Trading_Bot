import pandas as pd
from config import symbol
from Client import client
import talib
import math


import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


mpl.style.use('seaborn')




import Utils
import pandas as pd
testdays= 100


df = pd.read_csv('./{}klines_{}.csv'.format(symbol,testdays))




# Add all ta features


 # example_to_plot df = ta.add_all_ta_features(
""" print(df.head())

df["SMA"] = talib.SMA(df.Open ,  timeperiod=100 )
df['winrelative'] = (df["SMA"] - df['Open']) / df['Open'] *100
plt.plot(df[40700: 42000].winrelative , label="relativegains")
plt.title('SMA')
plt.legend()
plt.show()
 """

    





min_Notational = float(Utils.symbol_info["filters"][3]["minNotional"])

frame_time = 1 
initial_portfolio_value = 20
quoteAsset_value =initial_portfolio_value/2
baseAsset_value= initial_portfolio_value / 2  / df["Open"][1000] 
#print( df["Open"].size)
#quoteAsset_token = quoteAsset_value/




max_historicalprice = df['High'].max()
min_order_quantity = Utils.fix_decimals_quantity(max_historicalprice , 0)

# 50 - 20 for buying and 50 for selling, steps distributed over 10% up and 10% down 

steps=50
percental_distribution = 0.1


orders = [{'symbol': 'SOLBNB', 'orderId': 230370261, 'orderListId': -1, 'clientOrderId': 'RhwU16BsXKd6DCtemnGpKD', 'price': '0.20000000', 'origQty': '0.50000000', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1651934533000, 'updateTime': 1651934533000, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}]

wallet = {'baseAsset': {'asset': 'SOL', 'free': '0.00000000', 'locked': '0.00000000'}, 'quoteAsset': {'asset': 'BNB', 'free': '1.28052742', 'locked': '0.10000000'}}

def strategieValidation(  Strategie  , wallet , orders ):   # It validates if the propoused move is in valid

    newOrders = Strategie ( orders , wallet  )


    return 

def wallet_float (wallet ):
    wallet['baseAsset']['free'] = float ( wallet['baseAsset']['free'])
    wallet['baseAsset']['locked'] = float ( wallet['baseAsset']['locked'])
    wallet['quoteAsset']['free'] = float ( wallet['quoteAsset']['free'])
    wallet['quoteAsset']['locked'] = float ( wallet['quoteAsset']['locked'])   

    return (wallet)

wallet_float(wallet )

def gridStrategie  (activeOrders, wallet, indicadoranalysis={'none'}):
        print( wallet)
        
        estimated_buys = min( math.floor(  wallet['quoteAsset']['free'] / min_Notational #TODO: fixed minNominal! see how to correct it  this may be higher it minbid is higher
        ) , steps ) 
        estimated_sells = min( math.floor(  wallet['baseAsset']['free'] / min_order_quantity #TODO: fixed minNominal! see how to correct it  this may be higher it minbid is higher
        ) , steps ) 
        buys =[]
        for i in range ( steps): 
            if  wallet['quoteAsset']['free'] < min_Notational:
                break             
            bid_price =  Utils.fix_decimals_price( indicadoranalysis['actual_price']*(1 - 0.1*(i/steps )) )
            quantity =  Utils.fix_decimals_quantity( bid_price , bid_price * (wallet['quoteAsset']['free'] / estimated_buys))
            if wallet["quoteAsset"]['free'] - bid_price*quantity < 0:
                break
            else:            
                buys.append ({'id':i , 'price': bid_price , 'quantity': quantity})            
                wallet["quoteAsset"]['free']= wallet["quoteAsset"]['free'] - bid_price*quantity

        sells =[]
        for i in range ( steps): 
            if  wallet['baseAsset']['free'] < min_order_quantity:
                break             
            ask_price =  Utils.fix_decimals_price( indicadoranalysis['actual_price']*(1 + 0.1*(i/steps )) )
            quantity =  Utils.fix_decimals_quantity( ask_price , (wallet['baseAsset']['free'] / estimated_sells))
            if wallet["baseAsset"]['free'] - quantity < 0 :
                break
            else:
                sells.append ({'id':-i , 'price': bid_price , 'quantity': quantity})            
                wallet["baseAsset"]['free']= wallet["baseAsset"] - quantity
        
        return( wallet ,  {"buy_orders": buys , "sell_orders":sells } )


print(


gridStrategie(  orders  , wallet_float(wallet ) , {"actual_price":0.2} ) 


)