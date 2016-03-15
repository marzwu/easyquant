from easyquant import StrategyTemplate
from easyquant import DefaultLogHandler


class Strategy(StrategyTemplate):
    name = 'PB'
    is_open = False

    def strategy(self, event):
        if not self.is_open:
            return

        self.log.info('\n\n策略PB触发')
        self.log.info('行情数据: 华宝油气 %s' % event.data['162411'])
        self.log.info('检查持仓')
        self.log.info(self.user.balance)
        self.log.info('\n')

    def check(self, event):
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

    def log_handler(self):
        return DefaultLogHandler(self.name, log_type='file', filepath='pb.log')

