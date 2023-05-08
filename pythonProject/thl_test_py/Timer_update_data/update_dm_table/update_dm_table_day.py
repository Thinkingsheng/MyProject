# -*- coding:utf-8 -*-

# 导入自定义DBHandle类
from thl_test_py.fun_sum.db_handle import DBHandle, sql_dict_overwrite
# 导入数据库信息
from thl_test_py.arguments_sum.db_info import thltest_db_info
# 导入SQL字典
from thl_test_py.arguments_sum.update_sql_desc_day import day_update_1, day_update_2


def update_day(db_dict):
    """
    日数据更新主函数。
    调用的类和函数：DBHandle类，sql_dict_overwrite函数
    :param db_dict:传入要刷新数据的数据库信息字典
    :return:
    """
    # target_db为要同步的数据库
    target_db = DBHandle(db_dict)

    # 一、运行excel_sheet_sum，将本地的正佳销售数据输出到表

    # 二、运行update_dim_table，同步dim日表

    # 三、运行update_dm_table_diffdb，同步跨库的 dm_yingyun_zhengjia_flow_arrive_day 表

    # 四、日调度更新部分：
    sql_dict_overwrite(target_db, day_update_1)
    sql_dict_overwrite(target_db, day_update_2)

    target_db.close_conn()


if __name__ == "__main__":
    update_day(thltest_db_info)
    # sleep(5)
    # update_day(thlprod_db_info)
else:
    pass
