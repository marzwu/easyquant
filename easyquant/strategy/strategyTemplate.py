# coding:utf-8
import traceback

class StrategyTemplate:
    name = 'DefaultStrategyTemplate'

    def __init__(self, user, log_handler):
        self.user = user
        custom_log_handler = self.log_handler()
        self.log = log_handler if custom_log_handler is None else custom_log_handler
        self.init()

    def init(self):
        # 进行相关的初始化操作
        pass

    def strategy(self, event):
        """:param event event.data 为所有股票的信息，结构如下
        {'162411':
        {'ask1': '0.493',
         'ask1_volume': '75500',
         'ask2': '0.494',
         'ask2_volume': '7699281',
         'ask3': '0.495',
         'ask3_volume': '2262666',
         'ask4': '0.496',
         'ask4_volume': '1579300',
         'ask5': '0.497',
         'ask5_volume': '901600',
         'bid1': '0.492',
         'bid1_volume': '10765200',
         'bid2': '0.491',
         'bid2_volume': '9031600',
         'bid3': '0.490',
         'bid3_volume': '16784100',
         'bid4': '0.489',
         'bid4_volume': '10049000',
         'bid5': '0.488',
         'bid5_volume': '3572800',
         'buy': '0.492',
         'close': '0.499',
         'high': '0.494',
         'low': '0.489',
         'name': '华宝油气',
         'now': '0.493',
         'open': '0.490',
         'sell': '0.493',
         'turnover': '420004912',
         'volume': '206390073.351'}}
        """
        pass

    def run(self, event):
        try:
            self.strategy(event)
        except Exception as e:
            self.log.error(e)
            self.log.error(traceback.format_exc())

    def clock(self, event):
        pass

    def log_handler(self):
        pass
