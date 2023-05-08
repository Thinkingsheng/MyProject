# -*- coding:utf-8 -*-

import os
import datetime
from dateutil.relativedelta import relativedelta


def get_files(path):
    for root, dirs, files in os.walk(path):
        print('root_dir:', root)  # 当前路径
        print('files:', files)  # 文件名称，返回list类型
    return files


class DateList():

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def date_compute(self):
        """
        输入：开始日期YYYY-MM-DD(或 YYYYMMDD), 结束日期YYYY-MM-DD(或 YYYYMMDD)
        输出：[YYYY-MM-DD, ...]
        """
        # 统一转为'%Y%m%d'的日期后，转为时间
        date_start = datetime.datetime.strptime(self.start_date.replace("-", ""), '%Y%m%d')
        date_end = datetime.datetime.strptime(self.end_date.replace("-", ""), '%Y%m%d')
        date_list = []
        while date_start <= date_end:
            # 将时间转为'%Y-%m-%d'的日期
            date_value = date_start.strftime('%Y-%m-%d')
            date_list.append(date_value)
            date_start += datetime.timedelta(days=1)
        return date_list

    def day_compute(self):
        """
        输入：开始日期YYYY-MM-DD(或 YYYYMMDD), 结束日期YYYY-MM-DD(或 YYYYMMDD)
        输出：[YYYYMMDD, ...]
        """
        # 统一转为'%Y%m%d'的日期后，转为时间
        date_start = datetime.datetime.strptime(self.start_date.replace("-", ""), '%Y%m%d')
        date_end = datetime.datetime.strptime(self.end_date.replace("-", ""), '%Y%m%d')
        date_list = []
        while date_start <= date_end:
            # 将时间转为'%Y%m%d'的日期
            date_value = date_start.strftime('%Y%m%d')
            date_list.append(date_value)
            date_start += datetime.timedelta(days=1)
        return date_list


def year_week_dict(start_year, start_week, end_year, end_week):
    """
    将开始和结束（年份.周数）的区间，转为字典（无序）
    :param start_year: 开始年份(int或str都可)
    :param start_week: 开始周数(int或str都可)
    :param end_year: 结束年份(int或str都可)
    :param end_week: 结束周数(int或str都可)
    :return:
    {
    开始年份(int):[1,2,3,4...(int)],
    ...
    结束年份(int):[1,2,3,4...(int)]
    }
    """
    # 存储完整年份&周数的字典
    full_dict = {}
    # 区间为当前年的处理
    if (start_year == end_year) and (end_week > start_week):
        # 直接获取开始周和结束周的序列表
        week_list = range(int(start_week), int(end_week)+1)
        full_dict = {int(start_year): week_list}
    elif (start_year == end_year) and (end_week == start_week):
        week_list = [int(start_week)]
        full_dict = {int(start_year): week_list}
    # 区间为跨年的处理
    elif start_year < end_year:
        # 先遍历年份
        for year_num in range(int(start_year), int(end_year)+1):
            # 判断是否首年
            if year_num == int(start_year):
                # 获取该年的最大周数
                cur_end_week = datetime.datetime(year_num, 12, 31).isocalendar()[1]
                # 用（开始周数,最大周数）构建该年的序列表
                cur_week_list = range(int(start_week), int(cur_end_week)+1)
                full_dict[year_num] = cur_week_list
            # 判断是否中间的年份
            elif (year_num > int(start_year)) & (year_num < int(end_year)):
                cur_end_week = datetime.datetime(year_num, 12, 31).isocalendar()[1]
                # 用（1,最大周数）构建该年的序列表
                cur_week_list = range(1, int(cur_end_week)+1)
                full_dict[year_num] = cur_week_list
            # 判断是否尾年
            elif year_num == int(end_year):
                # 用（1,结束周数）构建该年的序列表
                cur_week_list = range(1, int(end_week)+1)
                full_dict[year_num] = cur_week_list
    else:
        print("输入参数有误！")
    return full_dict


class MonthList():

    def __init__(self, start_month_str, end_month_str):
        """
        :param start_month_str: 开始月份字符串：YYYY-MM
        :param end_month_str: 结束月份字符串：YYYY-MM
        """
        self.start_month_str = start_month_str
        self.end_month_str = end_month_str

    def month_compute(self):
        """
        :return: 月份字符串列表：[YYYYMM, ...]
        """
        start_month_time = datetime.datetime.strptime(self.start_month_str.replace("-", ""), '%Y%m')
        end_month_time = datetime.datetime.strptime(self.end_month_str.replace("-", ""), '%Y%m')
        month_list = []
        while start_month_time <= end_month_time:
            month_str = start_month_time.strftime('%Y%m')
            month_list.append(month_str)
            start_month_time = start_month_time + relativedelta(months=1)
        return month_list


