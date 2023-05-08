# -*- coding:utf-8 -*-
# @Author : Think
# @Date : 2023-04-14
# @File_name : data_collection.py

import httpx
from thl_test_py.MaoBo_data_collection.utils.log_data_handle import log_data_handle
from thl_test_py.MaoBo_data_collection.utils.data_append_db import data_append_db


def get_data_collection(url, params_dict, db_dict):
    """
    单个uri的get请求获取数据，然后将请求的信息及数据存入到库，直接返回字典
    :param url: 单个url
    :param params_dict: 参数字典
    :param db_dict: thl_test_py/arguments_sum/db_info模块的db信息字典
    :return: 返回的res.text直接转的字典(  结构:{'status':..., 'message':..., 'content':[{字段1：值1, 字段2：值2,...},{字段1：值1, 字段2：值2,...}]}  )
    """
    # 一、声明使用http2，请求获取数据
    with httpx.Client(http2=True) as client:
        res = client.get(url, params=params_dict)
        res_str = res.text
        # 用eval函数转为字典对象
        res_dict = eval(res_str)
    # 二、请求的uri及数据，存入到日志表
    # 构建存入到数据收集日志表的df
    log_df = log_data_handle("MaoBo", "GET", url, str(params_dict), res_str)
    # 存入到数据收集日志表(这里日志表名暂时固定为data_collect_log)
    data_append_db(log_df, db_dict, "data_collect_log")
    # 三、判断请求发送状态并作异常处理
    if res.status_code == 200:
        # 如果返回数据内的状态码不等于200,则多为参数构建错误
        if res_dict["status"] != 200:
            print("返回的状态码为：%s" % str(res_dict["status"]))
            print("返回的信息为：%s" % res_dict["message"])
            raise ValueError("参数构建错误!")
        # 如果请求发送成功，没返回数据，则抛出异常
        elif (res_dict["status"] == 200) & (len(res_dict["content"]) == 0):
            raise ValueError("数据获取失败!")
        # 成功获取数据，以字典形式返回
        elif (res_dict["status"] == 200) & (len(res_dict["content"]) != 0):
            return res_dict
    # 如果status_code不等于200，则请求发送失败，抛出异常
    else:
        raise ValueError("请求发送失败!")

