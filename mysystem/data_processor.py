import pandas as pd
def preprocess_data(file_path, fillna_method = 'drop'):
    """
    从给定的文件路径读取数据并返回一个字典，里面不同的key对应的value为不同指标的全市场数据。
    """
    pv_df = pd.read_feather(file_path)  # 由于给定数据是feather格式。故用read_feather
    def get_data(df, value_name):
        data_df = df.pivot_table(index = 'date',columns = 'stk_id', values = value_name)
        if(fillna_method == 'drop'):
            data_df = data_df.dropna(axis = 1)
        elif(fillna_method == 'bfill' or fillna_method == 'ffill'):
            data_df = data_df.fillna(method = fillna_method)
        else:
            print('invalid fillna method!')
        return data_df
    close_df = get_data(pv_df, 'close')
    open_df = get_data(pv_df, 'open')
    high_df = get_data(pv_df,'high')
    low_df = get_data(pv_df, 'low')
    amount_df = get_data(pv_df, 'amount')
    volume_df = get_data(pv_df, 'volume')
    cumadj_df = get_data(pv_df, 'cumadj')
    adjclose_df = close_df.multiply(cumadj_df)
    return_df = adjclose_df/adjclose_df.shift(1)-1
    return_df = return_df.fillna(0)
    result = {
        'close':close_df,
        'open':open_df,
        'high':high_df,
        'low':low_df,
        'amount':amount_df,
        'volume':volume_df,
        'cumadj':cumadj_df,
        'adjclose':adjclose_df,
        'return':return_df
    }
    return result

def preprocess_benchmark(file_path):
    hushen = pd.read_excel(file_path)
    hushen['date'] = pd.to_datetime(hushen['date'])
    hushen = hushen.set_index('date')
    return hushen 

