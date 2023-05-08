# -*- coding:utf-8 -*-

from thl_test_py.fun_sum.get_api_data import get_epidemic_area_str
from thl_test_py.fun_sum.excel_handle import excel_handle_output_1


if __name__ == "__main__":
    # 定义文档地址、sheet_name、写入列名
    input_excel_path = r"C:\Users\Think\Desktop\Data\111.xlsx"
    input_sheet_name = 'Sheet1'
    input_col_name = u'日期文本2'
    output_excel_path = r"C:\Users\Think\Desktop\Data\222.xlsx"
    output_col_name = u'广州市_高风险地区数'
    # 定义输出结果的位置（在excel里面的行数）
    output_index = 2
    temp_result = "0"

    excel_handle_output_1(
        get_epidemic_area_str
        , input_excel_path
        , input_col_name
        , output_excel_path
        , output_col_name
        , output_index
        , temp_result
        , input_sheet_name)
else:
    pass
