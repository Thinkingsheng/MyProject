# -*- coding:utf-8 -*-

import pandas as pd
from thl_test_py.fun_sum.get_api_data import get_epidemic_data, get_holiday_data, get_weather_data
from thl_test_py.fun_sum.global_fun import CurrentTimeTrans
from thl_test_py.fun_sum.global_fun import DateList
# 导入自建的数据库处理类
from thl_test_py.fun_sum.db_handle import DBHandle
# 导入数据库配置信息字典
from thl_test_py.arguments_sum.db_info import thltest_db_info

target_table = 'dim_holiday_weather_day_1'

max_date_sql = "select max(`day`) from %s" % target_table


def update_dim_table_fun(db_dict, target_table, max_date_sql):
    # 创建自定义的DBHandle实例
    my_db = DBHandle(db_dict)
    # 调用get_start_date方法获取start_date，然后传入start_date和end_date到Data_list类获取日期区间列表
    history_date_range = DateList(my_db.get_start_date(max_date_sql), CurrentTimeTrans().get_end_date()).date_compute()
    # 定义多个merge_data的列表（存储各个日期的数据）
    merge_data_list = []
    # 遍历每个日期，查询数据，写入到库
    for history_date in history_date_range:
        # 合并多个dataframe，为merge_data
        temp_data = pd.merge(get_holiday_data(history_date), get_weather_data(history_date), on='date', how='left')
        merge_data = pd.merge(temp_data, get_epidemic_data(history_date), on='date', how='left')
        # 插入到merge_data_list
        merge_data_list.append(merge_data)
    # 将merge_data_list里的dataframe上下拼接
    full_data = pd.concat(merge_data_list, axis=0)
    full_data = full_data.reset_index(drop=True)
    # 将full_data里的日期字符串转为datetime64（似乎不转也可以导为MYSQL表的date类型）
    # full_data['date'] = pd.to_datetime(fin_data['date'])
    # 调用append_data方法新增到库，后用close_conn关闭引擎
    my_db.append_data(target_table, full_data)
    my_db.close_conn()


if __name__ == "__main__":
    update_dim_table_fun(thltest_db_info, target_table, max_date_sql)
    # sleep(5)
    # update_dim_table_fun(thlprod_db_info, target_table, max_date_sql)
else:
    pass

