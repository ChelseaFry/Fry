# user.ipynb的用户使用指南
在第一个cell输入参数：

n: n日反转策略的n。

percentage: 多空策略的两端比例。

start_date,end_date:回测的时间段始末。要求时间段在2020.1.1-2022.12.31之间。

依次运行以下所有的cell。其中evaluate这个部分给出了回测结果。compare的部分可以对两种策略的回测结果进行比较。

在compare若要自己传入signal来测试其他类型的股票策略，请以以下格式传入evaluate和compare函数。

| 日期 | 股票1 |股票2|……|股票n|
|------|-----|---|---|---|
|    |  各种股票因子值   |

# 系统文件组成


## *data_processor.py*: 读入并处理数据。
内置函数：

***1、preprocess_data(file_path, fillna_method)***

参数解释：


file_path:读取文件路径

fillna_method:填充缺失值的方法。可选的有'drop'（直接去除所有含有缺失值的股票），'bfill'、'ffill'(向后填充、向前填充)

返回值：一个数据的dict，里面不同字段代表不同数据类型所有股票的全时段数据。

函数功能：读入量价数据文件。便于后续处理。

***2、preprocess_benchmark(file_path)***

参数解释：

file_path:读取文件路径

函数返回值：一个以date为索引的沪深300价格数据，作为基准收益率的参考。

函数功能：读入沪深300价格文件并整理格式，便于后续比较。

## *signal_generator.py*：生成信号

内置函数：

***1、generate_signal(data_dict, n, percentage, start_time, end_time)***

参数解释：

data_dict：在之前的data_processor中给出的数据字典

n = "n日反转策略"中的n值。

percentage: 根据因子值做多空策略，做多前percentage比例的股票，做空后percentage比例的股票

start_time, end_time：回测的时间段。

函数返回值：每个股票信号的时间序列

函数功能：生成n日反转信号。

## *mybacktest.py*:回测信号

内置函数：

***1、evaluate_signal(benchmark, signal, start_time, end_time, data_dict)***

参数解释：

benchmark：沪深300，作为基准收益率

signal：signal_generator中生成的信号

start_time,end_time：回测的时间段

data_dict：在之前的data_processor中给出的数据字典

函数功能：输出该策略的净值曲线、与沪深300的对比曲线，以及一些基础的指标：年化收益、年化波动率、夏普比率、最大回撤等

***2、compare_signal(signal1, signal2, start_time, end_time, data_dict)***

参数解释：

signal1,signal2：待比较的两种信号

start_time,end_time：回测的时间段

data_dict: 在之前的data_processor中给出的数据字典

函数功能：比较两个给定的信号的回测结果。

