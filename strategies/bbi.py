import datetime
import time

import redis

from easyquant.strategy.strategyTemplate import StrategyTemplate


class Strategy(StrategyTemplate):
    name = 'bbi'
    redis_poll = None

    def strategy(self, event):
        print(datetime.datetime.now(), 'strategy')
        if '600423' in event.data:
            print(event.data['600423'])

    def clock(self, event):
        print('trading state', event.data.trading_state)

        if event.data.clock_event == 'open':
            # 开市了
            self.log.info('open')
        elif event.data.clock_event == 'close':
            # 收市了
            self.log.info('close')
        elif event.data.clock_event == 5:
            # 5 分钟的 clock
            self.log.info("5分钟")

    def log_handler(self):
        super().log_handler()

    def init(self):
        super().init()
        self.log.info("连接redis")
        self.redis_poll = redis.ConnectionPool(host='127.0.0.1', port='6379')

    def shutdown(self):
        super().shutdown()
        self.redis_poll.disconnect()

    def s_sell(self):
        while True:
            self.user.sell('600423')
            time.sleep(5)
