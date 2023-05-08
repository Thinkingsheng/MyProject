# -*- coding:utf-8 -*-
# @Author : Think
# @Date : 2023-03-31
# @File_name : http_post_data.py
import datetime

import httpx
import pandas as pd
from thl_test_py.fun_sum.global_fun import T_1TimeTrans
from thl_test_py.fun_sum.global_fun import irregular_date_trans
from time import sleep
from collections import OrderedDict
from thl_test_py.fun_sum.global_fun import DateList


def http_post_weibo_data(start_date, end_date):
    """
    按日期区间，获取微博指数的数据，对应链接：https://data.weibo.com/index/newindex
    :param start_date: 开始日期（字符串，YYYY-mm-dd）
    :param end_date: 结束日期（字符串，YYYY-mm-dd）
    :return: dataframe（字段：日期,商综名，指数）
    """
    # 一、数据获取部分
    url = "https://data.weibo.com/index/ajax/newindex/getchartdata"
    # 商综体搜索词:[在该链接上传参的wid, headers的content-Length]的有序字典
    mall_wid_dict = OrderedDict()
    mall_wid_dict["ZJGC"] = [1091324231586, '34']
    mall_wid_dict["TGH"] = None
    mall_wid_dict["THC"] = [1011652601742, '34']
    mall_wid_dict["THGC"] = None
    mall_wid_dict["WDLGC"] = None
    mall_wid_dict["WLH"] = [120200901194031621324, '42']
    # # “商综体搜索词”与“存入的source字段值”的映射字典
    # mall_source_dict = {
    #     "正佳广场": "ZJGC",
    #     "太古汇": "TGH",
    #     "天河城": "THC",
    #     "天环广场": "THGC",
    #     "维多利广场": "WDLGC",
    #     "万菱汇": "WLH"
    # }
    # # ”中文日期范围“与“在该链接上传参的daterange”的映射字典
    # datestr_range_dict = {
    #     "90天": "3month",
    #     "30天": "1month",
    #     "24小时": "1day",
    #     "1小时": "1hour"
    # }
    # 构造headers和cookies
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-Type': 'application/x-www-form-urlencoded',
        'origin': 'https://data.weibo.com',
        'referer': 'https://data.weibo.com/index/newindex?visit_type=trend&wid=1091324231586',
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'
    }
    cookies = {
        'Cookies': 'SUB=_2AkMUfOTDf8NxqwJRmP4RzGPrbY5xzQzEieKiIBUYJRMxHRl-yT92qmgOtRB6P_zKLABFMpd9VZN47gIOV5-c1dl2HN6x; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5xbpEUDTAXT_1inllEzqaT; UOR=www.baidu.com,weibo.com,www.baidu.com; SINAGLOBAL=6362297338908.294.1668313263010; ULV=1668994531566:2:2:1:73990765834.7927.1668994531561:1668313263013; WEB3=cbf0c0854ffc0231c62d06ce4d64c2cf'
    }
    # 定义存储所有商综的df的字典
    sub_df_dict = {}
    # 利用start_date和end_date两个传参，到Data_list类获取日期区间列表
    param_date_list = DateList(start_date, end_date).date_compute()
    for mall_name, wid_list in mall_wid_dict.items():
        # 处理非空部分的商综
        if wid_list is not None:
            # post body内支持查询的日期范围（1小时、24小时、30天、90天），默认查近3个月
            data = {"wid": wid_list[0], "dateGroup": "3month"}
            # 传入'content-Length'参数
            headers['content-Length'] = wid_list[1]
            # 使用支持http2的httpx的Client对象
            with httpx.Client(http2=True) as client:
                res = client.post(url, headers=headers, cookies=cookies, data=data)
                text_start_index = res.text.index("data") + 6
                text_end_index = res.text.index("html") - 2
                # 按索引截取处理“返回结果字符串”
                res_str = res.text[text_start_index:text_end_index]
                res_list = eval(res_str)
            # 二、数据处理部分
            date_str_list = res_list[0]["trend"]["x"]
            value_list = res_list[0]["trend"]["s"]
            date_list = []
            # 对于跨年的处理，先检验区间内是否存在1月1日，存在则返回对应index，不存在则返回-1
            try:
                diff_year_index = date_str_list.index("1月1日")
            except ValueError:
                diff_year_index = -1
            # 如果没有跨年的情况，则均当做T-1天日期的年份处理：
            if diff_year_index == -1:
                # 遍历"X月X日"的date_str_list列表，转为"%Y%m%d"的b_date_list列表
                for date_str in date_str_list:
                    # 调用irregular_date_trans函数转换日期字符串为%Y%m%d（该函数默认当做T-1天日期的年份处理），并插入到b_date_list
                    date_list.append(irregular_date_trans(date_str))
            # 如果有跨年的情况：
            else:
                # 先处理上一年的日期，调用irregular_date_trans函数，结合T-1天日期的上一年年份，转换为%Y%m%d存入
                for l_year_date_index in range(diff_year_index):
                    date_list.append(irregular_date_trans(date_str_list[l_year_date_index],
                                                          T_1TimeTrans().get_t_1_date_last_year()))
                # 再处理今年的日期
                for year_date_index in range(diff_year_index, len(date_str_list)):
                    date_list.append(irregular_date_trans(date_str_list[year_date_index]))
            # 三、数据整合部分
            only_mall_df = pd.DataFrame(
                {
                    "date": date_list,
                    # 将mall_source_dict的商综名称转为小写，然后作为列名生成每个df
                    "%s_index" % mall_name.lower(): value_list
                }
            )
            # 按date区间为条件取df
            sub_df = only_mall_df.loc[(only_mall_df['date'] >= start_date) & (only_mall_df['date'] <= end_date)]
            # key:商综缩写,value:df，插入到sub_df_dict
            sub_df_dict[mall_name] = sub_df
            sleep(2)
        else:
            value_list = [None] * len(param_date_list)
            only_mall_df = pd.DataFrame(
                {
                    "date": param_date_list,
                    # 将mall_source_dict的商综名称转为小写，然后作为列名生成每个df
                    "%s_index" % mall_name.lower(): value_list
                }
            )
            # key:商综缩写,value:None，插入到sub_df_dict(此处因空数据是基于完整的param_date_list构造的，所以不用按date条件取df，直接插入only_mall_df)
            sub_df_dict[mall_name] = only_mall_df
            sleep(2)
    # 四、各df连表
    # 定义汇总的df（只新建date列和type列，是作索引作用）
    full_data = pd.DataFrame(
        {
            "date": param_date_list,
            "type": ["WB"] * len(param_date_list)
        }
    )
    # 将sub_df_dict内各商综的df，合并到full_data
    for mall_name in mall_wid_dict.keys():
        sub_df = sub_df_dict[mall_name]
        full_data = pd.merge(full_data, sub_df, on='date', how='left')
    # 定义结尾数据df，再合并
    end_df = pd.DataFrame(
        {
            "date": param_date_list,
            "last_edit_user": [None] * len(param_date_list),
            "last_edit_time": [None] * len(param_date_list)
        }
    )
    #
    end_df["last_edit_time"] = pd.to_datetime(end_df["last_edit_time"])
    full_data = pd.merge(full_data, end_df, on='date', how='left')
    # 重置df索引
    full_data = full_data.reset_index(drop=True)
    return full_data
