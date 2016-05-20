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
    max_stocks = 3

    def strategy(self, event):
        if not self.is_open:
            return

        self.make_min_cap_stocks(event)
        self.rebalance(event)

        self.log.info('balance: {}'.format(self.user.balance))
        self.log.info('position: {}'.format(self.user.position))
        entrust = self.user.entrust
        entrust = [x for x in entrust if x['entrust_status'] == '已报']
        self.log.info('entrust: {}'.format(entrust))
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

        datas = [x for x in iter(event.data.values()) if
                 x['volume'] > 0 and '*ST' not in x['name']]  # 交易量为0即停牌,剔除停牌,剔除*st
        datas = list(filter(lambda x: True if x['code'] in tickers else False, datas))  # 剔除非上市状态
        datas = list(filter(lambda x: x['总市值'] is not None and x['总市值'] > 0, datas))  # 排除市值等于0的,比如基金
        datas.sort(key=cmp_to_key(lambda x, y: x['总市值'] - y['总市值']))  # 市值升序排序
        datas = datas[:self.max_stocks]

        self.min_cap_stocks = []
        for x in datas:
            self.min_cap_stocks.append({'code': x['code'], '总市值': x['总市值'], 'name': x['name']})
        print('股票池:{}'.format(self.min_cap_stocks))

    def rebalance(self, event):
        if not self.should_rebalance:
            return
        else:
            self.should_rebalance = False

        positions = self.user.position
        entrust = self.user.entrust
        # 持仓和已经委托买入的
        position_codes = [x['stock_code'] for x in positions] \
                         + [x['stock_code'] for x in entrust if x['entrust_status'] == '已报' and x['entrust_bs'] == '买入']
        position_codes = [''.join(c for c in x if c in '0123456789') for x in position_codes]
        target_codes = [x['code'] for x in self.min_cap_stocks]

        # 卖出不在买入列表里的股票
        for x in positions:
            if x['stock_code'] == '':
                continue

            # code = filter(str.isdigit, x['stock_code'])
            code = ''.join(c for c in x['stock_code'] if c in '0123456789')
            # if not code in target_codes:
            if True:
                self.log.info('sell {}'.format(x))
                print('sell {}'.format(x))
                self.user.sell(x['stock_code'], event.data[code]['ask1'], x['enable_amount'], x['market_value'])

        # return

        # 买入股票
        buy_codes = []
        for x in target_codes:
            # if not (x in position_codes):
            if True:
                buy_codes.append(x)

        if len(buy_codes) > 0:
            balance = self.user.balance[0]
            balance_each = balance['current_balance'] / len(buy_codes)
            for x in buy_codes:
                bid1 = event.data[x]['bid1']
                if bid1 <= 0:  # 如果停牌
                    continue
                amount = int(balance_each / bid1 / 100) * 100
                self.log.info('buy {} {}'.format(x, amount))
                print('buy {} {}'.format(x, amount))
                self.user.buy(x, bid1, amount)
