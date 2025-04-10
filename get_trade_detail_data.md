get_trade_detail_data-查询账号资金信息、委托记录等
get_trade_detail_data(accountID, strAccountType, strDatatype) 可以查询持仓，委托，交易，账号等信息

调用方法 get_trade_detail_data(accountID, strAccountType, strDatatype, strategyName)时，通过strategyName来区分不同的策略标记

示例代码

#coding:gbk

account = '800174' # 在策略交易界面运行时，account的值会被赋值为策略配置中的账号，编辑器界面运行时，需要手动赋值；编译器环境里执行的下单函数不会产生实际委托

def init(ContextInfo):
    pass

def handlebar(ContextInfo):
    if not ContextInfo.is_last_bar():
        return
    
    orders = get_trade_detail_data(account, 'stock', 'order')
    print('查询委托结果：')
    for o in orders:
        print(f'股票代码: {o.m_strInstrumentID}, 市场类型: {o.m_strExchangeID}, 证券名称: {o.m_strInstrumentName}, 买卖方向: {o.m_nOffsetFlag}',
        f'委托数量: {o.m_nVolumeTotalOriginal}, 成交均价: {o.m_dTradedPrice}, 成交数量: {o.m_nVolumeTraded}, 成交金额:{o.m_dTradeAmount}')


    deals = get_trade_detail_data(account, 'stock', 'deal')
    print('查询成交结果：')
    for dt in deals:
        print(f'股票代码: {dt.m_strInstrumentID}, 市场类型: {dt.m_strExchangeID}, 证券名称: {dt.m_strInstrumentName}, 买卖方向: {dt.m_nOffsetFlag}', 
        f'成交价格: {dt.m_dPrice}, 成交数量: {dt.m_nVolume}, 成交金额: {dt.m_dTradeAmount}')

    positions = get_trade_detail_data(account, 'stock', 'position')
    print('查询持仓结果：')
    for dt in positions:
        print(f'股票代码: {dt.m_strInstrumentID}, 市场类型: {dt.m_strExchangeID}, 证券名称: {dt.m_strInstrumentName}, 持仓量: {dt.m_nVolume}, 可用数量: {dt.m_nCanUseVolume}',
        f'成本价: {dt.m_dOpenPrice:.2f}, 市值: {dt.m_dInstrumentValue:.2f}, 持仓成本: {dt.m_dPositionCost:.2f}, 盈亏: {dt.m_dPositionProfit:.2f}')


    accounts = get_trade_detail_data(account, 'stock', 'account')
    print('查询账号结果：')
    for dt in accounts:
        print(f'总资产: {dt.m_dBalance:.2f}, 净资产: {dt.m_dAssureAsset:.2f}, 总市值: {dt.m_dInstrumentValue:.2f}', 
        f'总负债: {dt.m_dTotalDebit:.2f}, 可用金额: {dt.m_dAvailable:.2f}, 盈亏: {dt.m_dPositionProfit:.2f}')
    
    position_statistics = get_trade_detail_data(account,"FUTURE",'POSITION_STATISTICS')
    for obj in position_statistics:
        if obj.m_nDirection == 49:
			continue
		PositionInfo_dict[obj.m_strInstrumentID+"."+obj.m_strExchangeID]={
		"持仓":obj.m_nPosition,
		"成本":obj.m_dPositionCost,
		"浮动盈亏":obj.m_dFloatProfit,
		"保证金占用":obj.m_dUsedMargin
		}
	print(PositionInfo_dict)

	
