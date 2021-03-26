#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/8 10:14 下午
# software: PyCharm

from flask import jsonify, request, current_app, g
from models.users import UsersModel
from models import db
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.vaild import password_len
from sqlalchemy.exc import SQLAlchemyError
from common.decorators import login_required


class ApprovalManagementResource(Resource):
    """
    users management资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        获取用户列表信息
        :return: json
        """
        data = {
          "code": 200,
          "msg": "获取成功",
          "data": {
            "deptId": 1,
            "deptName": "xxx公司"
          }
        }
        return data

    @login_required
    def post(self):
        data = {
            "code": 200,
            "msg": "获取成功",
            "data": [
                {
                    "userId": 20,
                    "userName": "张三",
                    "deptId": 1
                },
                {
                    "userId": 30,
                    "userName": "李四",
                    "deptId": 1
                },
                {
                    "userId": 40,
                    "userName": "王五",
                    "deptId": 1
                },
                {
                    "userId": 50,
                    "userName": "二麻子",
                    "deptId": 1
                },
                {
                    "userId": 60,
                    "userName": "富贵",
                    "deptId": 1
                }
            ]
        }
        return data

    @login_required
    def put(self):
        data = {
          "code": 200,
          "msg": "获取成功",
          "data": [
            {
              "deptId": 2,
              "deptName": "xxx财务部",
              "parentDeptId": 1
            },
            {
              "deptId": 3,
              "deptName": "xxx行政部",
              "parentDeptId": 1
            },
            {
              "deptId": 4,
              "deptName": "xxx研发部",
              "parentDeptId": 1
            },
            {
              "deptId": 5,
              "deptName": "xxx工程部",
              "parentDeptId": 1
            },
            {
              "deptId": 6,
              "deptName": "xxx后勤部",
              "parentDeptId": 1
            }
          ]
        }
        return data

    @login_required
    def delete(self):
        data = {
          "code": 200,
          "msg": "获取成功",
          "data": [
            {
              "userId": 20,
              "userName": "张三",
              "deptId": 1
            },
            {
              "userId": 30,
              "userName": "李四",
              "deptId": 1
            },
            {
              "userId": 40,
              "userName": "王五",
              "deptId": 1
            },
            {
              "userId": 50,
              "userName": "二麻子",
              "deptId": 1
            },
            {
              "userId": 60,
              "userName": "富贵",
              "deptId": 1
            }
          ]
        }
        return data
