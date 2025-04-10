deal_callback - 账号成交状态变化主推
提示

仅在实盘运行模式下生效。
需要先在init里调用ContextInfo.set_account后生效。

用法： deal_callback(ContextInfo, dealInfo)

释义： 当账号成交状态有变化时，这个函数被客户端调用


示例代码：
#coding:gbk
def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def init(ContextInfo):
    # 设置对应的资金账号
    # 示例需要在策略交易界面运行
    ContextInfo.set_account(account)
    
def after_init(ContextInfo):
    # 在策略交易界面运行时，account的值会被赋值为策略配置中的账号，编辑器界面运行时，需要手动赋值
    # 编译器界面里执行的下单函数不会产生实际委托  
    passorder(23, 1101, account, "000001.SZ", 5, 0, 100, "示例", 2, "投资备注",ContextInfo)
    pass

def deal_callback(ContextInfo, dealInfo):
    print(show_data(dealInfo))


还是持仓编号的callback等，暂不展开