#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/19 3:25 下午
# software: PyCharm
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.decorators import login_required
import json, os


class MenuManagementResource(Resource):
    """
    router list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    def format_route_dg(self, _id, routerList, menuList):
        for item in routerList:
            label = item["meta"]['title']
            _id = _id + 1
            children = []
            menuList.append({"label": label, "id": _id, "children": children})
            if item.get("children"):
                return self.format_route_dg(_id, children, menuList)
        return menuList

    @login_required
    def get(self):
        """
        获取路由信息
        :return: json
        """
        filePath = os.path.join(os.path.join(os.getcwd(), 'router.json'))
        with open(filePath, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        _id = 0
        menuList = []
        format_router = []
        for item in load_dict["data"]:
            if "meta" not in item.keys():
                for i in item["children"]:
                    format_router.append(i)
            else:
                format_router.append(item)
        # test = self.format_route_dg(_id, format_router, menuList)
        # 第一层
        for item in format_router:
            label = item["meta"]['title']
            if label == "个人中心" or label == "文档管理" or label == "配置管理":
                continue
            _id = _id + 1
            children = []
            # 第二层
            if not item.get("children"):
                menuList.append({"label": label, "id": _id, "value": label})
            else:
                menuList.append({"label": label, "id": _id, "value": label, "children": children})
                for i2 in item["children"]:
                    label2 = i2["meta"]['title']
                    _id = _id + 1
                    children2 = []
                    # 第三层
                    if not i2.get("children"):
                        children.append({"label": label2, "id": _id, "value": label2})
                    else:
                        children.append({"label": label2, "id": _id, "value": label2, "children": children2})
                        for i3 in item["children"]:
                            label3 = i3["meta"]['title']
                            _id = _id + 1
                            children3 = []
                            # 第四层
                            if not i3.get("children"):
                                children2.append({"label": label3, "id": _id, "value": label3})
                            else:
                                children2.append({"label": label3, "id": _id, "value": label3, "children": children3})
                                for i4 in item["children"]:
                                    label4 = i4["meta"]['title']
                                    _id = _id + 1
                                    children4 = []
                                    # 第五层
                                    if not i4.get("children"):
                                        children3.append({"label": label4, "id": _id, "value": label4})
                                    else:
                                        children3.append({"label": label4, "id": _id, "value": label4, "children": children4})
                                        for i5 in item["children"]:
                                            label5 = i5["meta"]['title']
                                            _id = _id + 1
                                            children5 = []
                                            if not i5.get("children"):
                                                children4.append({"label": label5, "id": _id, "value": label5})
                                            else:
                                                children4.append(
                                                    {"label": label5, "id": _id, "value": label5, "children": children5})
        return pretty_result(code.OK, data=menuList)

    # @login_required
    # def get(self):
    #     """
    #     获取路由信息
    #     :return: json
    #     """
    #     filePath = os.path.join(os.path.join(os.getcwd(), 'router.json'))
    #     with open(filePath, 'r', encoding='utf-8') as load_f:
    #         load_dict = json.load(load_f)
    #     return pretty_result(code.OK, data=load_dict["data"])
