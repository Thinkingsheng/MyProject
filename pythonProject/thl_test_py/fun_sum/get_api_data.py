# -*- coding:utf-8 -*-

import json
import requests
from urllib.parse import quote
import pandas as pd


def get_gcj02_lnglat(add):
    """
    调用高德地图地址转(gcj02坐标系)经纬度API
    :param add:详细地址（str）
    :return:(gcj02坐标系)经纬度(格式：lng,lat; 字符串)
    """
    url = 'https://restapi.amap.com/v3/geocode/geo'
    appkey = '3bdd27040c132577c1b8135db6690f50'
    uri = url + '?' + 'address=' + add + '&output=JSON&' + 'key=' + appkey
    res = requests.get(uri).text
    temp = json.loads(res)
    gcj02_lnglat = temp['geocodes'][0]['location']
    return gcj02_lnglat


def get_bd09_lnglat(add):
    """
    调用百度地图地址转(bd09坐标系)经纬度API
    :param add:详细地址（str）
    :return:(bd09坐标系)经纬度(格式：lng,lat; 字符串)
    """
    url = 'https://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    # 百度地图ak，具体申请自行百度，提醒需要在“控制台”-“设置”-“启动服务”-“正逆地理编码”，启动
    ak = 'sh9oB4QXuzFYzHx6B36piF4N7essH2o0'
    add = quote(add)  # 由于本文地址变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak + '&callback=showLocation%20' + '//GET%E8%AF%B7%E6%B1%82'
    # 这种方式也可以，和下面的效果一样，都是返回json格式
    # req = urlopen(uri)
    # res = req.read().decode()
    res = requests.get(uri).text
    # 将字符串转化为json
    temp = json.loads(res)
    lng = temp['result']['location']['lng']
    lat = temp['result']['location']['lat']
    # 经度 longitude, 纬度 latitude
    return str(round(lng, 6)) + "," + str(round(lat, 6))


def transform_coords(coords, from_type, to_type):
    """
    调用百度地图 API 进行地图坐标系转换
    :param coords:需转换的源坐标(传入格式：经度，纬度【字符串】)，多组坐标以“;”分隔
    :param from_type:传入格式可为int。具体参数见文档：https://lbsyun.baidu.com/index.php?title=webapi/guide/changeposition
    :param to_type:传入格式可为int。具体参数见文档：https://lbsyun.baidu.com/index.php?title=webapi/guide/changeposition
    :return:转换后的坐标(传出格式：经度，纬度【字符串】)
    """
    url = 'https://api.map.baidu.com/geoconv/v1/'
    # 百度地图ak，具体申请自行百度，提醒需要在“控制台”-“设置”-“启动服务”-“正逆地理编码”，启动
    ak = 'sh9oB4QXuzFYzHx6B36piF4N7essH2o0'
    uri = url + '?' + 'coords=' + coords + '&from=' + str(from_type) + '&to=' + str(to_type) + '&ak=' + ak
    res = requests.get(uri).text
    temp = json.loads(res)
    lng = temp['result'][0]['x']
    lat = temp['result'][0]['y']
    return str(round(lng, 6)) + ',' + str(round(lat, 6))


def get_epidemic_area_str(date, type_str):
    """
    调用天行数据API，获取高中低风险的疫情地区数（数据源暂不可用）
    :param date: 日期(YYYY-MM-DD)字符串
    :param type_str: 风险地区(high,mid,low等)字符串
    :return:高中低风险的疫情地区数
    """
    url = 'http://api.tianapi.com/ncov/index'
    appkey = '643c46be55bbfee4be1a7024837b1ee7'
    uri = url + '?' + 'key=' + appkey + '&date=' + date
    res = requests.get(uri).text
    temp = json.loads(res)
    area_list = temp['newslist'][0]['riskarea'][type_str]
    gz_area = []
    for a in area_list:
        if (a.find("广东省") >= 0) & (a.find("广州") >= 0):
            gz_area.append(a)
        else:
            pass
    gz_area_str = str(len(gz_area)) + '&'
    for gz_a in gz_area:
        gz_area_str = gz_area_str + gz_a + ';'
    return gz_area_str


