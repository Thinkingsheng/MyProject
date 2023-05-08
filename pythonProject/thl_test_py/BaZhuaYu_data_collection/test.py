# -*- coding:utf-8 -*-
# @Author : Think
# @Date : 2023-04-27
# @File_name : test.py

import httpx
from thl_test_py.fun_sum.excel_handle import json_data_trans


uri = "https://openapi.dataduoduo.com/commonproject/project/loadData"

body = {"consumerId": "zjkj-de7c80bda45524cb", "type": "dz_comments", "pullField": "_id", "cursor": "", "size": "100"}

with httpx.Client(http2=True) as client:
    res = client.post(uri, json=body)
    res_str = res.text
res_dict = eval(res_str)
res_json_list = res_dict["data"]["list"]
json_data_trans(res_json_list, r"C:\Users\Think\Desktop\output_data", "八爪鱼数据.xlsx")