class DateChange():
    """
    将传入日期进行转换
    """
    def __init__(self, date_str):
        """
        :param date_str: 日期字符串(YYYY-MM-DD 或 YYYYMMDD)
        """
        self.date_str = date_str

    def last_month_date(self):
        """
        获取上月日期
        :return: 日期字符串(YYYY-MM-DD)
        """
        # 将'%Y-%m-%d'的日期转为时间
        date_time = datetime.datetime.strptime(self.date_str.replace("-", ""), '%Y%m%d')
        # 月加减用dateutil.relativedelta.relativedelta
        date_time = date_time - relativedelta(months=1)
        date_value = date_time.strftime('%Y-%m-%d')
        return date_value

    def last_week_date(self):
        """
        获取上周日期
        :return: 日期字符串(YYYY-MM-DD)
        """
        # 将'%Y-%m-%d'的日期转为时间
        date_time = datetime.datetime.strptime(self.date_str.replace("-", ""), '%Y%m%d')
        # 日加减用datetime.timedelta
        date_time = date_time - datetime.timedelta(days=7)
        date_value = date_time.strftime('%Y-%m-%d')
        return date_value

    def last_day_date(self):
        """
        获取昨日日期
        :return: 日期字符串(YYYY-MM-DD)
        """
        # 将'%Y-%m-%d'的日期转为时间
        date_time = datetime.datetime.strptime(self.date_str.replace("-", ""), '%Y%m%d')
        date_time = date_time - datetime.timedelta(days=1)
        date_value = date_time.strftime('%Y-%m-%d')
        return date_value


class CurrentTimeTrans():
    """
    将当前时间进行转换
    """
    def __init__(self):
        self.now = datetime.datetime.now()

    def get_end_date(self):
        """
        定义获取“当前日期-1天”函数（T-1获取数据）
        :return:end_date（T-1日期YYYY-MM-DD的字符串）
        """
        end_date = (self.now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        return end_date

    def get_current_date(self):
        """
        定义获取“当前日期”函数
        :return:current_date（当前日期YYYY-MM-DD的字符串）
        """
        current_date = self.now.strftime("%Y-%m-%d")
        return current_date

    def get_current_month(self):
        """
        定义获取“当前月份”函数
        :return:current_month（当前月份mm的字符串）
        """
        current_month = self.now.strftime("%m")
        return current_month

    def get_current_year(self):
        """
        定义获取“当前年份”函数
        :return:current_year（当前年份YYYY的字符串）
        """
        current_year = self.now.strftime("%Y")
        return current_year


class T_1TimeTrans():
    """
    将T-1时间进行转换
    """
    def __init__(self):
        self.t_1_time = datetime.datetime.now() - datetime.timedelta(days=1)

    def get_t_1_date_year(self):
        """
        获取“当前日期-1天的年份”函数
        :return:t_1_date_year（T-1日期的年份YYYY的字符串）
        """
        t_1_date_year = self.t_1_time.strftime("%Y")
        return t_1_date_year

    def get_t_1_date_last_year(self):
        """
        获取“当前日期-1天的上一年年份”函数
        :return:t_1_date_last_year（T-1日期的年份YYYY的字符串）
        """
        t_1_date_last_year = (self.t_1_time - relativedelta(years=1)).strftime("%Y")
        return t_1_date_last_year


def irregular_date_trans(date_str, year_str_fun=T_1TimeTrans().get_t_1_date_year()):
    """
    不规则的日期字符串转换（将 “传入的X月X日” 结合 “T-1日期的年份”，转为 %Y%m%d）
    :param year_str_fun: 返回年份字符串的函数（默认为“T-1日期的年份”）
    :param date_str: "X月X日"字符串
    :return: 日期字符串（%Y-%m-%d）
    """
    # 调用T_1TimeTrans类的get_t_1_date_year()函数获取T-1日期的年份，并合并
    full_date_str = year_str_fun + "年" + date_str
    time_value = datetime.datetime.strptime(full_date_str, "%Y年%m月%d日")
    return time_value.strftime("%Y-%m-%d")
