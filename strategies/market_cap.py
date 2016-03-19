from datetime import date
from easyquant import StrategyTemplate
from easyquant import DefaultLogHandler


class Strategy(StrategyTemplate):
    name = 'market_cap'
    is_open = False

    def strategy(self, event):
        if not self.is_open:
            return



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