# -*- coding:utf-8 -*-


# # 第九章——类
# class Dog:
#     feet_num = 4
#
#     def __init__(self, name, age):
#         self.name = name
#         self.__age = age
#
#     def call_name(self):
#         print(self.name + "快回来！")
#
#     def how_ago(self):
#         print("它今年 " + str(self.__age) + " 岁了！")
#
#     def update_ago(self, new_age):
#         self.__age = new_age
#
#     def increment_age(self, increment_age_num):
#         if increment_age_num > 0:
#             self.__age += increment_age_num
#         else:
#             pass
#
#     def __str__(self):
#         return "它的名字是%s,它今年%s岁了" % (self.name, str(self.__age))
#
#     @classmethod
#     def cm(cls):
#         print("我是类方法")
#
#     @staticmethod
#     def sm():
#         print("我是静态方法")
#
#
# class NewDog(Dog):
#
#     def __init__(self, name, age, like_food):
#         super().__init__(name, age)
#         self.like_food = like_food
#
#     def call_like_food(self):
#         print("它最喜欢的食物是： " + self.like_food)
#
#
# my_dog_n = NewDog("think", 2, "chicken")
# my_dog = Dog("danny", 1)
#
# print(my_dog)


class Animal(object):
    def eat(self):
        print("动物会吃")


class Dog(Animal):
    def eat(self):
        print("狗吃骨头")


class Cat(Animal):
    def eat(self):
        print("猫吃鱼")






