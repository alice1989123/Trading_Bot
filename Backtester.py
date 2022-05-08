import pandas as pd
from config import symbol
from Client import client
import talib
import math
import Utils
import numpy as np
from Utils import filter
import copy




import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


mpl.style.use('seaborn')




import Utils
import pandas as pd
testdays= 100


df = pd.read_csv('./{}klines_{}.csv'.format(symbol,testdays))
df = df.iloc[: , 1:]





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

steps=2
percental_distribution = 0.1


def walletUpdater(   orders, wallet ):   # given the orders to do it updates the wallet in accordance

    wallet_ = copy.deepcopy(wallet) 

    buyorders= filter( orders , lambda x: x['side'] == "BUY" )
    sellOrders = filter( orders , lambda x: x['side'] == "SELL" )
    for order in buyorders:
        wallet_['quoteAsset']['free'] = wallet_['quoteAsset']['free'] - order['price']*order['quantity']
        wallet_ ['quoteAsset' ]['locked'] = wallet_['quoteAsset']['locked'] + order['price']*order['quantity']
    
    for order in sellOrders : 
        wallet_['baseAsset']['free'] = wallet_['baseAsset']['free'] - order['quantity']
        wallet_ ['baseAsset' ]['locked'] = wallet_['baseAsset']['locked'] + order['quantity']
        

    return wallet_
def OrderUpdater ( orders , newOrders  ): # TODO: When cancelling orders is added it should be handled acordingly 
    return orders + newOrders


def wallet_float (wallet ):
    wallet['baseAsset']['free'] = float ( wallet['baseAsset']['free'])
    wallet['baseAsset']['locked'] = float ( wallet['baseAsset']['locked'])
    wallet['quoteAsset']['free'] = float ( wallet['quoteAsset']['free'])
    wallet['quoteAsset']['locked'] = float ( wallet['quoteAsset']['locked'])   

    return (wallet)
wallet = Utils.wallet ( )
orders = client.get_open_orders()

def gridStrategie  (activeOrders, wallet, indicadoranalysis={'none'}):


        #Use a internal wallet to construct the transactions and be sure the strategie does not do silly stuff.. but the wallet update is donde by the Wallet Updater
         
        wallet_ = copy.deepcopy(wallet) 

        estimated_buys = min( math.floor(  wallet_['quoteAsset']['free'] / min_Notational #TODO: fixed minNominal! see how to correct it  this may be higher it minbid is higher
        ) , steps ) 
        estimated_sells = min( math.floor(  wallet_['baseAsset']['free'] / min_order_quantity #TODO: fixed minNominal! see how to correct it  this may be higher it minbid is higher
        ) , steps ) 
        buys =[]
        for i in range ( steps): 
            if  wallet_['quoteAsset']['free'] < min_Notational:
                break             
            bid_price =  Utils.fix_decimals_price( indicadoranalysis['actual_price']*(1 - 0.02*(i +1 /steps )) )
            quantity =  Utils.fix_decimals_quantity( bid_price , (wallet['quoteAsset']['free'] / estimated_buys)/bid_price)
            if wallet_["quoteAsset"]['free'] - bid_price*quantity < 0:
                break
            else:            
                buys.append ({'id':i +1 , 'price': bid_price , 'quantity': quantity , 'side':"BUY",  'type':"LIMIT"} )            
                wallet_["quoteAsset"]['free']= wallet_["quoteAsset"]['free'] - bid_price*quantity
                wallet_["quoteAsset" ]["locked"] = wallet_["quoteAsset" ]["locked"] + bid_price*quantity

        sells =[]
        for i in range ( steps): 
            if  wallet_['baseAsset']['free'] < min_order_quantity:
                break             
            ask_price =  Utils.fix_decimals_price( indicadoranalysis['actual_price']*(1 + 0.02*(i +1/steps )) )
            quantity =  Utils.fix_decimals_quantity( ask_price , (wallet['baseAsset']['free'] / estimated_sells))
            if wallet_["baseAsset"]['free'] - quantity < 0 :
                break
            else:
                sells.append ({'id':- (i+1) , 'price': ask_price , 'quantity': quantity , 'side':"SELL",  'type':"LIMIT"})            
                wallet_["baseAsset"]['free']= wallet_["baseAsset"]['free'] - quantity
                wallet_["baseAsset" ]["locked"] = wallet_["baseAsset" ]["locked"] + quantity

        
        return buys + sells      


#newWallet = walletUpdater( newOrders , wallet)
#print( wallet ,newOrders , newWallet )
windowSize = 50

def exchangeResponse (orders , wallet , event):
    orders_ = copy.deepcopy(orders)
    wallet_ = copy.deepcopy(wallet)
    actual_price = event.iloc[-1]["Close"]
    buyorders= filter( orders_ , lambda x: x['side'] == "BUY" )
    sellOrders = filter( orders_ , lambda x: x['side'] == "SELL" )
    fillBuys =  filter(buyorders , lambda x: x['price'] >= actual_price)
    fillSells = filter(sellOrders , lambda x: x['price'] <= actual_price)
    for buy in fillBuys:
        wallet_['baseAsset']['free'] = wallet_['baseAsset']['free'] + buy['quantity']
        wallet_['quoteAsset']['locked'] = wallet_['quoteAsset']['locked'] - buy['quantity']*buy['price']
        orders_.remove(buy)
    for sell in fillSells:
        wallet_['baseAsset']['locked'] = wallet_['baseAsset']['locked'] - sell['quantity']
        wallet_['quoteAsset']['free'] = wallet_['quoteAsset']['free'] + sell["price"] * sell['price']
        orders_.remove(sell)
    return  orders_ , wallet_
    

        
        

 



for j in range (  1
    #int( round( df.size /windowSize))
    ):

    event = df.iloc[windowSize*j: windowSize*j+50]
    actualprice = windowSize*j

    wallet = {'baseAsset': {'asset': 'SOL', 'free': 0, 'locked': 0.0}, 'quoteAsset': {'asset': 'BNB', 'free': 10, 'locked': 0.0}}
    orders = []
    actual_price = event.iloc[-1]["Close"]
    newOrders = gridStrategie( orders ,  wallet_float(wallet), {"actual_price":actual_price} ) 
    orders = OrderUpdater(orders , newOrders)
    wallet = walletUpdater(orders , wallet )
    print ( exchangeResponse( wallet , orders  ,  df.iloc[windowSize*j+1: windowSize*j+1+50] ))




#print(wallet_ , newOrders , walletUpdater( newOrders , wallet_ ))

