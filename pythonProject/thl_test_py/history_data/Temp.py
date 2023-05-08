# -*- coding:utf-8 -*-


import httpx
import json


def juliang_data():
    url = 'https://trendinsight.oceanengine.com/api/open/index/get_multi_keyword_hot_trend?msToken=MMnCB_ulKplr8GWCRUm8RJwOPlbJ8yBlVx1o3fMAUV8yO5ulSe3qiubUwRZk4NEV_Zkrh94bSJEhaEizU5XBU9z8iFnZXQ_Ts6uJzQvmajGGANO-c3YFo_dbs5bNiuOQ&X-Bogus=DFSzKwGL0NBB2xUltGBGkl9WX7ny&_signature=_02B4Z6wo00001K39kFAAAIDALf9qEM-.OMit7ZTAAE9eC6kyUM4LNmdxhPvMibngPLzF-Rj.UiOJQZQTAR3dLMfrZ6gr-q-AuUkfJO1W8K1yXlf2RdzH4ZvD0YqJpnPqVjBtswEbzpMTtb3V05'

    data = {
        "keyword_list": [
            "正佳广场"
        ],
        "start_date": "20230308",
        "end_date": "20230329",
        "app_name": "aweme",
        "region": []
    }

    js_data = json.dumps(data)

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '110',
        'content-type': 'application/json',
        'cookie': 'x-jupiter-uuid=16796481219034644;msToken=66lOEB0-Ah-3g0sSpjYcsTZ3j9oRSIGA4AxiT37RJVhvHmgwAq_Y4nnnEHOgvokyeS0QouLHYlzflToc6DGGogxZZMQiq6AA4jyS5vpOWzV2ZkvrvIQ4fpaJ6KaW40EM; _csrf_token=lZ8B0Vm5SvfrPuM0GTKXTDFb; msToken=MMnCB_ulKplr8GWCRUm8RJwOPlbJ8yBlVx1o3fMAUV8yO5ulSe3qiubUwRZk4NEV_Zkrh94bSJEhaEizU5XBU9z8iFnZXQ_Ts6uJzQvmajGGANO-c3YFo_dbs5bNiuOQ; msToken=VJQkp0r4fkwJAqqT50MwJqgmGCSTIVSil9PwMHuI8EDnyxJyiEuKvHyBs5WwXwWalJnk6MGthq1rpEa7oi0JFEtwiXmfQ4xvoOHRStD83ruOh2c0tKA79uzqb5KGDCjz; _csrf_token=VVjF6ubL5mIoHCrF9zX-jtWT',
        'origin': 'https://trendinsight.oceanengine.com',
        'referer': 'https://trendinsight.oceanengine.com/arithmetic-index/analysis?keyword=%E6%AD%A3%E4%BD%B3%E5%B9%BF%E5%9C%BA&appName=aweme',
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'
    }

    cookies_dict = {}
    cookies_str = 'x-jupiter-uuid=16796481219034644; passport_csrf_token=df147936a659bdd0333ab1ad7aee2de3; passport_csrf_token_default=df147936a659bdd0333ab1ad7aee2de3; ttcid=7a3bc9093a0f4ffda6662578c399efe929; s_v_web_id=verify_lfmb4vtg_naWepUUn_Sura_4hDv_8pb2_2fmJavkpYDI3; odin_tt=0208b3022a29b4d544ef50b30d42c02efc78ef41fcdc74763d543753edb46d4282af3db01e62ae7fd6648ea450ab9420f4975937649f96af72c8d0456410ebca; n_mh=wxbs1Iq0pm6xqoQ3YsXEcJX7lorbscDWOADKPD-5fKQ; passport_auth_status=905fc900ab62c5867392728c91f3cf83%2C; passport_auth_status_ss=905fc900ab62c5867392728c91f3cf83%2C; sso_auth_status=56ecea7790ba34c7e4ba634d1fc5f1db; sso_auth_status_ss=56ecea7790ba34c7e4ba634d1fc5f1db; sso_uid_tt=db9864126804da6da28a39d68a0b0d3d; sso_uid_tt_ss=db9864126804da6da28a39d68a0b0d3d; toutiao_sso_user=99925afc38f431adee362a6aacb92abe; toutiao_sso_user_ss=99925afc38f431adee362a6aacb92abe; sid_ucp_sso_v1=1.0.0-KDEwNzdlNDI2ZGQ0M2M0MGE3NDk4MGNkMTAxNTI0MTliZjI4MWE2ZTMKGAidmMCyncyYBxCby_WgBhjS3BU4AkDsBxoCbGYiIDk5OTI1YWZjMzhmNDMxYWRlZTM2MmE2YWFjYjkyYWJl; ssid_ucp_sso_v1=1.0.0-KDEwNzdlNDI2ZGQ0M2M0MGE3NDk4MGNkMTAxNTI0MTliZjI4MWE2ZTMKGAidmMCyncyYBxCby_WgBhjS3BU4AkDsBxoCbGYiIDk5OTI1YWZjMzhmNDMxYWRlZTM2MmE2YWFjYjkyYWJl; passport_auth_status_count=04771ef3cf1141b87f3698c745f32203%2C; passport_auth_status_ss_count=04771ef3cf1141b87f3698c745f32203%2C; sid_guard_count=a7dc3174992feb07507899f73ef048ed%7C1679648156%7C5183999%7CTue%2C+23-May-2023+08%3A55%3A55+GMT; uid_tt_count=bc17276ef106f1988b35ab41a7c58f1e; uid_tt_ss_count=bc17276ef106f1988b35ab41a7c58f1e; sid_tt_count=a7dc3174992feb07507899f73ef048ed; sessionid_count=a7dc3174992feb07507899f73ef048ed; sessionid_ss_count=a7dc3174992feb07507899f73ef048ed; sid_ucp_v1_count=1.0.0-KGU2NmI3ZDc1NGIxZjNmMTNmNmVmMDc0ZTQ2YTE2Y2RmMDMyZDQxMGQKGAidmMCyncyYBxCcy_WgBhjS3BU4AkDsBxoCbGYiIGE3ZGMzMTc0OTkyZmViMDc1MDc4OTlmNzNlZjA0OGVk; ssid_ucp_v1_count=1.0.0-KGU2NmI3ZDc1NGIxZjNmMTNmNmVmMDc0ZTQ2YTE2Y2RmMDMyZDQxMGQKGAidmMCyncyYBxCcy_WgBhjS3BU4AkDsBxoCbGYiIGE3ZGMzMTc0OTkyZmViMDc1MDc4OTlmNzNlZjA0OGVk; store-region=cn-gd; store-region-src=uid; sid_guard=99925afc38f431adee362a6aacb92abe%7C1679648167%7C5183988%7CTue%2C+23-May-2023+08%3A55%3A55+GMT; uid_tt=db9864126804da6da28a39d68a0b0d3d; uid_tt_ss=db9864126804da6da28a39d68a0b0d3d; sid_tt=99925afc38f431adee362a6aacb92abe; sessionid=99925afc38f431adee362a6aacb92abe; sessionid_ss=99925afc38f431adee362a6aacb92abe; Hm_lvt_c36ebf0e0753eda09586ef4fb80ea125=1679966639,1680052885,1680139361,1680225530; Hm_lpvt_c36ebf0e0753eda09586ef4fb80ea125=1680225530; tt_scid=mg6PJ9t4AvdpBo0SBUhAwg527Ht3PUenfXxMFgt9AMOwZwCzM..rz8hygfoUrDjZbacc; msToken=66lOEB0-Ah-3g0sSpjYcsTZ3j9oRSIGA4AxiT37RJVhvHmgwAq_Y4nnnEHOgvokyeS0QouLHYlzflToc6DGGogxZZMQiq6AA4jyS5vpOWzV2ZkvrvIQ4fpaJ6KaW40EM; _csrf_token=lZ8B0Vm5SvfrPuM0GTKXTDFb; msToken=MMnCB_ulKplr8GWCRUm8RJwOPlbJ8yBlVx1o3fMAUV8yO5ulSe3qiubUwRZk4NEV_Zkrh94bSJEhaEizU5XBU9z8iFnZXQ_Ts6uJzQvmajGGANO-c3YFo_dbs5bNiuOQ'
    # 创建cookies实例
    cookies = httpx.Cookies()
    # 先将cookies_str按分号;切割为'x=y'
    c_split_list = cookies_str.split(";")
    # 遍历各个'x=y'
    for only_c in c_split_list:
        # 按等号=拆分x和y，再存入cookies字典
        only_c_split_list = only_c.split("=")
        cookies_dict[only_c_split_list[0]] = only_c_split_list[1]
    # 之后的使用方式和requests一样
    # post

    with httpx.Client(http2=True, follow_redirects=True, ) as client:
        res = client.post(url=url, headers=headers, json=data)
        print(res.status_code)
        print(res)
        print(res.text)
    # # get
    # result = client.get(url,headers=headers).text


