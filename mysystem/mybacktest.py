import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False #显示负号
from IPython.display import display


def evaluate_signal(benchmark, signal, start_time, end_time, data_dict):
    return_df = data_dict['return']
    return_df = return_df.loc[start_time: end_time]
    benchmark = benchmark.loc[start_time: end_time]
    port_ret = signal.shift(1)*return_df
    benchmark_ret = benchmark/benchmark.shift(1)-1
    benchmark_ret = benchmark_ret.fillna(0)
    benchmark = benchmark/benchmark['price'][0]
    benchmark_annual_ret = (benchmark_ret.mean()*242)[0]
    port_ret = port_ret.mean(axis = 1).dropna()
    mv = (port_ret + 1).cumprod()
    plt.plot(mv.index, mv)
    plt.legend(['策略净值'], loc = 'upper right')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('策略净值曲线')
    plt.show()
    fig, ax = plt.subplots()
    ax.plot(mv.index, mv, label = '策略')
    ax.plot(benchmark.index, benchmark['price'], label = '沪深300')
    ax.legend()
    ax.set_title('策略与沪深300走势比较')
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    plt.show()
    annual_ret = port_ret.mean()*242
    excess_ret = annual_ret - benchmark_annual_ret
    annual_vol = port_ret.std()* np.sqrt(242)
    sharpe = annual_ret / annual_vol
    mdd = -min(mv / mv.cummax() - 1)
    cs = ['回测开始时间','回测结束时间','年化收益','年化超额收益','年化波动','夏普比率','最大回撤']
    vs = [start_time, end_time, annual_ret, excess_ret, annual_vol, sharpe, mdd]
    stats = pd.DataFrame({'指标名称':cs,'指标值':vs})
    stats = stats.set_index('指标名称')
    display(stats)
    return stats

def compare_signal(signal1, signal2, start_time, end_time, data_dict):
    return_df = data_dict['return']
    return_df = return_df.loc[start_time:end_time]
    port1_ret = signal1.shift(1)*return_df
    port2_ret = signal2.shift(1)*return_df
    port1_ret = port1_ret.mean(axis = 1).dropna()
    port2_ret = port2_ret.mean(axis = 1).dropna()
    mv1 = (1+port1_ret).cumprod()
    mv2 = (1+port2_ret).cumprod()
    fig,ax = plt.subplots()
    ax.plot(mv1.index, mv1, label = '策略1')
    ax.plot(mv2.index, mv2, label = '策略2')
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.legend()
    ax.set_title('不同策略的比较')
    plt.show()
    annual_ret1 = port1_ret.mean()*242
    annual_vol1 = port1_ret.std()* np.sqrt(242)
    sharpe1 = annual_ret1 / annual_vol1
    mdd1 = -min(mv1 / mv1.cummax() - 1)
    annual_ret2 = port2_ret.mean()*242
    annual_vol2 = port2_ret.std()* np.sqrt(242)
    sharpe2 = annual_ret2 / annual_vol2
    mdd2 = -min(mv2 / mv2.cummax() - 1)
    cs = ['年化收益','年化波动','夏普比率','最大回撤']
    vs1 = [annual_ret1,  annual_vol1, sharpe1, mdd1]
    vs2 = [annual_ret2,  annual_vol2, sharpe2, mdd2]
    stats = pd.DataFrame({'指标名称':cs,'策略1':vs1,'策略2':vs2})
    stats = stats.set_index('指标名称')
    display(stats)