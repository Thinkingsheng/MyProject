# -*- coding:utf-8 -*-

# 导入自定义DBHandle类
from thl_test_py.fun_sum.db_handle import DBHandle
# 导入datavm跨库同步信息字典
from thl_test_py.arguments_sum.update_sql_desc_diffdb import datavm_data
# 导入数据库信息
from thl_test_py.arguments_sum.db_info import thltest_db_info, datavm_db_info


def update_dm_table_diffdb_fun(db_dict):
    """
    利用datavm_data信息，在datavm库查出数据，然后存储到db_dict里
    调用的类和函数：DBHandle类，sql_dict_overwrite函数
    :param db_dict:传入要刷新数据的数据库信息字典
    :return:
    """
    # target_db为要同步的数据库
    target_db = DBHandle(db_dict)

    # 查询 dm_yingyun_zhengjia_flow_arrive_day 表数据的最大日期，+1天，并转为YYYYMMDD
    try:
        datavm_db = DBHandle(datavm_db_info)
        start_date_str = target_db.get_start_date(
            datavm_data['start_date_sql']
        ).replace("-", "")
        # 将SQL里的${b_date}替换成start_date_str，查询得出datavm_df
        datavm_df = datavm_db.select_data(
            datavm_data['data_sql'].replace("${b_date}", start_date_str)
        )
        # 将 datavm_df 输出到 dm_yingyun_zhengjia_flow_arrive_day 表
        target_db.append_data(
            datavm_data['append_table'],
            datavm_df
        )
        datavm_db.close_conn()
    except:
        pass
        print("dm_yingyun_zhengjia_flow_arrive_day表同步失败，可能情况：1、连接不上datavm库；2、已有数据；3、db_dict出错。")

    target_db.close_conn()


# 注意：修改数据库信息参数
if __name__ == "__main__":
    update_dm_table_diffdb_fun(thltest_db_info)
    # sleep(5)
    # update_dm_table_diffdb_fun(thlprod_db_info)
else:
    pass
