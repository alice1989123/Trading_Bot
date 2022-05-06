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

    




baseAsset = Utils.symbol_info['baseAsset']
quoteAsset = Utils.symbol_info['quoteAsset']
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

def gridStrategie  (activeOrders, availableFunds, indicadoranalysis={'none'}):
        estimated_buys = min( math.floor(  availableFunds['quoteAsset'] / min_Notational #TODO: fixed minNominal! see how to correct it  this may be higher it minbid is higher
        ) , steps ) 
        estimated_sells = min( math.floor(  availableFunds['baseAsset'] / min_order_quantity #TODO: fixed minNominal! see how to correct it  this may be higher it minbid is higher
        ) , steps ) 
        buys =[]
        for i in range ( steps): 
            if  availableFunds['quoteAsset'] < min_Notational:
                break             
            bid_price =  Utils.fix_decimals_price( indicadoranalysis['actual_price']*(1 - 0.1*(i/steps )) )
            quantity =  Utils.fix_decimals_quantity( bid_price , bid_price * (availableFunds['quoteAsset'] / estimated_buys))
            if availableFunds["quoteAsset"] - bid_price*quantity < 0:
                break
            else:            
                buys.append ({'id':i , 'price': bid_price , 'quantity': quantity})            
                availableFunds["quoteAsset"]= availableFunds["quoteAsset"] - bid_price*quantity

        sells =[]
        for i in range ( steps): 
            if  availableFunds['baseAsset'] < min_order_quantity:
                break             
            ask_price =  Utils.fix_decimals_price( indicadoranalysis['actual_price']*(1 + 0.1*(i/steps )) )
            quantity =  Utils.fix_decimals_quantity( ask_price , (availableFunds['baseAsset'] / estimated_sells))
            if availableFunds["baseAsset"] - quantity < 0 :
                break
            else:
                sells.append ({'id':-i , 'price': bid_price , 'quantity': quantity})            
                availableFunds["baseAsset"]= availableFunds["baseAsset"] - quantity
        
        return( availableFunds ,  {"buy_orders": buys , "sell_orders":sells } )


print(


gridStrategie(  "activeOrders"  , {"baseAsset":0 , 'quoteAsset':1 }   , {"actual_price":0.2} ) 


)