def get_holiday_str(date):
    """
    调用日期接口，获取假期等信息，详情链接：https://blog.csdn.net/u012981882/article/details/112552450
    :param date:日期（格式:YYYY-MM-DD或YYYYMMDD）字符串
    :return:“是否工作日_节假日_节假日2_是否节日当天_是否假期节假日”字符串
    """
    date_str = date.replace("-", "")
    url = 'https://api.apihubs.cn/holiday/get'
    uri = url + '?' + '&date=' + date_str + '&cn=1'
    res = requests.get(uri).text
    temp = json.loads(res)
    if temp['data']['list'][0]['holiday_cn'] == temp['data']['list'][0]['holiday_or_cn']:
        holiday_cn = temp['data']['list'][0]['workday_cn'] + '_' + temp['data']['list'][0]['holiday_cn'] + '_' + '_' + \
                     temp['data']['list'][0]['holiday_today_cn'] + '_' + temp['data']['list'][0]['holiday_recess_cn']
    else:
        holiday_cn = temp['data']['list'][0]['workday_cn'] + '_' + temp['data']['list'][0]['holiday_cn'] + '_' + \
                     temp['data']['list'][0]['holiday_or_cn'] + '_' + temp['data']['list'][0]['holiday_today_cn'] \
                     + '_' + temp['data']['list'][0]['holiday_recess_cn']
    return holiday_cn


def get_full_holiday_desc(date):
    """
    （主要用于测试）
    调用日期接口，获取假期等信息，详情链接：https://blog.csdn.net/u012981882/article/details/112552450
    :param date:日期（格式:YYYY-MM-DD或YYYYMMDD）字符串
    :return:假期等所有信息详情
    """
    date_str = date.replace("-", "")
    url = 'https://api.apihubs.cn/holiday/get'
    uri = url + '?' + '&date=' + date_str + '&cn=1'
    res = requests.get(uri).text
    temp = json.loads(res)
    return temp


def get_weather_str(date):
    """
    调用进制数据API，获取天气数据，详情链接：https://www.binstd.com/api/weather2.html
    :param date: 日期(格式：YYYY-MM-DD或YYYYMMDD)字符串
    :return: 返回天气字符串
    """
    date_str = date.replace("-", "")
    url = 'https://api.binstd.com/weather2/query'
    appkey = '7bab5299b28b4a58'
    uri = url + '?' + 'appkey=' + appkey + '&city=广州' + '&date=' + date_str
    res = requests.get(uri).text
    temp = json.loads(res)
    wt_status = temp['result']['weather']
    return wt_status


def get_temp_str(date):
    """
    调用进制数据API，获取天气数据，详情链接：https://www.binstd.com/api/weather2.html
    :param date: 日期(格式：YYYY-MM-DD或YYYYMMDD)字符串
    :return: 返回最高气温和最低气温(格式：最高气温,最低气温)字符串
    """
    date_str = date.replace("-", "")
    url = 'https://api.binstd.com/weather2/query'
    appkey = '7bab5299b28b4a58'
    uri = url + '?' + 'appkey=' + appkey + '&city=广州' + '&date=' + date_str
    res = requests.get(uri).text
    temp = json.loads(res)
    temps = temp['result']['temphigh'] + "," + temp['result']['templow']
    return temps


