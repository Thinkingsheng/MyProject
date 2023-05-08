# -*- coding:utf-8 -*-
# @Author : Think
# @Date : 2023-04-14
# @File_name : starter.py

from thl_test_py.MaoBo_data_collection.params import uri_params
from thl_test_py.MaoBo_data_collection.utils.get_params_make import GetParamsMake
from thl_test_py.MaoBo_data_collection.utils.data_handle import data_handle
from thl_test_py.MaoBo_data_collection.utils.data_append_db import data_append_db


def starter(db_dict, table_name, url_dict, params_dict, append_db_params_list, *uri_make_params):
    """
    全部模块的启动器
    :param db_dict: db信息字典
    :param table_name: 数据库的表名
    :param url_dict: uri_params文件内定义的各个接口的url_dict
    :param params_dict: uri_params文件内定义的各个接口的params_dict
    :param append_db_params_list: thl_test_py/MaoBo_data_collection/params/uri_params的append_db_params_list（“需要插入到数据库的参数名称”列表）
    :param uri_make_params: GetUriMake类对应方法的全部参数
    :return: 提示
    """
    url_params_list = []
    # 按照映射字典uri_params.uri_make_dict，找对应uri构建的类型
    if uri_params.uri_make_dict[url_dict["path"]] == "one_day":
        url_params_list = GetParamsMake(url_dict, params_dict).one_day_param(uri_make_params[0], uri_make_params[1],
                                                                             uri_make_params[2])
    elif uri_params.uri_make_dict[url_dict["path"]] == "two_day":
        url_params_list = GetParamsMake(url_dict, params_dict).two_day_param(uri_make_params[0], uri_make_params[1],
                                                                             uri_make_params[2], uri_make_params[3])
    elif uri_params.uri_make_dict[url_dict["path"]] == "one_month":
        url_params_list = GetParamsMake(url_dict, params_dict).one_month_param(uri_make_params[0], uri_make_params[1],
                                                                               uri_make_params[2])
    # 获取df
    data_df = data_handle(url_params_list, append_db_params_list, db_dict)
    # 插入到数据库的对应表
    data_append_db(data_df, db_dict, table_name)
