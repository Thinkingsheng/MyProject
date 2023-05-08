# -*- coding:utf-8 -*-

# 导入自定义DBHandle类
from thl_test_py.fun_sum.db_handle import DBHandle, sql_dict_overwrite
# 导入数据库信息
from thl_test_py.arguments_sum.db_info import thltest_db_info
# 导入SQL字典
from thl_test_py.arguments_sum.update_sql_desc_unionpay_sale import unionpay_sale_update


def update_unionpay_sale(db_dict):
    """
    日数据更新主函数。
    调用的类和函数：DBHandle类，sql_dict_overwrite函数
    :param db_dict:传入要刷新数据的数据库信息字典
    :return:
    """
    # target_db为要同步的数据库实例
    target_db = DBHandle(db_dict)

    # 银联_销售数据更新部分：
    sql_dict_overwrite(target_db, unionpay_sale_update)

    target_db.close_conn()


if __name__ == "__main__":
    update_unionpay_sale(thltest_db_info)
    # sleep(5)
    # update_unionpay_sale(thlprod_db_info)
else:
    pass