def weibo_data():
    url = "https://data.weibo.com/index/ajax/newindex/getchartdata"

    data = {"wid": 120200901194031621324, "dateGroup": "1month"}

    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-Length': '42',
        'content-Type': 'application/x-www-form-urlencoded',
        'origin': 'https://data.weibo.com',
        'referer': 'https://data.weibo.com/index/newindex?visit_type=trend&wid=1091324231586',
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'
    }

    cookies = {
        'Cookies': 'SUB=_2AkMUfOTDf8NxqwJRmP4RzGPrbY5xzQzEieKiIBUYJRMxHRl-yT92qmgOtRB6P_zKLABFMpd9VZN47gIOV5-c1dl2HN6x; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5xbpEUDTAXT_1inllEzqaT; UOR=www.baidu.com,weibo.com,www.baidu.com; SINAGLOBAL=6362297338908.294.1668313263010; ULV=1668994531566:2:2:1:73990765834.7927.1668994531561:1668313263013; WEB3=cbf0c0854ffc0231c62d06ce4d64c2cf'}

    # 之后的使用方式和requests一样
    # post

    with httpx.Client(http2=True) as client:
        res = client.post(url, headers=headers, cookies=cookies, data=data)
        print(res.text)



# def temp_cokies():
#     cookies_dict = {}
#     cookies_str = 'x-jupiter-uuid=16796481219034644; passport_csrf_token=df147936a659bdd0333ab1ad7aee2de3; passport_csrf_token_default=df147936a659bdd0333ab1ad7aee2de3; ttcid=7a3bc9093a0f4ffda6662578c399efe929; s_v_web_id=verify_lfmb4vtg_naWepUUn_Sura_4hDv_8pb2_2fmJavkpYDI3; odin_tt=0208b3022a29b4d544ef50b30d42c02efc78ef41fcdc74763d543753edb46d4282af3db01e62ae7fd6648ea450ab9420f4975937649f96af72c8d0456410ebca; n_mh=wxbs1Iq0pm6xqoQ3YsXEcJX7lorbscDWOADKPD-5fKQ; passport_auth_status=905fc900ab62c5867392728c91f3cf83%2C; passport_auth_status_ss=905fc900ab62c5867392728c91f3cf83%2C; sso_auth_status=56ecea7790ba34c7e4ba634d1fc5f1db; sso_auth_status_ss=56ecea7790ba34c7e4ba634d1fc5f1db; sso_uid_tt=db9864126804da6da28a39d68a0b0d3d; sso_uid_tt_ss=db9864126804da6da28a39d68a0b0d3d; toutiao_sso_user=99925afc38f431adee362a6aacb92abe; toutiao_sso_user_ss=99925afc38f431adee362a6aacb92abe; sid_ucp_sso_v1=1.0.0-KDEwNzdlNDI2ZGQ0M2M0MGE3NDk4MGNkMTAxNTI0MTliZjI4MWE2ZTMKGAidmMCyncyYBxCby_WgBhjS3BU4AkDsBxoCbGYiIDk5OTI1YWZjMzhmNDMxYWRlZTM2MmE2YWFjYjkyYWJl; ssid_ucp_sso_v1=1.0.0-KDEwNzdlNDI2ZGQ0M2M0MGE3NDk4MGNkMTAxNTI0MTliZjI4MWE2ZTMKGAidmMCyncyYBxCby_WgBhjS3BU4AkDsBxoCbGYiIDk5OTI1YWZjMzhmNDMxYWRlZTM2MmE2YWFjYjkyYWJl; passport_auth_status_count=04771ef3cf1141b87f3698c745f32203%2C; passport_auth_status_ss_count=04771ef3cf1141b87f3698c745f32203%2C; sid_guard_count=a7dc3174992feb07507899f73ef048ed%7C1679648156%7C5183999%7CTue%2C+23-May-2023+08%3A55%3A55+GMT; uid_tt_count=bc17276ef106f1988b35ab41a7c58f1e; uid_tt_ss_count=bc17276ef106f1988b35ab41a7c58f1e; sid_tt_count=a7dc3174992feb07507899f73ef048ed; sessionid_count=a7dc3174992feb07507899f73ef048ed; sessionid_ss_count=a7dc3174992feb07507899f73ef048ed; sid_ucp_v1_count=1.0.0-KGU2NmI3ZDc1NGIxZjNmMTNmNmVmMDc0ZTQ2YTE2Y2RmMDMyZDQxMGQKGAidmMCyncyYBxCcy_WgBhjS3BU4AkDsBxoCbGYiIGE3ZGMzMTc0OTkyZmViMDc1MDc4OTlmNzNlZjA0OGVk; ssid_ucp_v1_count=1.0.0-KGU2NmI3ZDc1NGIxZjNmMTNmNmVmMDc0ZTQ2YTE2Y2RmMDMyZDQxMGQKGAidmMCyncyYBxCcy_WgBhjS3BU4AkDsBxoCbGYiIGE3ZGMzMTc0OTkyZmViMDc1MDc4OTlmNzNlZjA0OGVk; store-region=cn-gd; store-region-src=uid; sid_guard=99925afc38f431adee362a6aacb92abe%7C1679648167%7C5183988%7CTue%2C+23-May-2023+08%3A55%3A55+GMT; uid_tt=db9864126804da6da28a39d68a0b0d3d; uid_tt_ss=db9864126804da6da28a39d68a0b0d3d; sid_tt=99925afc38f431adee362a6aacb92abe; sessionid=99925afc38f431adee362a6aacb92abe; sessionid_ss=99925afc38f431adee362a6aacb92abe; Hm_lvt_c36ebf0e0753eda09586ef4fb80ea125=1679966639,1680052885,1680139361,1680225530; Hm_lpvt_c36ebf0e0753eda09586ef4fb80ea125=1680225530; tt_scid=mg6PJ9t4AvdpBo0SBUhAwg527Ht3PUenfXxMFgt9AMOwZwCzM..rz8hygfoUrDjZbacc; msToken=66lOEB0-Ah-3g0sSpjYcsTZ3j9oRSIGA4AxiT37RJVhvHmgwAq_Y4nnnEHOgvokyeS0QouLHYlzflToc6DGGogxZZMQiq6AA4jyS5vpOWzV2ZkvrvIQ4fpaJ6KaW40EM; _csrf_token=lZ8B0Vm5SvfrPuM0GTKXTDFb; msToken=MMnCB_ulKplr8GWCRUm8RJwOPlbJ8yBlVx1o3fMAUV8yO5ulSe3qiubUwRZk4NEV_Zkrh94bSJEhaEizU5XBU9z8iFnZXQ_Ts6uJzQvmajGGANO-c3YFo_dbs5bNiuOQ'
#     # 创建cookies实例
#     cookies = httpx.Cookies()
#     # 先将cookies_str按分号;切割为'x=y'
#     c_split_list = cookies_str.split(";")
#     # 遍历各个'x=y'
#     for only_c in c_split_list:
#         # 按等号=拆分x和y，再存入cookies字典
#         only_c_split_list = only_c.split("=")
#         cookies_dict[only_c_split_list[0]] = only_c_split_list[1]
#     cookies.update(cookies_dict)
#     print(cookies)
#     print(type(cookies))
#
#
# temp_cokies()


# juliang_data()
# weibo_data()
# juliang_data_2()
# print(T_1TimeTrans().get_t_1_date_year())


# print(data_json_trans(r"C:\Users\Think\Desktop\Input_data\3月热力数据.xlsx", "处理表", r"C:\Users\Think\Desktop\output_data\3月热力数据.json"))


weibo_data()
