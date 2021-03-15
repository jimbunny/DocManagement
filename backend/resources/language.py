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


class LanguageResource(Resource):
    """
    router list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        """
        获取语言信息
        :return: json
        """
        self.parser.add_argument("language", required=True, type=str, location="args", help='language is str')
        args = self.parser.parse_args()
        filePath = os.path.join(os.path.join(os.getcwd(), args.language + '.json'))
        with open(filePath, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        return pretty_result(code.OK, data=load_dict["data"])

    @login_required
    def post(self):
        """
        获取title信息
        :return: json
        """
        self.parser.add_argument("language", required=True, type=str, location="json", help='language is str')
        self.parser.add_argument("title", required=True, type=str, location="json", help='title is str')
        args = self.parser.parse_args()
        filePath = os.path.join(os.path.join(os.getcwd(), args.language + '.json'))
        with open(filePath, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        title = load_dict["data"].get("route").get(args.title)
        return pretty_result(code.OK, data={"language": args.language, "title": title})

    @login_required
    def put(self):
        """
        更新title信息
        :return: json
        """
        self.parser.add_argument("language", required=True, type=str, location="json", help='language is str')
        self.parser.add_argument("title", required=True, type=str, location="json", help='title is str')
        self.parser.add_argument("name", required=True, type=str, location="json", help='name is str')
        args = self.parser.parse_args()
        filePath = os.path.join(os.path.join(os.getcwd(), args.language + '.json'))
        with open(filePath, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        try:
            load_dict["data"]["route"][args.name] = args.title
            with open(filePath, 'w', encoding='utf-8') as file:
                file.write(json.dumps(load_dict))
        except Exception as e:
            return pretty_result(code.ERROR, msg="标题更新失败！")
        return pretty_result(code.OK, data="")

    @login_required
    def delete(self):
        """
        删除title信息
        :return: json
        """
        self.parser.add_argument("language", required=True, type=str, location="json", help='language is str')
        self.parser.add_argument("name", required=True, type=str, location="json", help='name is str')
        args = self.parser.parse_args()
        filePath = os.path.join(os.path.join(os.getcwd(), args.language + '.json'))
        with open(filePath, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        try:
            del load_dict["data"]["route"][args.name]
            with open(filePath, 'w', encoding='utf-8') as file:
                file.write(json.dumps(load_dict))
        except Exception as e:
            return pretty_result(code.ERROR, msg="标题删除失败！")
        return pretty_result(code.OK, data="")


class LanguageFileResource(Resource):
    """
    router list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def put(self):
        """
        更新语言文件信息
        :return: json
        """
        self.parser.add_argument("type", type=str, location="json", help='type is str')
        self.parser.add_argument("language", type=dict, location="json", help='language is dict')
        args = self.parser.parse_args()
        data = {
            "code": 200,
            "msg": "success",
            "data": args.language
        }
        filePath = os.path.join(os.path.join(os.getcwd(), args.type + '.json'))
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))
        return pretty_result(code.OK, data=args.language)