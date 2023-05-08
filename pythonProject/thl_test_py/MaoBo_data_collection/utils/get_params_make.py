# -*- coding:utf-8 -*-
# @Author : Think
# @Date : 2023-04-14
# @File_name : get_params_make.py

from itertools import product
from thl_test_py.fun_sum.global_fun import DateList, MonthList
import datetime


class GetParamsMake():
    """
    方法的日期相关命名：
    YYYY-mm-dd命名为date
    YYYYmmdd命名为day
    """

    def __init__(self, url_dict, params_dict):
        """
        合并url_dict内的各值——url。
        :param url_dict: uri_params文件内定义的各个接口的url_dict
        :param params_dict: uri_params文件内定义的各个接口的params_dict
        """
        self.url = "".join(url_dict.values())
        self.params_dict = params_dict

    def one_day_param(self, day_param_name, start_date, end_date):
        """
        “只有一个日期参数（请求格式：YYYYmmdd）”的uri及各参数字典构造
        :param day_param_name: 日期参数的名称（字符串）
        :param start_date: 开始日期参数(YYYY-mm-dd 或 YYYYmmdd，字符串)
        :param end_date: 开始日期参数(YYYY-mm-dd 或 YYYYmmdd，字符串)
        :return: url 和 笛卡尔积后的参数字典的列表，组成的url_params_list列表
        结构：[uri, [{key_1: value_1, key_2: value_2,...}, {key_1: value_1, key_2: value_2,...}, ...]]
        """
        # 一、各params的各部分获取
        # 定义储存笛卡尔积后的参数字典的列表
        cart_pamams_dict_list = []
        # 定义存储日期区间内各个日参数(YYYYmmdd)的列表
        day_list = DateList(start_date, end_date).day_compute()
        # 定义存储参数名称的列表params_n_list
        params_n_list = []
        # 定义存储参数值的列表params_v_list（结构：[[],[],[]]，用于转为笛卡尔积）
        params_v_list = []
        # 先遍历params_dict插入到params_name_list和value_list
        for name, value in self.params_dict.items():
            params_n_list.append(name)
            params_v_list.append(value)
        # 最后插入传入的日期参数名称和参数(注：参数因itertools模块的product类，要构建成列表形式)
        params_n_list.append(day_param_name)
        params_v_list.append(day_list)
        # *号打开params_v_list最外层列表，调用itertools模块的product类，构建笛卡尔积的对象，再转为params_g_list列表
        params_g_list = list(product(*params_v_list))

        # 二、合并为每个参数字典
        for params_g in params_g_list:
            # 定义笛卡尔积后的参数字典，并用于重置字典值
            cart_pamams_dict = {}
            # 遍历名称和值后，添加到cart_pamams_dict，再添加到cart_pamams_dict_list
            for i in range(len(params_n_list)):
                cart_pamams_dict[params_n_list[i]] = params_g[i]
            cart_pamams_dict_list.append(cart_pamams_dict)
        # 构建只有“url”和“笛卡尔积后的参数字典的列表cart_pamams_dict_list”两个对象的url_params_list
        url_params_list = [self.url, cart_pamams_dict_list]
        return url_params_list

    def two_day_param(self, start_day_param_name, end_day_param_name, start_date, end_date):
        """
        “两个日期参数（请求格式：YYYYmmdd）”的uri及各参数字典构造
        :param start_day_param_name: 开始日期参数的名称（字符串）
        :param end_day_param_name: 结束日期参数的名称（字符串）
        :param start_date: 开始日期参数(YYYY-mm-dd 或 YYYYmmdd，字符串)
        :param end_date: 开始日期参数(YYYY-mm-dd 或 YYYYmmdd，字符串)
        :return: url 和 笛卡尔积后的参数字典的列表，组成的url_params_list列表
        结构：[uri, [{key_1: value_1, key_2: value_2,...}, {key_1: value_1, key_2: value_2,...}, ...]]
        """
        # 一、各params的各部分获取
        # 定义储存笛卡尔积后的参数字典的列表
        cart_pamams_dict_list = []
        # 将YYYY-mm-dd 转为 YYYYmmdd
        start_day = start_date.replace("-", "")
        # 因袤博数据接口，传20230301-20230303,会返回20230301-20230302的数据，所以此处+1天
        end_day = (datetime.datetime.strptime(end_date.replace("-", ""), '%Y%m%d') + datetime.timedelta(days=1)).strftime('%Y%m%d')
        # 定义存储参数名称的列表params_n_list
        params_n_list = []
        # 定义存储参数值的列表params_v_list（结构：[[],[],[]]，用于转为笛卡尔积）
        params_v_list = []
        # 先遍历params_dict插入到params_name_list和value_list
        for name, value in self.params_dict.items():
            params_n_list.append(name)
            params_v_list.append(value)
        # 最后插入传入的日期参数名称和参数(注：参数因itertools模块的product类，要构建成列表形式)
        params_n_list.append(start_day_param_name)
        params_v_list.append([start_day])
        params_n_list.append(end_day_param_name)
        params_v_list.append([end_day])
        # *号打开value_list最外层列表，调用itertools模块的product类，构建笛卡尔积的对象，再转为params_g_list列表
        params_g_list = list(product(*params_v_list))

        # 二、合并为每个参数字典
        for params_g in params_g_list:
            # 定义笛卡尔积后的参数字典，并用于重置字典值
            cart_pamams_dict = {}
            # 遍历名称和值后，添加到cart_pamams_dict，再添加到cart_pamams_dict_list
            for i in range(len(params_n_list)):
                cart_pamams_dict[params_n_list[i]] = params_g[i]
            cart_pamams_dict_list.append(cart_pamams_dict)
        # 构建只有“url”和“笛卡尔积后的参数字典的列表cart_pamams_dict_list”两个对象的url_params_list
        url_params_list = [self.url, cart_pamams_dict_list]
        return url_params_list

    def one_month_param(self, month_param_name, start_month, end_month):
        """
        “只有一个月份参数（请求格式：YYYYmmdd）”的uri及各参数字典构造
        :param month_param_name: 月份参数的名称（字符串）
        :param start_month: 开始月份参数(YYYY-mm 或 YYYYmm，字符串)
        :param end_month: 结束月份参数(YYYY-mm 或 YYYYmm，字符串)
        :return: url 和 笛卡尔积后的参数字典的列表，组成的url_params_list列表
        结构：[uri, [{key_1: value_1, key_2: value_2,...}, {key_1: value_1, key_2: value_2,...}, ...]]
        """
        # 一、各params的各部分获取
        # 定义储存笛卡尔积后的参数字典的列表
        cart_pamams_dict_list = []
        # 定义存储日期区间内各个月参数(YYYYmm)的列表
        month_list = MonthList(start_month, end_month).month_compute()
        # 定义存储参数名称的列表params_n_list
        params_n_list = []
        # 定义存储参数值的列表params_v_list（结构：[[],[],[]]，用于转为笛卡尔积）
        params_v_list = []
        # 先按顺序遍历params_dict插入到params_name_list和value_list
        for key, value in self.params_dict.items():
            params_n_list.append(key)
            params_v_list.append(value)
        # 最后插入传入的日期参数名称和参数(注：参数因itertools模块的product类，要构建成列表形式)
        params_n_list.append(month_param_name)
        params_v_list.append(month_list)
        # *号打开value_list最外层列表，调用itertools模块的product类，构建笛卡尔积的对象，再转为params_g_list列表
        params_g_list = list(product(*params_v_list))

        # 二、合并为每个参数字典
        for params_g in params_g_list:
            # 定义笛卡尔积后的参数字典，并用于重置字典值
            cart_pamams_dict = {}
            # 遍历名称和值后，添加到cart_pamams_dict，再添加到cart_pamams_dict_list
            for i in range(len(params_n_list)):
                cart_pamams_dict[params_n_list[i]] = params_g[i]
            cart_pamams_dict_list.append(cart_pamams_dict)
        # 构建只有“url”和“笛卡尔积后的参数字典的列表cart_pamams_dict_list”两个对象的url_params_list
        url_params_list = [self.url, cart_pamams_dict_list]
        return url_params_list


