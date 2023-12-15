import numpy as np
def generate_signal(data_dict, n, percentage, start_time, end_time):
    adjclose_df = data_dict['adjclose']
    factor_df = (adjclose_df/adjclose_df.shift(n))-1
    def process_row(row):
        max_threshold = row.quantile(1 - percentage)
        min_threshold = row.quantile(percentage)
        return row.apply(lambda x: -x if (x <= min_threshold or x >= max_threshold) else np.nan)
    factor_df = factor_df.apply(process_row, axis = 1)
    factor_df = factor_df.loc[start_time: end_time]
    return factor_df