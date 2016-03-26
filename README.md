# easyquant

基于 [easytrader](https://github.com/shidenggui/easytrader) 和 [easyquotation](https://github.com/shidenggui/easyquotation) 的量化交易框架


事件引擎借鉴 `vnpy` 

交易:支持华泰、佣金宝、银河以及雪球模拟盘


行情:支持新浪免费实时行情，集思路分级基金以及 leverfun 的免费十档行情

有兴趣的可以加群 `429011814` 一起交流

欢迎 `star` && `fork`

### 相关

[获取免费实时行情的类库: easyquotation](https://github.com/shidenggui/easyquotation)

[实现交易的类库: easytrader](https://github.com/shidenggui/easytrader)

捐助: [支付宝](http://7xqo8v.com1.z0.glb.clouddn.com/zhifubao2.png)  [微信](http://7xqo8v.com1.z0.glb.clouddn.com/wx.png)

### requirements

* python 3.5
* pip install -r requirements.txt

### 关于行情

默认使用的是 sina 的免费全市场行情，1s 推送一次


可自定义使用的行情来源或者使用 `easyquotation` 的 `lf` 免费十档行情 和 集思路的分级基金行情


具体可参见 [easyquotation](https://github.com/shidenggui/easyquotation) 

### 关于交易

具体可参见 [easytrader](https://github.com/shidenggui/easytrader) 

### 使用 

#### 准备交易账户

在 `ht.json` 或 `yjb.json` 或 `yh.json` 或 `xq.json` 中填入你的账户相关信息

[如何填写相关信息](https://github.com/shidenggui/easytrader)

#### 快速开始

```
python test.py
```

### 策略编写

策略用 `Python` 编写后置于 `strategies` 文件夹下
格式可参考其中的 `Demo`

#### Hello World


```
# 引入策略模板
from easyquant import StrategyTemplate

# 定义策略类
class Strategy(StrategyTemplate):
    name = 'Hello World' # 定义策略名字
    
    # 策略函数，收到行情推送后会自动调用
    def strategy(self, event):
        """:param event event.data 为所有股票行情的字典，结构如下
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
        # 使用 self.user 来操作账户，用法见 easytrader 用法
        # 使用 self.log.info('message') 来打印你所需要的 log
        self.log.info('\n\n策略1触发')
        self.log.info('行情数据: 万科价格: %s' % event.data['000002'])
        self.log.info('检查持仓')
        self.log.info(self.user.balance)
```

##### 效果

```
启动主引擎
[2015-12-28 14:05:36.649599] INFO: main_engine.py: 加载策略: 策略1_Demo
[2015-12-28 14:05:36.650250] INFO: main_engine.py: 加载策略: 策略2_Demo
[2015-12-28 14:05:36.650713] INFO: main_engine.py: 加载策略完毕
触发每秒定时计时器



策略1触发
行情数据: 万科价格:  {'ask4': 0.0, 'ask1': 0.0, 'bid2_volume': 0, 'bid3': 0.0, 'bid5_volume': 0, 'name': '万  科Ａ', 'ask4_volume': 0, 'close': 24.43, 'volume': 0.0, 'ask3_volume': 0, 'bid5': 0.0, 'bid1': 0.0, 'ask2': 0.0, 'bid4_volume': 0, 'high': 0.0, 'ask5': 0.0, 'bid4': 0.0, 'ask5_volume': 0, 'turnover': 0, 'ask2_volume': 0, 'sell': 0.0, 'open': 0.0, 'bid3_volume': 0, 'bid2': 0.0, 'bid1_volume': 0, 'buy': 0.0, 'ask3': 0.0, 'low': 0.0, 'now': 0.0, 'ask1_volume': 0}
检查持仓
[{'asset_balance': 2758.98, 'market_value': 2740.9, 'enable_balance': 18.08, 'current_balance': 18.08, 'money_name': '人民币', 'fetch_balance': 18.08, 'money_type': '0'}]




策略2触发
行情数据: 华宝油气 {'ask4': 0.5, 'ask1': 0.497, 'bid2_volume': 4594100, 'bid3': 0.494, 'bid5_volume': 851300, 'name': '华宝油气', 'ask4_volume': 15650706, 'close': 0.5, 'volume': 138149552.799, 'ask3_volume': 19611307, 'bid5': 0.492, 'bid1': 0.496, 'ask2': 0.498, 'bid4_volume': 313700, 'high': 0.501, 'ask5': 0.501, 'bid4': 0.493, 'ask5_volume': 10108300, 'turnover': 277462973, 'ask2_volume': 10747730, 'sell': 0.497, 'open': 0.5, 'bid3_volume': 997500, 'bid2': 0.495, 'bid1_volume': 5507952, 'buy': 0.496, 'ask3': 0.499, 'low': 0.495, 'now': 0.497, 'ask1_volume': 14948518}
检查持仓
[{'asset_balance': 2758.98, 'market_value': 2740.9, 'enable_balance': 18.08, 'current_balance': 18.08, 'money_name': '人民币', 'fetch_balance': 18.08, 'money_type': '0'}]

```

#### 稍显复杂的策略示例

```python
# 引入策略模板
from easyquant import StrategyTemplate

# 定义策略类
class Strategy(StrategyTemplate):
    name = '测试策略1' # 定义策略名字
    
    def init(self):
        # 进行相关的初始化定义
        self.buy_stocks = [] # 假如一个股票一天只想买入一次。定义一个列表用来存储策略买过的股票
    
    # 策略函数，收到行情推送后会自动调用
    def strategy(self, event):
        """:param event event.data 为所有股票行情的字典，结构如下
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
        # 使用 self.user 来操作账户，用法见 easytrader 用法
        # 使用 self.log.info('message') 来打印你所需要的 log
        self.log.info('\n\n策略1触发')
        self.log.info('行情数据: 万科价格: %s' % event.data['000002'])
        self.log.info('检查持仓')
        self.log.info(self.user.balance)
        # 在未买入的情况下买入万科
        if '000002' not in self.buy_stocks:
            # self.user.buy('000002')
            self.buy_stocks.append('000002')

    # 时钟引擎，用于推送开市、收市以及其他定时事件
    def clock(self, event):
        """在交易时间会定时推送 clock 事件
        :param event: event.data.clock_event 为 [0.5, 1, 3, 5, 15, 30, 60] 单位为分钟,  ['open', 'close'] 为开市、收市
            event.data.trading_state  bool 是否处于交易时间
        """
        if event.data.clock_event == 'open':
            # 开市了
            self.log.info('open')
        elif event.data.clock_event == 'close':
            # 收市了
            self.log.info('close')
            # 收盘时清空已买股票列表 self.buy_stocks
            self.buy_stocks.clear()
        elif event.data.clock_event == 5:
            # 5 分钟的 clock
            self.log.info("5分钟")
```

#### 加载指定策略


```python
m.load_strategy(names=['测试策略2']) # 指定 names 参数，类型为列表，内容为策略的 name 属性
```


### log system

#### 存储日志到文件

```python
from easyquant import DefaultLogHandler # 默认的 log handler,支持输出日志到屏幕和文件,

#  这里使用自带的 log handler, 也可使用自己编写的其他 log handler
log_handler = DefaultLogHandler(name='策略日志', log_type='file', filepath='日志文件.log')

m = easyquant.MainEngine(broker, need_data, log_handler=log_handler)
m.load_strategy()
m.start()
```

#### 自定义每个策略的 log handler

除了上面使用的全局 log handler 外，还可以为每个策略定义使用的 log handler

```python
# define your_log_handler
class Strategy(StrategyTemplate):
    ...
    def log_handler(self):
        return your_log_handler
```

##### 示例: 存储每个策略的日志到不同的文件中

```python
from easyquant import DefaultLogHandler

class Strategy(StrategyTemplate):
    ...
    def log_handler(self):
        return DefaultLogHandler(self.name, log_type='file', filepath='策略xx.log')
```

### 自定义行情引擎

允许使用自定义的其他行情，支持添加多个行情来源

#### 修改默认 sina 行情的推送时间

``` python
from easyquant import DefaultQuotationEngine

DefaultQuotationEngine.PushInterval = 30 # 改为 30s 推送一次
m = easyquant.MainEngine(broker, need_data, quotation_engine=[DefaultQuotationEngine])
```

#### 示例: 使用 lf 的十档行情

```python
import easyquotation
from easyquant import PushBaseEngine # 引入行情引擎的基类

class LFEngine(PushBaseEngine):
    EventType = 'lf' # 指定行情的 EventType
    PushInterval = 5 # 指定行情的推送间隔， 默认为 1s

    def init(self):
        # 进行相关的初始化操作
        self.source = easyquotation.use('lf')

    def fetch_quotation(self):
        # 返回行情
        return self.source.stocks(['162411', '000002'])
m = easyquant.MainEngine(broker, need_data, quotation_engine=[LFEngine])
```

#### 使用多个行情来源

可同时使用多个行情引擎，此时在策略中使用 `event.event_type` 来区分行情来源

```python
from easyquant import DefaultQuotationEngine

m = easyquant.MainEngine(broker, need_data, quotation_engine=[DefaultQuotationEngine, LFEngine, OtherEngine])
```
