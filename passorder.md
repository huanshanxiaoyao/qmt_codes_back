迅投 QMT 中的综合下单函数
综合下单函数，用于股票、期货、期权等下单和新股、新债申购、融资融券等交易操作推荐使用
调用方法
passorder(
    opType, orderType, accountid
    , orderCode, prType, price, volume
    , strategyName, quickTrade, userOrderId
    , ContextInfo
)
'''
passorder(
    2 #opType 操作号
    , 1101 #orderType 组合方式
    , '1000044' #accountid 资金账号
    , 'cu2403.SF' #orderCode 品种代码
    , 14 #prType 报价类型
    , 0.0 #price 价格
    , 2 #volume 下单量
    , '示例下单' #strategyName 策略名称
    , 1 #quickTrade 快速下单标记
    , '投资备注' #userOrderId 投资备注
    , C #ContextInfo 策略上下文
)
'''

示例
#coding:gbk

'''
# 在策略交易界面运行时，account的值会被赋值为策略配置中的账号，编辑器界面运行时，需要手动赋值
# 编译器界面里执行的下单函数不会产生实际委托
'''
account = "test"
def init(ContextInfo):
    pass
def handlebar(ContextInfo):
    if not ContextInfo.is_last_bar():
        return
    # 单股单账号期货最新价买入 10 手，快速下单参数设置为 1
    passorder(0, 1101, account, "rb2405.SF", 5, -1, 10, "示例", 1, "投资备注",ContextInfo)
    
    # 单股单账号期货指定价买入 10 手，快速下单参数设置为 1
    passorder(0, 1101, account,  "rb2405.SF", 11, 3000, 10, "示例", 1, "投资备注",ContextInfo)
    
    # 单股单账号股票最新价买入 100 股（1 手），快速下单参数设置为 1   
    passorder(23, 1101, account, "000001.SZ", 5, 0, 100, "示例", 1, "投资备注",ContextInfo)
    
    # 单股单账号股票指定价买入 100 股（1 手），快速下单参数设置为 1
    passorder(23, 1101, account, "000001.SZ", 11, 7, 100, "示例", 1, "投资备注",ContextInfo)



参数详解：
参数名        | 类型     | 说明              | 提示
-------------|----------|------------------|------------------
opType       | int      | 交易类型          | 可选买、卖，期货开仓、平仓等。可选值参考opType-操作类型
orderType    | int      | 下单方式          | 可选值参考orderType-下单方式。可选按股票数量买卖或按照金额等方式买卖。一、期货不支持 1102 和 1202；二、对所有账号组的操作相当于对账号组里的每个账号做一样的操作
accountID    | string   | 资金账号          | 下单的账号ID（可多个）或账号组名或套利组名（一个篮子一个套利账号，如 accountID = '股票账户名, 期货账号'）
orderCode    | string   | 下单代码          | 1. 如果是单股或单期货、港股，则该参数填合约代码；2. 如果是组合交易, 则该参数填篮子名称；3. 如果是组合套利，则填一个篮子名和一个期货合约名
prType       | int      | 下单选价类型       | 可选值参考prType-下单选价类型。特别的对于套利，这个 prType 只对篮子起作用，期货采用默认的方式
price        | float    | 下单价格          | 一、单股下单时，prType 是模型价/科创板盘后定价时 price 有效；其它情况无效。二、组合下单时，是组合套利时，price 作套利比例有效，其它情况无效
volume       | int      | 下单数量          | 根据 orderType 值最后一位确定 volume 的单位（股/手/元/%），可选值参考volume-下单
strategyName | string   | 自定义策略名       | 用来区分 order 委托和deal 成交来自不同的策略。根据该策略名可获取相应策略名对应的委托或成交集合
quickTrade   | int      | 设定是否立即触发下单 | 可选值参考quicktrade-快速下单。1：非历史bar上立即触发；2：所有情况都立即触发，需谨慎使用
userOrderId  | string   | 用户自设委托 ID    | 如传入该参数，需同时填写strategyName和quickTrade。对应order委托对象和deal成交对象中的m_strRemark属性
ContextInfo  | class    | 系统参数          | 含有k线信息和接口的上下文对象