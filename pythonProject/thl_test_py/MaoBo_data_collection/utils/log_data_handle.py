# -*- coding:utf-8 -*-
# @Author : Think
# @Date : 2023-05-04
# @File_name : log_data_handle.py

import datetime
import pandas as pd


def log_data_handle(source_str, request_type, uri, request_params, respond_str):
    """
    导入到日志表data_collect_log的df构建
    :param source_str: 数据源名称的字符串
    :param request_type: 请求类型的字符串("get","POST"等)
    :param uri: 完整的请求uri
    :param respond_str: 完整的回应数据字符串
    :param request_params: 请求的参数(GET请求存储参数字典；POST请求存储body)
    :return: 构建好的dataframe
    """
    log_df = pd.DataFrame(
        {
            "data_source": [source_str],
            "request_time": [datetime.datetime.now()],
            "type": [request_type],
            "request_full_uri": [uri],
            "request_params": [request_params],
            "respond": [respond_str]
         }
    )
    return log_df



