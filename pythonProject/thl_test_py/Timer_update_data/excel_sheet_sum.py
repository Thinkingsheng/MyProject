# -*- coding:utf-8 -*-

from thl_test_py.fun_sum.db_handle import xls_db_append
from thl_test_py.arguments_sum.db_info import thltest_db_info, thlprod_db_info
from time import sleep


input_dir = r'C:\Users\Think\Desktop\及刻_历史数据导入\大屏销售页建表\销售源数据_2023(4)'  # 输入的文件夹名
# output_dir = r'C:\Users\Think\Desktop\及刻_历史数据导入\大屏销售页建表\销售数据_汇总表'  # 输出的文件夹名

target_table = 'zhengjia_sale_data'


if __name__ == "__main__":
    xls_db_append(input_dir, thltest_db_info, target_table)
    sleep(5)
    xls_db_append(input_dir, thlprod_db_info, target_table)
else:
    pass
