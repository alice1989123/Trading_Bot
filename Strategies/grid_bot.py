import copy
import math
import Utils

class gridStrategie:

    def __init__(self, percental_distribution , steps , min_Notational , min_order_quantity) :
        self.percental_distribution = percental_distribution
        self.steps = steps
        self.min_Notational = min_Notational
        self.min_order_quantity = min_order_quantity
     

    def strategie  (self , activeOrders, wallet,  indicadoranalysis  ):        #Use a internal wallet to construct the transactions and be sure the strategie does not do silly stuff.. but the wallet update is donde by the Wallet Updater
        
        wallet_ = copy.deepcopy(wallet) 

        estimated_buys = min( math.floor(  wallet_['quoteAsset']['free'] / self.min_Notational #TODO: fixed minNominal! see how to correct it  this may be higher it minbid is higher
        ) , self.steps ) 
        estimated_sells = min( math.floor(  wallet_['baseAsset']['free'] / self.min_order_quantity #TODO: fixed minNominal! see how to correct it  this may be higher it minbid is higher
        ) , self.steps ) 
        buys =[]
        for i in range ( self.steps): 
            if  wallet_['quoteAsset']['free'] < self.min_Notational:
                break 
            print(wallet_['quoteAsset']['free'] , self.min_Notational )            
            bid_price =  Utils.fix_decimals_price( indicadoranalysis['actual_price']*(1 - self.percental_distribution*(i +1 /self.steps )) )
            quantity =  Utils.fix_decimals_quantity( bid_price , (wallet['quoteAsset']['free'] / estimated_buys)/bid_price)
            print( wallet_["quoteAsset"]['free'] , bid_price*quantity )
            if wallet_["quoteAsset"]['free'] - bid_price*quantity < 0:
                break
            else:            
                buys.append ({'id':i +1 , 'price': bid_price , 'quantity': quantity , 'side':"BUY",  'type':"LIMIT"} )            
                wallet_["quoteAsset"]['free']= wallet_["quoteAsset"]['free'] - bid_price*quantity
                wallet_["quoteAsset" ]["locked"] = wallet_["quoteAsset" ]["locked"] + bid_price*quantity

        sells =[]
        for i in range ( self.steps): 
            if  wallet_['baseAsset']['free'] < self.min_order_quantity:
                break             
            ask_price =  Utils.fix_decimals_price( indicadoranalysis['actual_price']*(1 + self.percental_distribution*(i +1/self.steps )) )
            quantity =  Utils.fix_decimals_quantity( ask_price , (wallet['baseAsset']['free'] / estimated_sells))
            if wallet_["baseAsset"]['free'] - quantity < 0 :
                break
            else:
                sells.append ({'id':- (i+1) , 'price': ask_price , 'quantity': quantity , 'side':"SELL",  'type':"LIMIT"})            
                wallet_["baseAsset"]['free']= wallet_["baseAsset"]['free'] - quantity
                wallet_["baseAsset" ]["locked"] = wallet_["baseAsset" ]["locked"] + quantity


        
        return buys + sells      
