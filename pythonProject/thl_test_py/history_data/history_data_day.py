# -*- coding:utf-8 -*-

import requests
from thl_test_py.fun_sum.global_fun import DateList


# 请求4. 时段内客群到访时长分布. 获取指定日期最近7天到访驻留时间
# dm_stay_days_day
def get_duration_day(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/flow/duration?date=@@"
    print("开始插入到 dm_stay_days_day 表：")
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


# 请求7. 客群品牌和业态偏好画像，获取指定日期客群品牌和业态偏好画像(能取到20210101)
# dm_consumer_brand_favour_day
def get_brand_image_day(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/image/brand/day?date=@@"
    print("开始插入到 dm_consumer_brand_favour_day 表：")
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


# 请求6和10. 6.客群基础画像/10.酒旅出行画像.获取指定月份客群基础画像
# dm_consumer_image_day
def get_image_day(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/image/consumer/day?date=@@"
    print("开始插入到 dm_consumer_image_day 表：")
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


# 请求9. 地理属性，获取指定日期热力图
# dm_district_image_geo_heatmap_day
def get_geo_heatmap_day(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/tourism/image/geo/heatmap/day?date=@@"
    print("开始插入到 dm_district_image_geo_heatmap_day 表：")
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


# 请求9. 地理属性，获取指定日期分布占比
# dm_district_image_geo_day
def get_geo_day(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/tourism/image/geo/percent/day?date=@@"
    print("开始插入到 dm_district_image_geo_day 表：")
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


# 请求11. 网络行为，获取指定日期网络行为画像
# dm_consumer_network_image_day
def get_network_image_day(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/image/network/day?date=@@"
    print("开始插入到 dm_consumer_network_image_day 表：")
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


# 请求14. 实时到访客流量，调用接口15补历史的数据
# dm_realtime_flow_arrive_hour
def get_realtime_day(date_list):
    uri_all = "http://test-tinhotown.tianheroad.com:8084/jk/flow/supplementRealTimeFLowByHistoryFlow?dateStr=@@&source=all"
    uri_mall = "http://test-tinhotown.tianheroad.com:8084/jk/flow/supplementRealTimeFLowByHistoryFlow?dateStr=@@&source=mall"
    print("开始插入到 dm_realtime_flow_arrive_hour 表：")
    for date_value in date_list:
        uri_all_r = uri_all.replace("@@", date_value)
        uri_mall_r = uri_mall.replace("@@", date_value)
        res = requests.get(uri_all_r).text
        print(res + " : " + date_value + " ——导入完成！")
        res = requests.get(uri_mall_r).text
        print(res + " : " + date_value + " ——导入完成！")


# 请求15. 历史到访客流量. 获取指定日期(及小时)历史客流量
# dm_consumer_flow_arrive_day
# dm_consumer_flow_arrive_hour
def get_arrive_day(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/flow/arrive/day?day=@@"
    print("开始插入到 dm_consumer_flow_arrive_day/dm_consumer_flow_arrive_hour 表：")
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


# 请求19. 小时分段到访分布. 获取小时分段到访分布
# dm_stay_duration_day
def get_duration_hour_day(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/flow/duration/hour?day=@@"
    print("开始插入到 dm_stay_duration_day 表：")
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


# 请求101. 小时分段到访分布. 获取小时分段到访分布
# dm_poi_image_day
def get_poi_image_day(date_list):
    uri = "http://test-tinhotown.tianheroad.com:8084/jk/flow/sourcePoiDay?day=@@"
    print("开始插入到 dm_poi_image_day 表：")
    for date_value in date_list:
        uri_r = uri.replace("@@", date_value)
        res = requests.get(uri_r).text
        print(res + " : " + date_value + " ——导入完成！")


# # 请求. 第三方天气接口. 获取指定日期天气数据
# # dim_realtime_weather_data_hour
# # dim_weather_data_day
# def get_weather_day(date_list):
#     uri = "http://test-tinhotown.tianheroad.com:8084/jk/weather/history?dayStr=@@"
#     for date_value in date_list:
#         uri_r = uri.replace("@@", date_value)
#         res = requests.get(uri_r).text
#         print(res + " : " + date_value + " ——导入完成！")
#         sleep(2)


# 调用Data_list类获取日期区间列表
history_date_range = DateList('2023-01-01', '2023-03-02').date_compute()


# # 调用各自函数
# get_duration_day(history_date_range)
# get_brand_image_day(history_date_range)
# get_image_day(history_date_range)
# get_geo_heatmap_day(history_date_range)
# get_geo_day(history_date_range)
# get_network_image_day(history_date_range)
# # get_arrive_day(history_date_range)
# get_duration_hour_day(history_date_range)
# # get_weather_day(history_date_range)
get_poi_image_day(history_date_range)



