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


class RouterResource(Resource):
    """
    router list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        获取路由信息
        :return: json
        """
        self.parser.add_argument("permission", type=str, location="args", help='permission is json')
        args = self.parser.parse_args()
        print(args.permission)
        filePath = os.path.join(os.path.join(os.getcwd(), 'router.json'))
        with open(filePath, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        result = []
        for item in load_dict["data"]:
            pass
        return pretty_result(code.OK, data=load_dict["data"])
