# -*- coding:utf-8 -*-


# # 第十章——文件和异常
# file_reader.py

# with open(r"C:\Users\Think\Desktop\Input_data\Test1\pi_digits.txt") as file_object:
#     contents = file_object.read()
#     print(contents)
#
# with open(r"C:\Users\Think\Desktop\Input_data\Test1\pi_digits.txt") as file_object:
#     for line in file_object:
#         print(line)
#
# with open(r"C:\Users\Think\Desktop\Input_data\Test1\pi_digits.txt") as file_object:
#     lines = file_object.readlines()
# for line in lines:
#     print(line)
#
# with open(r"C:\Users\Think\Desktop\output_data\Test1\programming.txt", "a") as f:
#     f.write("\nI love programming.")
#     f.write("\nI love python.")

# 10-3 访客
# message = ""
#
# with open(r"C:\Users\Think\Desktop\output_data\Test1\name.txt", "a") as f:
#     while message != "no":
#         name = input("请问你的名字是：")
#         print("Hi,%s!" % name)
#         f.write("%s\n" % name)
#         message = input("姓名已添加，请问还要继续吗？（若要退出则输入no）")

# def count_works(file_path):
#     try:
#         with open(file_path) as f:
#             contents = f.read()
#     except FileNotFoundError:
#         pass
#     else:
#         works = contents.split()
#         work_num = len(works)
#         print("文件路径:%s\n单词数：%s" % (file_path, str(work_num)))
#
#
# count_works(r"C:\Users\Think\Desktop\Input_data\Test1\English_1.txt")
# count_works(r"C:\Users\Think\Desktop\Input_data\Test1\English_3.txt")
# count_works(r"C:\Users\Think\Desktop\Input_data\Test1\English_2.txt")

# 10-6 加法运算
# a = True
# while a:
#     num_1 = input("请输入数字1：")
#     num_2 = input("请输入数字2：")
#     try:
#         answer = int(num_1) + int(num_2)
#     except ValueError:
#         print("输入有误，请输入数字")
#         continue
#     else:
#         print("计算结果为:%s" % str(answer))
#         a = False

# 10-8 猫和狗
# def read_file(path):
#     try:
#         with open(path) as f:
#             contents = f.read()
#     except FileNotFoundError:
#         pass
#     else:
#         print(contents)
#
#
# read_file(r"C:\Users\Think\Desktop\Input_data\Test1\cats.txt")
# read_file(r"C:\Users\Think\Desktop\Input_data\Test1\dogs.txt")
# read_file(r"C:\Users\Think\Desktop\Input_data\Test1\alice.txt")

# 10-9 常见单词
# try:
#     with open(r"C:\Users\Think\Desktop\Input_data\Test1\English_3.txt") as f:
#         contents = f.read()
# except FileNotFoundError:
#     print("文件路径错误！")
# else:
#     print("该文件内'the'的出现个数为:%s" % str(contents.lower().count("the")))

# import json
#
# number = [3, 6, 8, 14, 22]
# file_path = r"C:\Users\Think\Desktop\Input_data\Test1\json_1.json"
# with open(file_path, 'w') as f:
#     json.dump(number, f)

# import json
# import codecs
#
# file_path = r"C:\Users\Think\Desktop\Input_data\Test1\json_3.json"
# with codecs.open(file_path, "r", "utf-8") as f:
#     num_str = json.load(f)
# print(num_str)
# print(type(num_str))
# print(dir(num_str))

# import json
#
# username = input("请输入你的姓名：")
# file_path = r"C:\Users\Think\Desktop\Input_data\Test1\username.json"
#
# with open(file_path, 'w') as f:
#     json.dump(username, f)
#     print("%s已添加到json文档。" % username)

# import json
#
# file_path = r"C:\Users\Think\Desktop\Input_data\Test1\username.json"
# with open(file_path) as f:
#     name_str = json.load(f)
# print(name_str)

