from datetime import date
from functools import cmp_to_key

from easyquant import StrategyTemplate
from easyquant import DefaultLogHandler

import tushare as ts


class Strategy(StrategyTemplate):
    name = '五日十日均线'

    balance = None
    position = None
    entrust = None

    is_open = False
    is_traded = False#当日是否交易过

    code = '150182'#军工B
    index = '399967'#中证军工

    def strategy(self, event):
        if (not self.is_open) or self.is_traded:
            return

        self.balance = self.user.balance
        self.position = self.user.position
        entrust = self.user.entrust()
        entrust = [x for x in entrust if x['entrust_status'] == '已报']
        self.entrust = entrust

        self.log.info('balance: {}'.format(self.balance))
        self.log.info('position: {}'.format(self.position))
        self.log.info('entrust: {}'.format(self.entrust))
        self.log.info('\n')

        self.handle_data(event)

        self.is_traded = True

    def clock(self, event):
        if event.data.clock_event == 'open':
            # 开市了
            self.log.info('open')
            self.is_traded = False
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

    def handle_data(self, event):
        hist = ts.get_hist_data(self.code)
        print(hist.head())
        print(hist['ma5'])

        a5 = hist['ma5'][0]
        a10 = hist['ma10'][0]

        hist = ts.get_hist_data(self.index)
        print(hist.head())

        b5 = hist['ma5'][0]
        b10 = hist['ma10'][0]

        code_data = event.data[self.code]
        current_price = code_data['bid1']
        cash = self.balance[0]['current_balance']
        today = date.today()

        if b5 > b10 and today.day < 25:  # 五日线大于十日线买入
            if cash > 100 * current_price:
                amount = int(cash / current_price / 100) * 100
                self.log.info('buy {} {}'.format(self.code, amount))
                self.user.buy(self.code, current_price, amount)
        elif current_price < a5:  # 卖出要敏感一些
            for x in self.position:
                # code = filter(str.isdigit, x['stock_code'])
                code = ''.join(c for c in x['stock_code'] if c in '0123456789')
                self.log.info('sell {}'.format(x))
                self.user.sell(x['stock_code'], event.data[code]['ask1'], x['enable_amount'], x['market_value'])