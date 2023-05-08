# -*- coding:utf-8 -*-
# @Author : Think
# @Date : 2023-04-23
# @File_name : data_handle.py

from thl_test_py.MaoBo_data_collection.utils.data_collection import get_data_collection
import pandas as pd


def data_handle(url_params_list, append_db_param_list, db_dict):
    """
    用 “GetUriMake类返回的url_params_list” 多次调用 “get_data_collection函数” 获取数据dict，结合需要存入数据库的调用参数，将数据处理成完整的dataframe
    注：同一个url_params_list请求返回的数据，字段值和数目需一致！！！
    :param url_params_list: 调用thl_test_py/MaoBo_data_collection/utils/get_uri_make模块GetUriMake类返回的url_params_list
    :param append_db_param_list: thl_test_py/MaoBo_data_collection/params/uri_params的append_db_params_list（“需要插入到数据库的参数名称”列表）
    :param db_dict: thl_test_py/arguments_sum/db_info模块的db信息字典
    :return: 最终插入到数据库的dataframe
    """
    # 一、获取返回的数据字典，并处理成df，存到df_list
    # 定义存储df的列表
    df_list = []
    # 遍历参数字典列表的索引（后续便于添加到g_index_list）
    for g_index in range(len(url_params_list[1])):
        # 调用 “get_data_collection函数”请求并获取数据
        data_list = get_data_collection(url_params_list[0], url_params_list[1][g_index], db_dict)["content"]
        # 将字典列表data_list( 格式：[{字段1：值1, 字段2：值2,...},{字段1：值1, 字段2：值2,...}] )转为dataframe
        data_df = pd.DataFrame(data_list)
        # 插入到df_list
        df_list.append(data_df)

    # 二、将参数值整合到df
    # 定义存储完整df的列表
    full_df_list = []
    # 获取“需插入到数据库的对应参数”，插入到df
    if len(append_db_param_list) != 0:
        # 遍历每组参数/每组df对应的索引
        for g_index in range(len(url_params_list[1])):
            # 取并赋值给df
            df = df_list[g_index]
            for append_db_param in append_db_param_list:
                try:
                    # 将“需插入到数据库的对应参数”值插入到df
                    df[append_db_param + "_temp"] = url_params_list[1][g_index][append_db_param]
                except ValueError:
                    raise ValueError("“需要插入库的参数值列表”有误！")
                else:
                    full_df_list.append(df)
    # append_db_param_list为空，则将df_list赋给full_df_list
    else:
        full_df_list = df_list

    # 三、上下拼接df列表里的所有df（字段值和数目需一致）
    full_df = pd.concat(full_df_list, axis=0)
    # 重排df的index
    full_df = full_df.reset_index(drop=True)
    return full_df
