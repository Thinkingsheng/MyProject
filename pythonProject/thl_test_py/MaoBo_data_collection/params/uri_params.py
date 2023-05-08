# -*- coding:utf-8 -*-
# @Author : Think
# @Date : 2023-04-14
# @File_name : uri_params.py

from collections import OrderedDict

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
# url和path字典

# 接口1.商圈客流贡献度（trading_area_flow_ratio）
trading_area_flow_ratio_url_dict = OrderedDict(
    [
        ("url", "http://test-www-enterprise-mobeye-sit.ing.mob.com"),
        ("path", "/trading-area/flow-ratio")
    ]
)

# 接口2.客流量贡献度TOP5（trading_area_flow_rank）
trading_area_flow_rank_url_dict = OrderedDict(
    [
        ("url", "http://test-www-enterprise-mobeye-sit.ing.mob.com"),
        ("path", "/trading-area/flow-rank")
    ]
)

# 接口3.客流量指数（trading_area_flow_warning）
trading_area_flow_warning_url_dict = OrderedDict(
    [
        ("url", "http://test-www-enterprise-mobeye-sit.ing.mob.com"),
        ("path", "/trading-area/flow-warning")
    ]
)

# 接口4.客流来源地查询（trading_area_flow_source）
trading_area_flow_source_url_dict = OrderedDict(
    [
        ("url", "http://test-www-enterprise-mobeye-sit.ing.mob.com"),
        ("path", "/trading-area/flow-source")
    ]
)

# 接口4.客流来源地查询（trading_area_flow_source）
trading_area_flow_source_url_dict_1 = OrderedDict(
    [
        ("url", "http://test-www-enterprise-mobeye-sit.ing.mob.com"),
        ("path", "/trading-area/flow-source")
    ]
)

# 接口4.客流来源地查询（trading_area_flow_source）
trading_area_flow_source_url_dict_2 = OrderedDict(
    [
        ("url", "http://test-www-enterprise-mobeye-sit.ing.mob.com"),
        ("path", "/trading-area/flow-source")
    ]
)

# 接口4.客流来源地查询（trading_area_flow_source）
trading_area_flow_source_url_dict_3 = OrderedDict(
    [
        ("url", "http://test-www-enterprise-mobeye-sit.ing.mob.com"),
        ("path", "/trading-area/flow-source")
    ]
)

# 接口4.客流来源地查询（trading_area_flow_source）
trading_area_flow_source_url_dict_4 = OrderedDict(
    [
        ("url", "http://test-www-enterprise-mobeye-sit.ing.mob.com"),
        ("path", "/trading-area/flow-source")
    ]
)

# 接口5.商圈内客群分析（trading_area_profile）
trading_area_profile_url_dict = OrderedDict(
    [
        ("url", "http://test-www-enterprise-mobeye-sit.ing.mob.com"),
        ("path", "/trading-area/profile")
    ]
)

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
# 调用参数字典（注：各参数需为列表形式）

# 接口1.商圈客流贡献度（trading_area_flow_ratio）
trading_area_flow_ratio_params_dict = OrderedDict(
    [
        ("account", ["test@mob.com"]),
        ("userId", ["154"])
    ]
)

# 接口2.客流量贡献度TOP5（trading_area_flow_rank）
trading_area_flow_rank_params_dict = OrderedDict(
    [
        ("account", ["test@mob.com"]),
        ("userId", ["154"])
    ]
)

# 接口3.客流量指数（trading_area_flow_warning）
trading_area_flow_warning_params_dict = OrderedDict(
    [
        ("account", ["test@mob.com"]),
        ("userId", ["154"])
    ]
)

# 接口4.客流来源地查询（trading_area_flow_source）的类型1-商圈辐射力
trading_area_flow_source_params_dict_1 = OrderedDict(
    [
        ("account", ["test@mob.com"]),
        ("userId", ["154"]),
        # 查询类型：1-商圈辐射力，2-超区域辐射力商综体，3-最受外地人欢迎商综体top3，4-最受本地人欢迎商综体top3
        ("type", ["1"])
    ]
)

# 接口4.客流来源地查询（trading_area_flow_source）的类型2-超区域辐射力商综体
trading_area_flow_source_params_dict_2 = OrderedDict(
    [
        ("account", ["test@mob.com"]),
        ("userId", ["154"]),
        # 查询类型：1-商圈辐射力，2-超区域辐射力商综体，3-最受外地人欢迎商综体top3，4-最受本地人欢迎商综体top3
        ("type", ["2"])
    ]
)

# 接口4.客流来源地查询（trading_area_flow_source）的类型3-最受外地人欢迎商综体top3
trading_area_flow_source_params_dict_3 = OrderedDict(
    [
        ("account", ["test@mob.com"]),
        ("userId", ["154"]),
        # 查询类型：1-商圈辐射力，2-超区域辐射力商综体，3-最受外地人欢迎商综体top3，4-最受本地人欢迎商综体top3
        ("type", ["3"])
    ]
)

# 接口4.客流来源地查询（trading_area_flow_source）的类型4-最受本地人欢迎商综体top3
trading_area_flow_source_params_dict_4 = OrderedDict(
    [
        ("account", ["test@mob.com"]),
        ("userId", ["154"]),
        # 查询类型：1-商圈辐射力，2-超区域辐射力商综体，3-最受外地人欢迎商综体top3，4-最受本地人欢迎商综体top3
        ("type", ["4"])
    ]
)

# 接口5.商圈内客群分析（trading_area_profile）
trading_area_profile_params_dict = OrderedDict(
    [
        ("account", ["test@mob.com"]),
        ("userId", ["154"]),
        # 居住客群：home,工作客群：work
        ("type", ["home", "work"])
    ]
)

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
# get_uri_make模块GetUriMake类构建uri的方法类型_映射字典

uri_make_dict = {
    "/trading-area/flow-ratio": "two_day",
    "/trading-area/flow-rank": "two_day",
    "/trading-area/flow-warning": "two_day",
    "/trading-area/flow-source": "one_day",
    "/trading-area/profile": "one_month"
}

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
# 需要插入到数据库的参数名称列表：

# 接口1.商圈客流贡献度（trading_area_flow_ratio）
trading_area_flow_ratio_append_db_params_list = []

# 接口2.客流量贡献度TOP5（trading_area_flow_rank）
trading_area_flow_rank_append_db_params_list = []

# 接口3.客流量指数（trading_area_flow_warning）
trading_area_flow_warning_append_db_params_list = []

# 接口4.客流来源地查询（trading_area_flow_source）的类型1-商圈辐射力
trading_area_flow_source_append_db_params_list_1 = ["day"]

# 接口4.客流来源地查询（trading_area_flow_source）的类型2-超区域辐射力商综体
trading_area_flow_source_append_db_params_list_2 = []

# 接口4.客流来源地查询（trading_area_flow_source）的类型3-最受外地人欢迎商综体top3
trading_area_flow_source_append_db_params_list_3 = []

# 接口4.客流来源地查询（trading_area_flow_source）的类型4-最受本地人欢迎商综体top3
trading_area_flow_source_append_db_params_list_4 = []

# 接口5.商圈内客群分析（trading_area_profile）
trading_area_profile_append_db_params_list = ["type"]
