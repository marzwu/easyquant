import math
import talib as tl
import pandas as pd
import numpy as np
from datetime import timedelta
import talib
from easyquant.strategy.strategyTemplate import StrategyTemplate


# 名称：
# 介绍：
# 风险：
# 仓位：
# 适用：
# 其他：
class Strategy(StrategyTemplate):
    g = {}

    # 初始化日期
    g.d_yesterday = ''
    g.d_today = ''
    
    ###### 各类常量 ######
    g.con_START_DATE = 100 # 股票上市时间限制
    g.con_MARKET_CAP = 200 # 流通市值标准
    
    # 初始化综合风险结果
    g.ris = 10
    g.ar = 1
    
    # 记录真实RSI_F和AR
    g.RIS_T = 0
    g.AR_T = 0
    
    # 上次风险判断标准
    g.risk_flag = 1
    g.buy_flag = 0
    
    # 初始化风险变化趋势数据
    g.risk_day1 = 0
    g.risk_day2 = 0
    g.risk_day3 = 0
    
    # 初始化风险参数
    g.con_FAST_RSI = 20
    g.con_SLOW_RSI = 60
    g.con_AR_COUNT = 26 # 以4天为期间计算AR值（普通为26天），反应长期趋势
    
    # 初始化当日买卖列表
    g.stock_buy = []
    
    # 取得对应股票代码的RSI风险指标
    def get_RSI(self, stock):
         # 取得历史收盘价格
        df_hData = attribute_history(stock, 80, unit = '1d', fields = ('close', 'high', 'low'), skip_paused = True)
        df_hData_today = get_price(stock,start_date = g.d_today, \
                                   end_date = g.d_today, frequency = 'daily', fields = ['close', 'high', 'low'])

        df_hData = df_hData.append(df_hData_today)

        closep = df_hData['close'].values

        RSI_F = tl.RSI(closep, timeperiod = g.con_FAST_RSI)
        RSI_S = tl.RSI(closep, timeperiod = g.con_SLOW_RSI)
        isFgtS = RSI_F > RSI_S

        rsiS = RSI_S[-1]
        rsiF = RSI_F[-1]

        '''
        慢速RSI 在55以上时，单边上涨市场，快速RSI上穿慢速RSI即可建仓
        慢速RSI 在55以下时，调整震荡市场，谨慎入市，取连续N天快速RSI大于慢速RSI建仓
        慢速RSI 在60以上时，牛市，无需减仓操作持仓即可
        '''
        # 基准仓位值
        bsFlag = 10

        if rsiS > 55 and isFgtS[-1]:
            bsFlag = 50 # "上行"
        elif rsiS > 68:
            bsFlag = 40 # "高位"
        elif rsiS > 60:
            bsFlag = 30 # "持仓"
        elif rsiS <= 55 \
            and isFgtS[-1] and isFgtS[-2] \
            and isFgtS[-3] and isFgtS[-4] \
            and isFgtS[-5] :
                bsFlag = 20 # "盘整建仓"
        else:
            bsFlag = 10 # "下行"

        g.RSI_T = rsiS

        return bsFlag

    # 取得对应股票代码的AR活跃度指标
    def get_AR(self, stock, count):
        df_ar = attribute_history(stock, count - 1, '1d', fields=('open', 'high', 'low'), skip_paused = True)
        df_ar_today = get_price(stock,start_date = g.d_today, \
                                end_date = g.d_today, frequency = 'daily', fields = ['open', 'high', 'low'])

        df_ar = df_ar.append(df_ar_today)

        ar = sum(df_ar['high'] - df_ar['open']) / sum(df_ar['open'] - df_ar['low']) * 100

        '''
        AR指标 在180以上时，股市极高活跃
        AR指标 在120 - 180时，股市高活跃
        AR指标 在70 - 120时，股市盘整
        AR指标 在60 - 70以上时，股市走低
        AR指标 在60以下时，股市极弱
        '''
        brFlag = 1

        if ar > 180 :
            brFlag = 5
        elif ar > 120 and ar <= 180 :
            brFlag = 4
        elif ar > 70 and ar <= 120 :
            brFlag = 3
        elif ar > 60 and ar <= 70 :
            brFlag = 2
        else :
            brFlag = 1

        g.AR_T = ar

        return brFlag

    # 取得对应大盘的风险
    def get_stock_risk(self, stock, count):
        # 今日风险估算
        rsi = get_RSI(stock)
        ar = get_AR(stock, count)

        g.ris = rsi
        g.ar = ar

        g.risk_day1 = g.risk_day2
        g.risk_day2 = g.risk_day3
        g.risk_day3 = g.AR_T

        buy_flag = 2

        if rsi == 10:
            buy_flag = 0
        elif rsi == 20:
            buy_flag = 2
        else:
            buy_flag = 1

        # 趋势控制
        if g.risk_day1 < 60 and g.risk_day2 < 60 and g.risk_day3 < 60:
            # 持续低迷
            buy_flag = 0
        elif g.risk_day1 < g.risk_day2 and g.risk_day2 < g.risk_day3 and \
            g.risk_day3 < 80 and g.risk_day3 > 65:
            # 弱市回升
            buy_flag = 1
        elif g.risk_day1 > g.risk_day2 and g.risk_day2 > g.risk_day3 and \
            g.risk_day3 < 150 and g.risk_day1 > 200:
            # 强市下跌
            buy_flag = 0
        elif g.risk_day1 > 70 and g.risk_day2 > 70 and g.risk_day3 > 70:
            # 维持正常
            buy_flag = 1
        else:
            buy_flag = 2

        return buy_flag

    # 测试数
    def get_test_list(self):

        alllist = ['600030.XSHG','601288.XSHG','601989.XSHG','300085.XSHE']

        alllist = ['300397.XSHE','600490.XSHG','000627.XSHE','300372.XSHE','000905.XSHE',
                    '002044.XSHE','300384.XSHE','601012.XSHG','601339.XSHG','000526.XSHE',
                    '002749.XSHE','002278.XSHE','002342.XSHE','002719.XSHE','603300.XSHG',
                    '600113.XSHG','000955.XSHE', '002346.XSHE', '300272.XSHE']
        return alllist

    def weekly(self, context):
        g.stock_buy = []

        if g.buy_flag <> 0:
            # 取得流通市值200亿以下的股票数据
            d_startdate = (context.current_dt  - timedelta(days = g.con_START_DATE)).strftime("%Y-%m-%d")

            q = query(
                valuation.code, valuation.circulating_cap
            ).filter(
                #valuation.code.in_(get_test_list()),
                valuation.circulating_market_cap < g.con_MARKET_CAP
            )

            df = get_fundamentals(q, date = d_startdate)

            df.index = list(df['code'])

            # 去除ST，*ST
            st = get_extras('is_st', list(df['code']), start_date = g.d_today, end_date = g.d_today, df = True)
            st = st.iloc[0]
            stock_list = list(st[st == False].index)

            df_list = get_price(stock_list, start_date=g.d_today, end_date=g.d_today, frequency='daily', fields=['pre_close'])
            df_close = history(29, unit='1d', field='pre_close', security_list = stock_list)
            df_close = df_close.append(df_list['pre_close'])

            MA30 = np.mean(df_close)
            MA12 = np.mean(df_close.tail(12))
            log_r = df_close.tail(1).iloc[0]

            df_weight_MA30 = pd.DataFrame((log_r**2) / (MA30**2))
            df_weight_MA12 = pd.DataFrame((log_r**2) / (MA12**2))

            df_weight_MA30.columns = ['weight_MA30']
            df_weight_MA12.columns = ['weight_MA12']

            df_weight = pd.concat([df_weight_MA30, df_weight_MA12], axis = 1, join_axes = [df_weight_MA30.index])

            df_weight = df_weight.dropna()
            df_weight = df_weight[df_weight['weight_MA30'] < 1]
            df_weight = df_weight[df_weight['weight_MA12'] < 1]
            '''
            if g.ris > 20 or g.ar > 3 :
                df_weight = df_weight.sort(columns = 'weight_MA30', ascending = False).tail(10)
                df_weight = df_weight.sort(columns = 'weight_MA12', ascending = False).head(3)

                log.info('强市选择')
            else:
                df_weight = df_weight.sort(columns = 'weight_MA30', ascending = False).tail(6)
                df_weight = df_weight.sort(columns = 'weight_MA12', ascending = False).tail(3)

                log.info('弱市选择')
            '''
            df_weight = df_weight.sort(columns = 'weight_MA30', ascending = False).tail(10)
            df_weight = df_weight.sort(columns = 'weight_MA12', ascending = False).head(3)
            g.stock_buy = df_weight.index

            log.info( g.stock_buy)

        for stock in context.portfolio.positions.keys():
            order_target(stock, 0)

        cash = context.portfolio.cash

        for stock in g.stock_buy:
            order_value(stock, cash / len(g.stock_buy))

    # 每天交易前调用
    def before_trading_start(self, context):
        # 昨天
        g.d_yesterday = (context.current_dt  - timedelta(days = 1)).strftime("%Y-%m-%d")

        # 今天
        g.d_today = (context.current_dt).strftime("%Y-%m-%d")

    # 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
    def handle_data(self, context, data):
        pass

    # 每天交易后调用
    def after_trading_end(self, context):
        self.g.buy_flag = get_stock_risk(self.g.riskbench, 4)

        self.log.info("今日风险："+ "RSI: %i" %self.g.ris + ", AR: %i" %self.g.ar + " 购买指标：" + str(self.g.buy_flag))
        '''
        if g.buy_flag == 2:
            g.buy_flag = g.risk_flag
        else:
            g.risk_flag = g.buy_flag
        '''