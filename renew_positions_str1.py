# -*- coding: utf-8 -*-
"""
基于波动的持仓优化策略
策略目标：利用周期内股价的波动，低点买入，高点时卖出，降低持仓成本，赚取收益
策略假设：选中的股票中长线稳健向上
"""

class MyStock:
    """股票类，包含股票的基本信息和交易参数"""
    def __init__(self, code, related_industry_codes=None):
        self.code = code                      # 股票代码
        self.related_industry_codes = related_industry_codes or []  # 相关行业代码
        self.buy_threshold = 0.95             # 下跌买入阈值（默认0.95）
        self.sell_threshold = 1.05            # 上涨卖出阈值（默认1.05)
        self.current_position = 0             # 当前持仓数量
        self.cost_price = 0                   # 成本价
        self.max_position = 1000              # 最大持仓数量（默认1000）
        self.min_position = 200               # 最小市场数量（默认200）
        self.single_buy_amount = 100          # 单次买入额度，默认100


def init_mystock(C, code_list):
    """
    初始化股票对象
    
    Args:
        C: 全局上下文
        code_list: 目标股票代码列表
    
    Returns:
        dict: 股票代码到MyStock对象的映射
    """
    code2mystock = {}
    
    # 获取当前持仓的股票代码数量和成本价
    positions = C.get_trade_detail_data()
    
    for code in code_list:
        stock = MyStock(code)
        
        # 设置当前持仓数量和成本价（如果有持仓）
        if code in positions:
            stock.current_position = positions[code]['volume']
            stock.cost_price = positions[code]['cost_price']
        
        code2mystock[code] = stock
    
    return code2mystock


def init(C):
    """
    策略初始化函数
    
    Args:
        C: 全局上下文
    """
    # 设置目标股票代码
    target_codes = ['832491.BJ', '832522.BJ']
    
    # 初始化股票对象
    C.code2mystock = init_mystock(C, target_codes)
    
    # 定义相关股票列表：目标代码 + BJ50指数 + 相关行业代码
    C.related_stocks = target_codes.copy() + ['899050.BJ']
    # 添加所有股票的相关行业代码
    for stock in C.code2mystock.values():
        C.related_stocks.extend(stock.related_industry_codes)
    C.related_stocks = list(set(C.related_stocks))
    
    # 获取过去10天收盘价
    C.code2avg = {}
    for code in C.related_stocks:
        history_data = C.download_history_data( code, fields=['close'], start_time=None, end_time=None, 
            period='1d'
        )
        close_prices = [data['close'] for data in history_data]
        # 计算10天收盘价均值
        C.code2avg[code] = sum(close_prices) / len(close_prices) if close_prices else 0


def calculate_industry_status(ticks, related_industry_codes):
    """
    计算行业相关股票的涨跌状态
    Args:
        ticks: 所有股票的实时行情
        related_industry_codes: 特定股票的相关行业代码列表
    Returns:
        tuple: (industry_bad, industry_rise_percent) 行业是否有严重下跌的股票，行业平均涨幅
    """
    industry_bad = False
    industry_rise_percent = 0
    industry_count = 0
    
    for code in related_industry_codes:
        tick = ticks.get(code)
        if not tick:
            continue
        # 计算涨跌幅
        rise_percent = (tick['last_price'] / tick['open_price'] - 1) * 100
        industry_rise_percent += rise_percent
        industry_count += 1
        
        if rise_percent < -5:
            industry_bad = True
            break
    # 计算行业平均涨幅
    if industry_count > 0:
        industry_rise_percent /= industry_count
        
    return industry_bad, industry_rise_percent

def handlebar(C):
    """
    策略主函数，每个周期调用一次
    
    Args:
        C: 全局上下文
    """
    # 获取所有related_stocks代码实时行情
    ticks = C.get_full_tick(C.related_stocks)
    
    # 获取BJ50指数行情，代表大盘行情
    bj50_tick = ticks.get('899050.BJ')
    if not bj50_tick:
        return
    
    # 判断大盘是否向好（当前价格大于开盘价）
    market_good = bj50_tick['lastPrice'] > bj50_tick['open']
    market_rise_percent = (bj50_tick['lastPrice'] / bj50_tick['open'] - 1) * 100
    
    # 对每一个目标代码进行交易决策
    for code, stock in C.code2mystock.items():
        tick = ticks.get(code)
        if not tick:
            continue
        
        # 为当前股票计算行业状态，使用其相关行业代码
        industry_bad, industry_rise_percent = calculate_industry_status(ticks, stock.related_industry_codes)
        
        current_price = tick['last_price']
        
        # 计算相对于10日均值的比例
        avg_price = C.code2avg.get(code, 0)
        avg_ratio = current_price / avg_price if avg_price else 1
        
        # 买入条件：大盘向好，行业没有严重下跌，股票价格低于成本或均值，持仓未满
        if (market_good and not industry_bad and 
            (current_price < stock.cost_price * stock.buy_threshold or 
             avg_ratio < 0.9) and 
            stock.current_position < stock.max_position):
            
            # 计算买入数量
            buy_amount = stock.single_buy_amount
            
            # 执行买入
            C.buy(code, current_price, buy_amount)
            
            # 更新持仓信息
            stock.current_position += buy_amount
            stock.cost_price = ((stock.cost_price * (stock.current_position - buy_amount) + 
                               current_price * buy_amount) / stock.current_position)
            
            # 记录交易日志
            C.log(f"买入 {code}: 价格={current_price}, 数量={buy_amount}, 新持仓={stock.current_position}, 新成本={stock.cost_price}")
        
        # 卖出条件：大盘涨幅小，行业涨幅小，股票价格高于成本或均值，持仓充足
        elif (market_rise_percent < 2 and industry_rise_percent < 5 and 
              (current_price > stock.cost_price * stock.sell_threshold or 
               avg_ratio > 1.2) and 
              stock.current_position > stock.min_position):
            
            # 计算卖出数量
            sell_amount = stock.single_buy_amount
            
            # 确保不会卖出超过持仓量
            sell_amount = min(sell_amount, stock.current_position - stock.min_position)
            
            if sell_amount > 0:
                # 执行卖出
                C.sell(code, current_price, sell_amount)
                
                # 更新持仓信息
                stock.current_position -= sell_amount
                
                # 记录交易日志
                C.log(f"卖出 {code}: 价格={current_price}, 数量={sell_amount}, 新持仓={stock.current_position}")