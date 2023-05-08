# -*- coding:utf-8 -*-
# @Author : Think
# @Date : 2023-04-24
# @File_name : main_starter.py

from thl_test_py.arguments_sum.db_info import thltest_db_info
from thl_test_py.MaoBo_data_collection.starter.starter import starter
from thl_test_py.MaoBo_data_collection.params import uri_params


if __name__ == "__main__":
    starter(
        thltest_db_info, "ods_mb_trading_area_flow_source_3_test", uri_params.trading_area_flow_source_url_dict_3,
        uri_params.trading_area_flow_source_params_dict_3, uri_params.trading_area_flow_source_append_db_params_list_3,
        "day",  "2023-03-01", "2023-03-10"
    )
    starter(
        thltest_db_info, "ods_mb_trading_area_flow_ratio_test", uri_params.trading_area_flow_ratio_url_dict,
        uri_params.trading_area_flow_ratio_params_dict, uri_params.trading_area_flow_ratio_append_db_params_list,
        "startTime", "endTime", "2023-03-01", "2023-03-10"
        )
    starter(
        thltest_db_info, "ods_mb_trading_area_profile_test", uri_params.trading_area_profile_url_dict,
        uri_params.trading_area_profile_params_dict, uri_params.trading_area_profile_append_db_params_list,
        "month", "2023-03", "2023-03"
        )
else:
    pass
