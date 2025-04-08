ContextInfo.get_full_tick - 获取全推数据
不能用于回测 只能取最新的分笔，不能取历史分笔
ContextInfo.get_full_tick(stock_code=[])
stock_code	合约代码列表，如['600000.SH','600036.SH']，不指定时为当前主图合约。

示例
# coding:gbk
import pandas as pd
import numpy as np

def init(C):
	C.stock_list = ["000001.SZ","600519.SH", "510050.SH"]
	
def handlebar(C):
	tick = C.get_full_tick(C.stock_list)
	print(tick["510050.SH"])

预期返回值格式：
{'timetag': '20231106 15:00:04', 'lastPrice': 2.533, 'open': 2.528, 'high': 2.5380000000000003, 'low': 2.521, 'lastClose': 2.513, 'amount': 1442588037.0, 'volume': 5701929, 'pvolume': 5701929, 'stockStatus': 5, 'openInt': 15, 'settlementPrice': 0.0, 'lastSettlementPrice': 0.0, 'askPrice': [2.533, 2.5340000000000003, 2.535, 2.536, 2.537], 'bidPrice': [2.532, 2.531, 2.5300000000000002, 2.529, 2.528], 'askVol': [2615, 19753, 24334, 16932, 35835], 'bidVol': [5662, 24808, 11876, 11472, 14966]}
