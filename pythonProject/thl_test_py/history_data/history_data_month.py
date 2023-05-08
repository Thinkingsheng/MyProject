# -*- coding:utf-8 -*-

import requests
from thl_test_py.fun_sum.global_fun import MonthList


# 请求7. 客群品牌和业态偏好画像，获取指定月份客群品牌和业态偏好画像(能取到202101)
# dm_consumer_brand_favour_month
def get_brand_image_month(month_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/image/brand/month?month=@@"
    for month_value in month_list:
        uri_r = uri.replace("@@", month_value)
        res = requests.get(uri_r).text
        print(res + " : " + month_value + " ——导入完成！")


# 请求6和10. 6.客群基础画像/10.酒旅出行画像.获取指定月份客群基础画像
# dm_consumer_image_month
def get_image_month(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/image/consumer/month?month=@@"
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


# 请求11. 网络行为，获取指定月份网络行为画像
# dm_consumer_network_image_month
def get_network_image_month(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/image/network/month?month=@@"
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


# 请求9. 地理属性，获取指定月份热力图
# dm_district_image_geo_heatmap_month
def get_geo_heatmap_month(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/tourism/image/geo/heatmap/month?date=@@"
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


# 请求9. 地理属性，获取指定月份分布占比
# dm_district_image_geo_month
def get_geo_month(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/tourism/image/geo/percent/month?date=@@"
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


# 请求206. 商圈客流外溢统计. 获取指定月份商圈客流外溢情况
# dm_district_spillover_month
def get_district_spillover_month(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/spillover/month?month=@@"
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


history_month_range = MonthList('2023-01', '2023-01').month_compute()
print(history_month_range)


# get_brand_image_month(history_month_range)
get_image_month(history_month_range)
# get_network_image_month(history_month_range)
# get_geo_month(history_month_range)
# get_district_spillover_month(history_month_range)