# import json
#
#
# def greet_user():
#     """问候用户，并指出其名字"""
#     path = r"C:\Users\Think\Desktop\Input_data\Test1\username.json"
#     try:
#         with open(path) as f:
#             name_str = json.load(f)
#     except FileNotFoundError:
#         name_str = input("请输入你的姓名：")
#         with open(path, 'w') as f:
#             json.dump(name_str, f)
#         print("%s已添加到json文档。" % name_str)
#     else:
#         print("Hi,%s" % name_str)
#
#
# greet_user()

# import json
#
#
# def get_stored_username():
#     """如果存储了用户名，就获取它"""
#     path = r"C:\Users\Think\Desktop\Input_data\Test1\username.json"
#     try:
#         with open(path) as f:
#             username = json.load(f)
#     except FileNotFoundError:
#         return None
#     else:
#         return username
#
#
# def get_new_name():
#     """提示用户输入用户名"""
#     username = input("请输入你的姓名：")
#     path = r"C:\Users\Think\Desktop\Input_data\Test1\username.json"
#     with open(path, 'w') as f:
#         json.dump(username, f)
#     return username
#
#
# def greet_user():
#     """问候用户，并指出其名字"""
#     username = get_stored_username()
#     if username:
#         print("Hi,%s" % username)
#     else:
#         username = get_new_name()
#         print("%s已添加到json文档。" % username)
#
#
# greet_user()

# 10-11
# import json
#
#
# def get_history_like_num():
#     try:
#         with open(r"C:\Users\Think\Desktop\Input_data\Test1\likenum.json") as f:
#             like_num = json.load(f)
#     except FileNotFoundError:
#         return None
#     else:
#         return like_num
#
#
# def get_like_num():
#     like_num = input("请问你喜欢的数字是：")
#     with open(r"C:\Users\Think\Desktop\Input_data\Test1\likenum.json", 'w') as f:
#         json.dump(like_num, f)
#     return like_num
#
#
# def check_like_num():
#     like_num = get_history_like_num()
#     if like_num:
#         print("我知道了你喜欢的数字，是%s" % like_num)
#     else:
#         like_num = get_like_num()
#         print("你最喜欢的数字%s已添加到json文档。" % like_num)

# 10-12
# import json
#
#
# def check_like_num():
#     try:
#         with open(r"C:\Users\Think\Desktop\Input_data\Test1\likenum.json") as f:
#             like_num = json.load(f)
#         print("我知道了你喜欢的数字，是%s" % like_num)
#     except FileNotFoundError:
#         like_num = input("请问你喜欢的数字是：")
#         with open(r"C:\Users\Think\Desktop\Input_data\Test1\likenum.json", 'w') as f:
#             json.dump(like_num, f)
#         print("你最喜欢的数字%s已添加到json文档。" % like_num)
#     else:
#         pass

# 10-13
import json


def get_stored_username():
    """如果存储了用户名，就获取它"""
    path = r"C:\Users\Think\Desktop\Input_data\Test1\username.json"
    try:
        with open(path) as f:
            username = json.load(f)
    except FileNotFoundError:
        return None
    else:
        return username


def get_new_name():
    """提示用户输入用户名"""
    username = input("请输入你的姓名：")
    path = r"C:\Users\Think\Desktop\Input_data\Test1\username.json"
    with open(path, 'w') as f:
        json.dump(username, f)
    return username


def greet_user():
    """问候用户，并指出其名字"""
    username = get_stored_username()
    if username:
        b = True
        while b:
            a = int(input("请问： %s 是否您的姓名？（1为是，0为否）：\n" % username))
            if a == 1:
                print("Hi,%s" % username)
                b = False
            elif a == 0:
                username = get_new_name()
                print("%s 已更改到json文档。" % username)
                b = False
            else:
                print("输入有误，请重新输入。。。")
                b = True
    else:
        username = get_new_name()
        print("%s 已添加到json文档。" % username)


greet_user()


