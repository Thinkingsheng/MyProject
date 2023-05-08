# -*- coding:utf-8 -*-


# # 9-13 使用 OrderedDict
# from collections import OrderedDict
#
# letter_dict = OrderedDict()
# small_letters = [chr(i) for i in range(97, 123)]
# big_letters = [chr(i) for i in range(65, 91)]
#
# for i in range(len(small_letters)):
#     letter_dict[small_letters[i]] = big_letters[i]
#
# print(letter_dict)


# # 9-14 骰子
# from random import randint
#
#
# class Die():
#     """
#     模拟骰子类
#     """
#     def __init__(self, sides=6):
#         self.sides = sides
#         print("创建了一个 %s 面骰子。" % str(sides))
#
#     def roll_die(self):
#         """模拟投掷一次"""
#         return randint(1, self.sides)
#
#     def repeat_roll_die(self, roll_times):
#         """模拟重复投掷多次"""
#         print("以下投掷 %s 次：" % str(roll_times))
#         for i in range(roll_times):
#             print("第%s次投掷结果：" % str(i+1) + str(randint(1, self.sides)))
#
#
# six_sides = Die()
# six_sides.repeat_roll_die(10)
#
# ten_sides = Die(10)
# ten_sides.repeat_roll_die(10)
#
# twenty_sides = Die(20)
# twenty_sides.repeat_roll_die(10)
print(1)
