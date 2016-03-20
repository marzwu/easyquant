from datetime import date
from functools import cmp_to_key

from easyquant import StrategyTemplate
from easyquant import DefaultLogHandler

import tushare as ts


class Strategy(StrategyTemplate):
    name = 'market_cap'
    is_open = False
    last_sort_date = None
    min_cap_stocks = []

    def strategy(self, event):
        # if not self.is_open:
        #     return

        self.make_min_cap_stocks(event)

        self.log.info(self.user.balance)
        self.log.info('\n')


    def clock(self, event):
        if event.data.clock_event == 'open':
            # 开市了
            self.log.info('open')
        elif event.data.clock_event == 'close':
            # 收市了
            self.log.info('close')
        elif event.data.clock_event == 5:
            # 5 分钟的 clock
            self.log.info("5分钟")

        self.is_open = event.data.trading_state
        print("event.data.trading_state: ", event.data.trading_state)


    def log_handler(self):
        today = date.today()
        return DefaultLogHandler(self.name, log_type='file', filepath='log/%s-%s.log' % (self.name, today.isoformat()))

    def make_min_cap_stocks(self, event):
        eq = ts.Equity()
        df = eq.Equ(equTypeCD='A', listStatusCD='L', field='ticker,secShortName,totalShares,nonrestFloatShares')
        df['ticker'] = df['ticker'].map(lambda x: str(x).zfill(6))
        tickers = df['ticker'].values
        print(tickers)

        datas = [x for x in iter(event.data.values())]
        datas = list(filter(lambda x: True if x['code'] in tickers else False, datas))
        datas = list(filter(lambda x: x['总市值'] is not None and x['总市值'] > 0, datas))
        datas.sort(key=cmp_to_key(lambda x,y: x['总市值']-y['总市值']))
        datas = datas[:7]

        self.min_cap_stocks = []
        for x in datas:
            self.min_cap_stocks.append({'code':x['code'], '总市值':x['总市值']})
        print(self.min_cap_stocks)
