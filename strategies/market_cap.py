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
    max_stocks = 7

    def strategy(self, event):
        # if not self.is_open:
        #     return

        self.make_min_cap_stocks(event)
        self.rebalance(event)

        self.log.info(self.user.balance)
        self.log.info(self.user.position)
        self.log.info(self.user.entrust)
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
        today = date.today()
        if self.last_sort_date is None:
            self.should_rebalance = True
        elif self.last_sort_date and (today - self.last_sort_date).days > 15:
            self.should_rebalance = True
        else:
            self.should_rebalance = False
            return

        self.last_sort_date = today

        eq = ts.Equity()
        df = eq.Equ(equTypeCD='A', listStatusCD='L',
                    field='ticker,secShortName,totalShares,nonrestFloatShares,listStatusCD')
        df['ticker'] = df['ticker'].map(lambda x: str(x).zfill(6))
        df['listStatusCD'] = df['listStatusCD'].str.contains('L')
        tickers = df['ticker'].values
        # print(tickers)

        datas = [x for x in iter(event.data.values())]
        datas = list(filter(lambda x: True if x['code'] in tickers else False, datas))
        datas = list(filter(lambda x: x['总市值'] is not None and x['总市值'] > 0, datas))
        datas.sort(key=cmp_to_key(lambda x, y: x['总市值'] - y['总市值']))
        datas = datas[:self.max_stocks]

        self.min_cap_stocks = []
        for x in datas:
            self.min_cap_stocks.append({'code': x['code'], '总市值': x['总市值'], 'name': x['name']})
        print(self.min_cap_stocks)

    def rebalance(self, event):
        if not self.should_rebalance:
            return
        else:
            self.should_rebalance = False

        positions = self.user.position
        position_codes = [x['stock_code'] for x in positions]
        target_codes = [x['code'] for x in self.min_cap_stocks]

        for x in positions:
            # code = filter(str.isdigit, x['stock_code'])
            code = ''.join(c for c in x['stock_code'] if c in '0123456789')
            if not code in target_codes:
                self.log.info('sell {}'.format(x))
                self.user.sell(x['stock_code'], event.data[code]['ask1'], x['enable_amount'], x['market_value'])

        balance = self.user.balance[0]
        buy_codes = []
        for x in target_codes:
            if not (x in position_codes):
                buy_codes.append(x)
        balance_each = balance['current_balance'] / len(buy_codes)
        for x in buy_codes:
            bid1 = event.data[x]['bid1']
            if bid1 <= 0:
                continue
            amount = int(balance_each / bid1 / 100) * 100
            self.log.info('buy {} {}'.format(x, amount))
            self.user.buy(x, bid1, amount)
