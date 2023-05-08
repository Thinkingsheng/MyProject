# -*- coding:utf-8 -*-
# @Author : Think
# @Date : 2023-04-14
# @File_name : data_append_db.py

from thl_test_py.fun_sum.db_handle import DBHandle


def data_append_db(data_df, db_dict, table_name):
    """
    :param data_df: 调用thl_test_py/MaoBo_data_collection/utils/data_handle模块的data_handle函数返回的dataframe
    :param db_dict: thl_test_py/arguments_sum/db_info模块的db信息字典
    :param table_name: 对应的表名（对应列的顺序要跟data_df一致）
    :return: 提示
    """
    my_db = DBHandle(db_dict)
    my_db.append_data(table_name, data_df)
    my_db.close_conn()
