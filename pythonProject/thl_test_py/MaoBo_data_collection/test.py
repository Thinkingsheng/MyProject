# -*- coding: utf-8 -*-
# Auther : Think
# Date : 2023/4/23 20:35
# File : test.py


# from thl_test_py.MaoBo_data_collection.params import uri_params
# from thl_test_py.MaoBo_data_collection.utils.get_uri_make import GetUriMake
#
# # params_uri_list = GetUriMake(
# #     uri_params.trading_area_flow_ratio_url_dict,
# #     uri_params.trading_area_flow_ratio_params_dict
# #     ).two_day_uri("startTime", "endTime", "2023-03-01", "2023-03-03")
#
# # params_uri_list = GetUriMake(
# #     uri_params.trading_area_flow_rank_url_dict,
# #     uri_params.trading_area_flow_rank_params_dict
# #     ).two_day_uri("startTime", "endTime", "2023-03-01", "2023-03-03")
#
# # params_uri_list = GetUriMake(
# #     uri_params.trading_area_flow_warning_url_dict,
# #     uri_params.trading_area_flow_warning_params_dict
# #     ).two_day_uri("startTime", "endTime", "2023-03-01", "2023-03-03")
#
# # params_uri_list = GetUriMake(
# #     uri_params.trading_area_flow_source_url_dict_1,
# #     uri_params.trading_area_flow_source_params_dict_1
# #     ).one_day_uri("day", "2023-03-01", "2023-03-03")
#
# # params_uri_list = GetUriMake(
# #     uri_params.trading_area_flow_source_url_dict_2,
# #     uri_params.trading_area_flow_source_params_dict_2
# #     ).one_day_uri("day", "2023-03-01", "2023-03-03")
#
# # params_uri_list = GetUriMake(
# #     uri_params.trading_area_flow_source_url_dict_3,
# #     uri_params.trading_area_flow_source_params_dict_3
# #     ).one_day_uri("day", "2023-03-01", "2023-03-03")
#
# # params_uri_list = GetUriMake(
# #     uri_params.trading_area_flow_source_url_dict_4,
# #     uri_params.trading_area_flow_source_params_dict_4
# #     ).one_day_uri("day", "2023-03-01", "2023-03-03")
#
# params_uri_list = GetUriMake(
#     uri_params.trading_area_profile_url_dict,
#     uri_params.trading_area_profile_params_dict
#     ).one_month_uri("month", "2023-03", "2023-03")
#
# print(params_uri_list)


# import httpx
#
# params = {'account': 'test@mob.com', 'userId': '154', 'type': 'home', 'month': '202303'}
#
# params_str = str(params)
#
# # 一、声明使用http2，请求获取数据
# with httpx.Client(http2=True) as client:
#     res = client.get("http://test-www-enterprise-mobeye-sit.ing.mob.com/trading-area/profile", params=params)
#     res_str = res.text
#
#
# print(res_str)


from thl_test_py.MaoBo_data_collection.utils.get_params_make import GetParamsMake
from thl_test_py.MaoBo_data_collection.params import uri_params
from thl_test_py.MaoBo_data_collection.utils.data_handle import data_handle
from thl_test_py.arguments_sum.db_info import thltest_db_info


flow_source_1_url_params_list = GetParamsMake(uri_params.trading_area_flow_source_url_dict_1,
                                              uri_params.trading_area_flow_source_params_dict_1).one_day_param("day", "20230301", "20230303")

full_data_df = data_handle(flow_source_1_url_params_list, uri_params.trading_area_flow_source_append_db_params_list_1,
                           thltest_db_info)

print(full_data_df)

print(GetParamsMake(uri_params.trading_area_flow_ratio_url_dict,
                    uri_params.trading_area_flow_ratio_params_dict).two_day_param("startTime", "endTime", "2023-03-07", "2023-03-10"))


print(GetParamsMake(uri_params.trading_area_profile_url_dict,
                                        uri_params.trading_area_profile_params_dict).one_month_param("month",  "2023-03", "2023-03"))