def get_epidemic_data(date):
    """
    定义获取百度的疫情数据函数
    :param date: 单个日期YYYY-MM-DD的字符串
    :return: 疫情新增数据的dataframe
    """
    # 百度疫情数据源：https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner&city=%E5%B9%BF%E4%B8%9C-%E5%B9%BF%E5%B7%9E
    url = 'https://voice.baidu.com/newpneumonia/getv2?from=mola-virus&stage=publish&target=trendCity&area=%E5%B9%BF%E4%B8%9C-%E5%B9%BF%E5%B7%9E&callback=jsonp_1666661306020_75644'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    response_data = json.loads(res.text.replace('jsonp_1666661306020_75644(', '').replace(';', '')[:-1])["data"]
    # 转为dataframe
    epidemic_data = pd.DataFrame(
        {
            '新增无症状': response_data[0]['trend']['list'][0]['data'],
            '新增本土': response_data[0]['trend']['list'][1]['data']
        },
        # 设数据更新日期为索引(格式:Y.M)
        index=response_data[0]['trend']['updateDate'])

    # 按返回数据的日期格式作处理，如09-01处理为9.1
    if date[5:7][0:1] == "0":
        month_str = date[5:7][1:2]
    else:
        month_str = date[5:7]
    if date[8:][0:1] == "0":
        day_str = date[8:][1:2]
    else:
        day_str = date[8:]
    date_str = month_str + "." + day_str

    # 获取新增本土+新增无症状人数，没有则返回None
    try:
        new_epidemic_count = epidemic_data.loc[date_str, '新增本土'] + epidemic_data.loc[date_str, '新增无症状']
    except KeyError:
        new_epidemic_count = None

    output_data = pd.DataFrame(
        {
            # 此处要转为列表形式
            'date': [date],
            'city_epidemic_count': [new_epidemic_count]
        })
    return output_data


def get_holiday_data(date):
    """
    定义获取假期数据函数
    :param date: 单个日期YYYY-MM-DD的字符串
    :return:假期数据的dataframe
    """
    # 文档链接：https://blog.csdn.net/u012981882/article/details/112552450
    date_str = date.replace("-", "")
    url = 'https://api.apihubs.cn/holiday/get'
    uri = url + '?' + '&date=' + date_str + '&cn=1'
    res = requests.get(uri).text
    temp = json.loads(res)

    # 处理各字段数据
    if temp['data']['list'][0]['workday_cn'] == "工作日":
        work_day = 1
    else:
        work_day = 0

    if temp['data']['list'][0]['holiday_today_cn'] == "节日当天":
        festival_today = 1
    else:
        festival_today = 0

    if temp['data']['list'][0]['holiday_recess_cn'] == "假期节假日":
        holiday_festival = 1
    else:
        holiday_festival = 0

    if temp['data']['list'][0]['holiday_cn'] == temp['data']['list'][0]['holiday_or_cn']:
        festival_or = ''
    else:
        festival_or = temp['data']['list'][0]['holiday_or_cn']

    output_data = pd.DataFrame(
        {
            # 此处要转为列表形式
            'date': [date],
            'week_num': [temp['data']['list'][0]['week_cn'].replace("星期", "周")],
            'work_day': [work_day],
            'festival': [temp['data']['list'][0]['holiday_cn']],
            'festival_or': [festival_or],
            'festival_today': [festival_today],
            'holiday_festival': [holiday_festival]
        })
    return output_data


def get_weather_data(date):
    """
    定义获取天气数据函数
    :param date: 单个日期YYYY-MM-DD的字符串
    :return:天气数据的dataframe
    """
    # 文档链接（聚合数据）：https://www.juhe.cn/docs/api/id/716
    url = 'http://v.juhe.cn/hisWeather/weather'
    appkey = '636674fa734449ff8c8a8c211d6ade6c'
    # city_id的获取需调用同一个tab的另外两个接口
    uri = url + '?' + 'key=' + appkey + '&city_id=265' + '&weather_date=' + date
    res = requests.get(uri).text
    temp = json.loads(res)
    output_data = pd.DataFrame(
        {
            # 此处要转为列表形式
            'date': [date],
            'weather': temp['result']['day_weather']
        })
    return output_data
