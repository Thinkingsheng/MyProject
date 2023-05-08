# -*- coding:utf-8 -*-
# @Author : Think
# @Date : 2023-04-10
# @File_name : update_dm_search_index.py


from thl_test_py.fun_sum.http_post_data import http_post_weibo_data
from thl_test_py.fun_sum.global_fun import CurrentTimeTrans
# 导入自建的数据库处理类
from thl_test_py.fun_sum.db_handle import DBHandle
# 导入数据库配置信息字典
from thl_test_py.arguments_sum.db_info import thltest_db_info

target_table = 'dm_search_index_day'

max_date_sql = "select max(`date`) from %s WHERE `type` = 'WB'" % target_table


# 主要更新调用函数
def update_dm_search_index_fun(db_dict, target_table, max_date_sql):
    # 创建自定义的DBHandle实例
    my_db = DBHandle(db_dict)
    full_data = http_post_weibo_data(my_db.get_start_date(max_date_sql), CurrentTimeTrans().get_end_date())
    # 调用append_data方法新增到库，后用close_conn关闭引擎
    my_db.append_data(target_table, full_data)
    my_db.close_conn()


# 补数据的函数
def replenish_dm_search_index_fun(db_dict, target_table, start_date, end_date):
    # 创建自定义的DBHandle实例
    my_db = DBHandle(db_dict)
    full_data = http_post_weibo_data(start_date, end_date)
    # 调用append_data方法新增到库，后用close_conn关闭引擎
    my_db.append_data(target_table, full_data)
    my_db.close_conn()


if __name__ == "__main__":
    # replenish_dm_search_index_fun(thltest_db_info, target_table, "2023-01-09", "2023-04-09")
    update_dm_search_index_fun(thltest_db_info, target_table, max_date_sql)
    # sleep(5)
    # update_dm_search_index_fun(thlprod_db_info, target_table, max_date_sql)
else:
    pass
