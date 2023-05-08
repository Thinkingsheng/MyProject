# -*- coding:utf-8 -*-

import requests
from time import sleep
from thl_test_py.fun_sum.global_fun import year_week_dict


# 请求301.POI业态偏好
# dm_mall_b_type_favour_week
def get_mall_b_type_favour_week(year_week_dict):
    for year_num, week_list in year_week_dict.items():
        for week_num in week_list:
            uri = "http://test-tinhotown.tianheroad.com:8084/jk/flow/poiPreferencesCate?week=%s&year=%s" \
                  % (str(week_num), str(year_num))
            res = requests.get(uri).text
            print(res + " —— " + str(year_num) + "-" + str(week_num) + " ——导入完成！")
            sleep(2)


# 请求302.全域二级业态占比
# dm_business_b_type_favour_week
def get_business_b_type_favour_week(year_week_dict):
    for year_num, week_list in year_week_dict.items():
        for week_num in week_list:
            uri = "http://test-tinhotown.tianheroad.com:8084/jk/flow/populationRatio?week=%s&year=%s" \
                  % (str(week_num), str(year_num))
            res = requests.get(uri).text
            print(res + " —— " + str(year_num) + "-" + str(week_num) + " ——导入完成！")
            sleep(2)


# 请求303.全域二级业态品牌TOP30
# dm_business_b_type_brand_top30_week
def get_business_b_type_brand_top30_week(year_week_dict):
    for year_num, week_list in year_week_dict.items():
        for week_num in week_list:
            uri = "http://test-tinhotown.tianheroad.com:8084/jk/flow/preferencesBrandTop30?week=%s&year=%s" \
                  % (str(week_num), str(year_num))
            res = requests.get(uri).text
            print(res + " —— " + str(year_num) + "-" + str(week_num) + " ——导入完成！")
            sleep(2)


# 请求304.POI业态客流贡献TOP30门店
# dm_mall_b_type_brand_top30_week
def get_mall_b_type_brand_top30_week(year_week_dict):
    for year_num, week_list in year_week_dict.items():
        for week_num in week_list:
            uri = "http://test-tinhotown.tianheroad.com:8084/jk/flow/preferencesContributionTop30?week=%s&year=%s" \
                  % (str(week_num), str(year_num))
            res = requests.get(uri).text
            print(res + " —— " + str(year_num) + "-" + str(week_num) + " ——导入完成！")
            sleep(2)


# 请求305.全域外地客群TOP30门店
# dm_tourist_b_type_brand_top30_week
def get_tourist_b_type_brand_top30_week(year_week_dict):
    for year_num, week_list in year_week_dict.items():
        for week_num in week_list:
            uri = "http://test-tinhotown.tianheroad.com:8084/jk/flow/preferencesCustomerTop30?week=%s&year=%s" \
                  % (str(week_num), str(year_num))
            res = requests.get(uri).text
            print(res + " —— " + str(year_num) + "-" + str(week_num) + " ——导入完成！")
            sleep(2)


# 调用year_week_dict函数获取周期区间列表
history_week_range = year_week_dict("2023", "14", "2023", "14")
print(history_week_range)

# 调用各自函数
get_mall_b_type_favour_week(history_week_range)
get_business_b_type_favour_week(history_week_range)
get_business_b_type_brand_top30_week(history_week_range)
get_mall_b_type_brand_top30_week(history_week_range)
get_tourist_b_type_brand_top30_week(history_week_range)






