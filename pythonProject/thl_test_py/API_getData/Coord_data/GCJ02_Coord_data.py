# -*- coding:utf-8 -*-

from thl_test_py.fun_sum.get_api_data import get_gcj02_lnglat
from thl_test_py.fun_sum.excel_handle import excel_handle_output_1


# if __name__ == "__main__":
#     # 定义文档地址、sheet_name、写入列名
#     input_excel_path = r"C:\Users\Think\Desktop\Input_data\全市公共厕所基本信息表.xlsx"
#     input_sheet_name = '越秀区核酸检测点'
#     output_excel_path = r"C:\Users\Think\Desktop\output_data\全市公共厕所基本信息表_越秀区核酸检测点.xlsx"
#     input_col_name = u'标准地址'
#     output_col_name = u'坐标'
#     # 定义输出结果的位置（在excel里面的行数）
#     output_index = 2
#     temp_result = "113.264434,23.129162"
#
#     excel_handle_output_1(
#         gcj02_getlnglat,
#         input_excel_path,
#         input_col_name,
#         output_excel_path,
#         output_col_name, output_index,
#         temp_result,
#         input_sheet_name)
# else:
#     pass


if __name__ == "__main__":
    # 定义文档地址、sheet_name、写入列名
    input_excel_path = r"C:\Users\Think\Desktop\Input_data\北京路商圈停车场.xlsx"
    input_sheet_name = 'Sheet1'
    input_col_name = u'详细地址'
    output_excel_path = r"C:\Users\Think\Desktop\output_data\北京路商圈停车场.xlsx"
    output_col_name = u'坐标'
    # 定义输出结果的位置（在excel里面的行数）
    output_index = 2
    temp_result = "0"

    excel_handle_output_1(
        get_gcj02_lnglat
        , input_excel_path
        , input_col_name
        , output_excel_path
        , output_col_name
        , output_index
        , temp_result
        , input_sheet_name)
else:
    pass
