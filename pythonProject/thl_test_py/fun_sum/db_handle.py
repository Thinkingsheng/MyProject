# -*- coding:utf-8 -*-

import xlrd2
import pandas as pd
import pymysql
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from thl_test_py.fun_sum.global_fun import get_files
import warnings
import platform


def xls_db_append(input_dir, db_dict, target_table):
    """
    遍历 input_dir 路径内所有的xls文档内所有sheet，汇总后插入到 db_dict 的 target_table 表
    (注意：要保证“线下文档的列”与“目标表的列”对应)
    :param input_dir: 输入的文件夹名
    :param db_dict: 数据库信息字典
    :param target_table: 目标表名
    :return:
    """
    # 开启mysql引擎
    db_str = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % (
        db_dict['user_name'], db_dict['password'], db_dict['host'], db_dict['port'], db_dict['db_name'],
        db_dict['charset'])
    engine = create_engine(db_str)
    # 开启查询连接
    connection = engine.connect()
    # 忽略文件的相关告警
    warnings.filterwarnings('ignore')
    # 遍历input_dir路径下的文件
    for file_name in get_files(input_dir):
        print("开始取数：" + file_name + "...")
        # 判断系统类型，然后分隔符值赋给split_str
        if platform.system().lower() == "windows":
            split_str = "\\"
        elif platform.system().lower() == "linux":
            split_str = "/"
        file_path = input_dir + split_str + file_name
        wb = xlrd2.open_workbook(file_path)
        sheets = wb.sheet_names()
        # 定义存多个dataframe（这里是指各个sheet）的列表
        df_list = []
        # 逐个sheet依次读取，然后存到df_list
        for i in range(len(sheets)):
            df = pd.read_excel(file_path, sheet_name=i)
            df_list.append(df)
        # 将df_list里的dataframe上下拼接
        df_sum = pd.concat(df_list, axis=0)
        df_sum = df_sum.reset_index(drop=True)
        print("行数：" + str(df_sum.shape[0]))
        print("列数：" + str(df_sum.shape[1]))
        # 若输入是xls文件，输出xlsx，则需要替换为xlsx
        # file_name_xlsx = file_name.replace(".xls", ".xlsx")
        # 若输入是xls文件，输出csv，则需要替换为xlsx
        # file_name_xlsx = file_name.replace(".xls", ".csv")
        print("开始导出：" + file_name + "...")
        file_name_xlsx = file_name

        # # 导出为excel文档
        # with pd.ExcelWriter(output_dir + "\%s" % file_name_xlsx) as writer:
        #     df_sum.to_excel(writer, sheet_name='data', index=0)
        # # 导出为csv文档(未成功）
        # df_sum.to_csv(output_dir + "\%s" % file_name_xlsx, sheet_name='data', index=0)

        # 导出到MYSQL
        # 查询首行数据，用来获取列名
        result = connection.execute("select * from %s LIMIT 1" % target_table)
        # 依次获取查询结果详情的元组里，首个字符（列名），存到col_names列表
        col_names = [i[0] for i in result.cursor.description]
        # 将列名改为col_names
        df_sum.columns = col_names
        print("预览数据...")
        print(df_sum.tail())
        # 导出df到target_table目标表
        df_sum.to_sql(target_table, con=engine, chunksize=200000, if_exists='append', index=False)
        print(file_name_xlsx + "————导出成功！")
        print("————————————————————————————————————————————————————————————————————————")
    connection.close()
    engine.dispose()


