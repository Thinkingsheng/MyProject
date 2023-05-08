# -*- coding:utf-8 -*-

# import json
#
# def loadJsonData(filename):
#     with open(filename) as f:
#         paper_data = json.load(f)
#         return paper_data
#
# def data_clean(paper_data):
#     author_name = []
#     author_org = []
#     paper_keywords = []
#     for id in paper_data.keys():
#         authors = paper_data[id]["authors"]
#         if "keywords" in paper_data[id].keys():
#             for i in range(len(authors)):
#                 paper_keywords.append(paper_data[id]["keywords"])
#         else:
#             for i in range(len(authors)):
#                 paper_keywords.append(" ")
#         for each in authors:
#             temp = list(each.values())
#             if len(temp) == 1:
#                 author_name.append(temp[0])
#                 author_org.append(" ")
#             else:
#                 author_name.append(temp[0])
#                 author_org.append(temp[1])
#     return author_name, author_org, paper_keywords

# filepath = r"C:\Users\Think\Desktop\response_1665475162198.json"


# author_dict = loadJsonData(filepath)
# author_name, author_org, author_keywords = author(author_dict)


import pandas as pd
import json

filepath = r"C:\Users\Think\Desktop\response_1665475162198.json"

def loadJsonData(filename):
    with open(filename) as f:
        paper_data = json.load(f)
        return paper_data


clean_data =loadJsonData(filepath)['data']['flow']

df = pd.DataFrame(clean_data)
print(df)