import pandas as pd
from config import symbol
from Client import client
import talib
import math
import Utils
import numpy as np
from Utils import filter
import copy
import Strategies.grid_bot




import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


mpl.style.use('seaborn')




import Utils
import pandas as pd
testdays= 100


df = pd.read_csv('./{}klines_{}.csv'.format(symbol,testdays))
df = df.iloc[: , 1:]



testWallet = {'baseAsset': {'asset': 'SOL', 'free': '3', 'locked': '0.00000000'}, 'quoteAsset': {'asset': 'BNB', 'free': '10', 'locked': '0.00000000'}}

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

steps=20
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



#newWallet = walletUpdater( newOrders , wallet)
#print( wallet ,newOrders , newWallet )

def exchangeResponse (orders , wallet , enviroment):
    actual_price = enviroment.iloc[-1]["Close"]
    #print(orders)
    #print(actual_price)

    orders_ = copy.deepcopy(orders)
    wallet_ = copy.deepcopy(wallet)
    buyorders= filter( orders_ , lambda x: x['side'] == "BUY" )
    sellOrders = filter( orders_ , lambda x: x['side'] == "SELL" )
    fillBuys =  filter(buyorders , lambda x: x['price'] >= actual_price)
    if len(fillBuys) > 0:
        print('a buy!')
    fillSells = filter(sellOrders , lambda x: x['price'] <= actual_price)
    if len(fillSells) > 0:
        print('a sell!')
    for buy in fillBuys:
        wallet_['baseAsset']['free'] = wallet_['baseAsset']['free'] + buy['quantity']
        wallet_['quoteAsset']['locked'] = wallet_['quoteAsset']['locked'] - buy['quantity']*buy['price']
        orders_.remove(buy)
    for sell in fillSells:
        wallet_['baseAsset']['locked'] = wallet_['baseAsset']['locked'] - sell['quantity']
        wallet_['quoteAsset']['free'] = wallet_['quoteAsset']['free'] + sell["price"] * sell['quantity']
        orders_.remove(sell)
    return     orders_ , wallet_
    
     
        


 




def BotAction ( orders, wallet , strategie , enviroment) :

    actual_price = enviroment.iloc[-1]["Close"]
    newOrders = strategie( orders ,  wallet_float(wallet), {"actual_price":actual_price} ) 
    orders_ = OrderUpdater(orders , newOrders)
    wallet = walletUpdater(orders_ , wallet )
    return   orders_,  wallet 

    #print ( exchangeResponse( wallet , orders  ,  df.iloc[windowSize*j+1: windowSize*j+1+50] ))



#print(wallet_ , newOrders , walletUpdater( newOrders , wallet_ ))

def walletValue(wallet , price):
    return(
   float( (wallet['baseAsset']['locked'] + wallet['baseAsset']['free']) )* price 
    + float((wallet['quoteAsset']['locked'] +     wallet['quoteAsset']['free'])))




def enviromentGenerator(slot,  df ):
    return df.iloc[: slot]

def BacktesterRuner( initialWallet , df  , stategie , windowSize=50):
    orders = [] 
    wallet = initialWallet
    for i in range(  windowSize , windowSize +3  #df.size 
    ):   
        
        actual_price = enviromentGenerator(i, df ).iloc[-1]["Close"]
        #print( walletValue (wallet , actual_price )  )
        [orders , wallet] = BotAction (orders , wallet , stategie , enviromentGenerator(i, df ) )
        print( wallet)
     
        [orders,wallet ]= exchangeResponse(orders ,wallet , enviromentGenerator(i+1 , df ) )



wallet = Utils.wallet ( )
orders = client.get_open_orders()


gb= Strategies.grid_bot.gridStrategie(0.020,30,min_Notational , min_order_quantity)


""" print(  enviromentGenerator(50, df ) )
 """
BacktesterRuner(testWallet , df , gb.strategie  )



""" print ( enviromentGenerator(1 ,50 , df )  ) 


print (BotAction (orders , testWallet , enviromentGenerator(1 ,50 , df ) )) """