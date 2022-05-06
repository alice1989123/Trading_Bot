
from binance.client import Client
from Client import client
import pandas as pd
from config import symbol


def getKlines(symbol,testdays):



  klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "{} day ago UTC".format(testdays))

  df=pd.DataFrame(klines )

  df = df[df.columns[1:6]]

  df.columns=["Open","High", "Low", "Close" , "Volume"]

  df.to_csv("./{}klines_{}.csv".format(symbol,testdays))

#getKlines(symbol,testdays)