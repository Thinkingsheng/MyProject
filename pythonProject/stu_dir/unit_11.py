# -*- coding:utf-8 -*-

# 第十一章——测试代码

# def get_full_name(first, last, middle=""):
#     if middle:
#         full_name = first + " " + middle + " " + last
#     else:
#         full_name = first + " " + last
#     return full_name

# from collections import Counter
#
#
# class CollectAnswers():
#     """收集调查问卷的答案"""
#
#     def __init__(self, question):
#         """存储一个问题，并为存储答案做准备"""
#         self.question = question
#         self.responses = []
#
#     def show_question(self):
#         """显示调查问卷"""
#         print(self.question)
#
#     def store_response(self, new_response):
#         """存储单份调查答卷"""
#         self.responses.append(new_response)
#
#     def show_result(self):
#         """显示收集到的答案"""
#         print("收集到的答案为：")
#         for response in self.responses:
#             print("- " + response)
#
#
# class CollectMoreAnswers(CollectAnswers):
#
#     def __init__(self, question):
#         super().__init__(question)
#         self.answers_dict = {}
#
#     def store_response(self, name: str, new_response: str):
#         """存储调查问卷"""
#         # 简单去除空格符
#         new_response = new_response.replace(" ", "")
#         # 将答案全部进行切割，返回列表
#         response_list = new_response.split(",", -1)
#         # 存入到回复字典
#         self.answers_dict[name] = response_list
#
#     def show_result(self):
#         """显示收集到的答案，及统计其答案个数"""
#         print("收集到的答案为：")
#         for key, value_list in self.answers_dict.items():
#             print("%s的回答是：%s" % (key, value_list))
#         print("收集到答案的统计：")
#         sum_v_list = []
#         for value_list in self.answers_dict.values():
#             for value in value_list:
#                 sum_v_list.append(value)
#         c = Counter(sum_v_list)
#         print(dict(c))


# 11-3
class Employee():
    def __init__(self, first_name, last_name, year_salary):
        self.first_name = first_name
        self.last_name = last_name
        self.year_salary = year_salary

    def give_raise(self, salary_increase=5000):
        if salary_increase > 0:
            self.year_salary += salary_increase
        else:
            print("上调薪资输入有误！")
