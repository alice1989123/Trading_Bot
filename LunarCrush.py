from lunarcrush import LunarCrush

lc = LunarCrush()

eth_1_year_data = lc.get_assets(symbol=['ETH'],
                                data_points=365, interval='day')

print (eth_1_year_data) 