class DBHandle():

    def __init__(self, db_dict):
        """
        同时创建pymysql连接、游标、sqlalchemy引擎
        :param db_dict: 数据库相关信息字典
        :return:提示
        """
        self.db_dict = db_dict
        self.table_name = ''
        self.db_conn = pymysql.connect(host=db_dict['host'], port=int(db_dict['port']), user=db_dict['user_name'],
                                       passwd=db_dict['password'], db=db_dict['db_name'], charset=db_dict['charset'])
        print(db_dict['db_name'] + " 的pymysql连接已创建。")
        self.cursor = self.db_conn.cursor()
        print(db_dict['db_name'] + " 的pymysql连接_游标已创建。")
        self.db_engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % (
            db_dict['user_name'], db_dict['password'], db_dict['host'], db_dict['port'],
            db_dict['db_name'], db_dict['charset']))
        print(db_dict['db_name'] + " 的sqlalchemy引擎已创建。")
        self.session = sessionmaker(bind=self.db_engine)()
        print(db_dict['db_name'] + " 的sqlalchemy引擎_会话已创建。")
        print("————————————————————————————————————————————————————————————————————————")

    def select_data(self, sql):
        """
        连接数据库查询数据，输出查询结果的dataframe
        :param sql:查询SQL
        :return: result_df(dataframe)
        """
        self.cursor.execute(sql)
        # 获取查询结果的列名列表（col_list）
        col_tuple = self.cursor.description
        col_list = []
        for col_str in col_tuple:
            col_list.append(col_str[0])
        # 获取查询结果
        result = self.cursor.fetchall()
        # 若结果不等于空元组，才作处理
        if result != ():
            result_list = list(result)
            # 如果查询出数据的话，重置游标到第一行
            if len(result_list) > 0:
                self.cursor.scroll(0, mode="absolute")
            else:
                pass
            # 执行结果转化为dataframe
            result_df = pd.DataFrame(result_list)
            # 更改df的columns为col_list
            result_df.columns = col_list
            print("查询成功！预览尾部查询数据...")
            print(result_df.tail())
            # 返回dataframe
            return result_df
        else:
            print("查无数据！")
            return None

    def append_data(self, table_name, data):
        """
        dataframe格式数据，输出到库的目标表的函数
        :param table_name:输出数据的目标表名
        :param data:数据(dataframe格式，注意！！要保证要和目标表的列名一致)
        :return:输出数据到库的目标表
        """
        print("即将对 " + table_name + " 表进行插入操作...")
        # 开启查询连接
        connection = self.db_engine.connect()
        result = connection.execute("select * from %s LIMIT 1" % table_name)
        # 依次获取查询结果详情的元组里，首个字符（列名），存到col_names列表
        col_names = [i[0] for i in result.cursor.description]
        connection.close()
        # 将列名改为col_names
        data.columns = col_names
        print("预览尾部数据...")
        print(data.tail())
        data.to_sql(table_name, con=self.db_engine, chunksize=200000, if_exists='append', index=False)
        print('插入成功条数：' + str(data.shape[0]))

    def delete_data(self, sql):
        """
        通过SQL删除数据
        :param sql:SQL字符串
        :return:删除成功与否提示
        """
        try:
            count = self.cursor.execute(sql)
            self.db_conn.commit()
            print("删除成功条数：" + str(count))
        except Exception as result:
            self.db_conn.rollback()
            print(result)
            print("删除异常SQL：" + sql)

    def commit_data(self):
        """
        刷新连接会话
        :return: 提示
        """
        self.session.commit()
        self.db_conn.commit()
        print("连接会话已提交刷新!")

    def get_start_date(self, max_date_sql):
        """
        定义获取“目标表里的最大日期+1天”函数
        :param db_table_dict: 数据库信息字典
        :param max_date_sql: 查询目标表最大日期的SQL
        :return: start_date（开始日期YYYY-MM-DD的字符串）
        """
        # SQL查出最大日期
        res = self.session.execute(max_date_sql).fetchone()
        # 需转为列表才能转为dataframe
        df = pd.DataFrame(data=list(res))
        max_date = str(df.iloc[0, 0])
        # 判断获取的max_date是"YYYY-MM-DD"格式还是"YYYYMMDD"格式，然后+1天后统一输出为"YYYY-MM-DD"
        if max_date.find("-") != -1:
            max_date_time = datetime.datetime.strptime(max_date, '%Y-%m-%d')
            max_date_time += datetime.timedelta(days=1)
            start_date_str = max_date_time.strftime('%Y-%m-%d')
        else:
            max_date_time = datetime.datetime.strptime(max_date, '%Y%m%d')
            max_date_time += datetime.timedelta(days=1)
            start_date_str = max_date_time.strftime('%Y-%m-%d')
        return start_date_str

    def close_conn(self):
        """
        关闭pymysql连接、游标、sqlalchemy连接池的所有连接
        :return:提示
        """
        print("————————————————————————————————————————————————————————————————————————")
        self.session.close()
        print(self.db_dict['db_name'] + " 的sqlalchemy引擎_会话已关闭。")
        self.db_engine.dispose()
        print(self.db_dict['db_name'] + " 的sqlalchemy连接池的所有连接已关闭。")
        self.cursor.close()
        print(self.db_dict['db_name'] + " 的pymysql连接_游标已关闭。")
        self.db_conn.close()
        print(self.db_dict['db_name'] + " 的pymysql连接已关闭。")


def sql_dict_overwrite(target_db, sql_dict_sum):
    """
    基于DBHandle类实例，遍历sql_dict_sum后，批量“查询数据后删除插入”函数。
    :param target_db: 调用DBHandle类后的实例（要处理的目标数据库实例）
    :param sql_dict_sum:含delete_sql, append_table, data_sql键的汇总sql字典（格式参照update_sql_desc_XXXXXX文件）
    :return:
    """
    for sql_dict in sql_dict_sum:
        temp_data = target_db.select_data(sql_dict['data_sql'])
        target_db.delete_data(sql_dict['delete_sql'])
        target_db.append_data(
            sql_dict['append_table'],
            temp_data
        )
        print("————————————————————————————————————————————————————————————————————————————————————————")

