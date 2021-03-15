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

    def get_menu_checked_by_permission(self, routeLIst, permission, result):
        if len(routeLIst):
            for item in routeLIst:
                if item.get("children"):
                    self.get_menu_checked_by_permission(item.get("children"), permission, result)
                else:
                    if permission in item.get("meta").get("permissions"):
                        result.append(item.get("name"))
        return result

    def add_menu_permission(self, routeLIst, permission, names):
        if len(routeLIst):
            for item in routeLIst:
                if item.get("name") in names:
                    if permission not in item.get("meta").get("permissions"):
                        item.get("meta").get("permissions").append(permission)
                else:
                    if permission in item.get("meta").get("permissions"):
                        item.get("meta").get("permissions").remove(permission)
                if item.get("children"):
                    self.add_menu_permission(item.get("children"), permission, names)
        return routeLIst

    @login_required
    def get(self):
        """
        获取菜单选中状态
        :return: json
        """
        self.parser.add_argument("permission", required=True, type=str, location="args", help='permission is str')
        args = self.parser.parse_args()
        filePath = os.path.join(os.path.join(os.getcwd(), 'router.json'))
        with open(filePath, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        menuList = self.get_menu_checked_by_permission(load_dict["data"], args.permission, [])
        return pretty_result(code.OK, data=menuList)

    @login_required
    def put(self):
        """
        更新菜单权限信息
        :return: json
        """
        self.parser.add_argument("permission", required=True, type=str, location="json", help='permission is str')
        self.parser.add_argument("names", required=True, type=list, location="json", help='names is list')
        args = self.parser.parse_args()
        filePath = os.path.join(os.path.join(os.getcwd(), 'router.json'))
        with open(filePath, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        menuList = self.add_menu_permission(load_dict["data"], args.permission, args.names)
        data = {
            "code": 200,
            "msg": "success",
            "data": menuList
        }
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))
        return pretty_result(code.OK)

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
