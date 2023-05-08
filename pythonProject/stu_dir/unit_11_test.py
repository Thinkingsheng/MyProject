# -*- coding:utf-8 -*-

# from unit_11 import get_full_name
#
#
# def name_test():
#     print("任意时间输入 q 退出程序...")
#     while True:
#         first = input("\n请输入你的姓：")
#         if first == "q":
#             break
#         last = input("\n请输入你的名：")
#         if last == "q":
#             break
#     full_name = get_full_name(first, last)


# 测试函数
# import unittest
# from unit_11 import get_full_name
#
#
# class Unit11TestCase(unittest.TestCase):
#     """测试unit_11.py"""
#     def test_first_last_name(self):
#         """能够正确处理像Tang Zhisheng这样的名字吗？"""
#         full_name = get_full_name("tang", "sheng", "zhi")
#         self.assertEqual(full_name, "tang zhisheng")
#
#
# if __name__ == "__main__":
#     unittest.main()


# 测试类
# from stu_dir.unit_11 import CollectAnswers


# question = "你学的第一门编程语言是？"
# my_collect = CollectAnswers(question)
#
# my_collect.show_question()
# print("输入 q 退出调查\n")
# while True:
#     response = input("请输入回答:")
#     if response == 'q':
#         break
#     my_collect.store_response(response)
#
# print("\n感谢你们接受调查！")
# my_collect.show_result()


# from stu_dir.unit_11 import CollectMoreAnswers
#
#
# question = "你学的第一门编程语言是？"
# my_more_collect = CollectMoreAnswers(question)
#
# my_more_collect.show_question()
#
# print("输入 q 退出调查\n")
# while True:
#     name = input("请输入姓名:")
#     if name == 'q':
#         break
#     response = input("请输入回答（可多个答案，用逗号隔开）:")
#     if response == 'q':
#         break
#     my_more_collect.store_response(name, response)
#
# print("\n感谢你们接受调查！")
# my_more_collect.show_result()


# import unittest
# from stu_dir.unit_11 import CollectAnswers
#
#
# class TestCollectAnswers(unittest.TestCase):
#     """针对CollectAnswers类的测试"""
#
#     def setUp(self):
#         """创建一个调查对象和一组答案，供使用的测试方法使用"""
#         question = "你学的编程语言有哪些？"
#         self.my_collect = CollectAnswers(question)
#         self.responses = ['Java', 'Python', 'Linux']
#
#     def test_single_response(self):
#         """测试单个答案是否存储"""
#         self.my_collect.store_response(self.responses[0])
#         self.assertIn(self.responses[1], self.my_collect.responses)
#
#     def test_three_responses(self):
#         """测试三个答案是否存储"""
#         for response in self.responses:
#             self.my_collect.store_response(response)
#         for response in self.responses:
#             self.assertIn(response, self.my_collect.responses)
#
#
# if __name__ == "__main__":
#     unittest.main()


# import unittest
# from stu_dir.unit_11 import CollectMoreAnswers
#
#
# class TestCollectMoreAnswers(unittest.TestCase):
#
#     def test_store_single_response(self):
#         """测试单个答案"""
#         question = "你学的编程语言有哪些？"
#         my_more_collect = CollectMoreAnswers(question)
#         my_more_collect.store_response('Tang', 'Python')
#
#         self.assertIn('Python', my_more_collect.answers_dict['Tang'][0])
#
#     def test_store_more_response(self):
#         """测试单个答案"""
#         question = "你学的编程语言有哪些？"
#         my_more_collect = CollectMoreAnswers(question)
#         my_more_collect.store_response('Tang', 'Python,Java,Linux')
#
#         response_list = ['Python', 'Java', 'Linux']
#
#         for i in range(len(response_list)):
#             self.assertIn(response_list[i], my_more_collect.answers_dict['Tang'][i])
#
#
# if __name__ == "__main__":
#     unittest.main()


# 11-3
import unittest
from stu_dir.unit_11 import Employee


class TestEmployee(unittest.TestCase):

    def setUp(self):
        self.test_employee = Employee("Tang", "zhisheng", 11000)

    def test_give_default_raise(self):
        self.assertEqual(self.test_employee.first_name, "Tang")
        self.assertEqual(self.test_employee.last_name, "zhisheng")
        self.assertEqual(self.test_employee.year_salary, 11000)

    def test_give_custom_raise(self):
        self.test_employee.give_raise()
        self.assertEqual(self.test_employee.year_salary, 16000)


if __name__ == "__main__":
    unittest.main()
