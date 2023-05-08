# -*- coding:utf-8 -*-
# @Author : Think
# @Date : 2023-04-10
# @File_name : update_wechat_mini_visit_trend_analysis.py

import pandas as pd
# 导入自建的数据库处理类
from thl_test_py.fun_sum.db_handle import DBHandle
# 导入数据库配置信息字典
from thl_test_py.arguments_sum.db_info import bjlmdc_db_info, thltest_db_info
# 导入自建的日期类
from thl_test_py.fun_sum.global_fun import CurrentTimeTrans


source_table = 'wechat_mini_visit_trend_analysis'

target_table = 'wechat_mini_visit_trend_analysis'

record_table = 'wechat_mini_visit_trend_analysis_update_record'

record_max_id_sql = "select * from %s where `date` = date_sub(date(now()),INTERVAL 1 DAY)" % record_table


# 主要更新调用函数
def update_wechat_mini_visit_trend_analysis_fun(source_db_dict, target_db_dict,
                                                source_table, target_table,
                                                record_table, record_max_id_sql):
    """
    :param source_db_dict: 源数据库_信息字典
    :param target_db_dict: 目标数据库_信息字典
    :param source_table: 源数据表
    :param target_table: 目标数据表
    :param record_table: 最大id记录表
    :param record_max_id_sql: 查询“最大id记录表”里最大id的sql
    :return: 成功后会返回提示
    """
    # 创建源数据库和目标数据库实例
    source_db = DBHandle(source_db_dict)
    target_db = DBHandle(target_db_dict)
    # 一、查询同步记录表最大id值
    record_max_id_df = target_db.select_data(record_max_id_sql)
    # 取出查出的dataframe里面的值
    record_max_id = record_max_id_df['id'].values[0]
    # 二、按照返回的最大id值，查询数据并插入到表
    select_sql = "select * from %s WHERE `id` > %d" % (source_table, int(record_max_id))
    res_df = source_db.select_data(select_sql)
    if res_df is not None:
        target_db.append_data(target_table, res_df)
    else:
        pass
    # 三、把当前表的最大id值插入到同步记录表
    # 提交刷新target_db的会话（没有这步的话，会话的表数据不会刷新）
    target_db.commit_data()
    c_max_id_sql = "select max(`id`) as 'max_id' from %s" % target_table
    # 查询当前目标表target_table的最大id
    c_max_id_df = target_db.select_data(c_max_id_sql)
    # 取出查出的dataframe里面的值
    c_max_id = c_max_id_df['max_id'].values[0]
    # 构造插入到同步记录表的df——max_id_df
    max_id_df = pd.DataFrame(
        {
            # 此处要转为列表形式
            'date': [CurrentTimeTrans().get_current_date()],
            'id': [c_max_id]
        })
    target_db.append_data(record_table, max_id_df)

    # 用close_conn关闭引擎
    source_db.close_conn()
    target_db.close_conn()


if __name__ == "__main__":
    update_wechat_mini_visit_trend_analysis_fun(bjlmdc_db_info, thltest_db_info,
                                                source_table, target_table,
                                                record_table, record_max_id_sql)
else:
    pass
