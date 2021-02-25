#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/21 9:22 下午
# software: PyCharm

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
from common.utils import createFile
import os

project_path = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + "/../"
backend_path = os.path.join(os.path.abspath(project_path), "Doc")
split_mark = "---***---"


class DocManagementResource(Resource):
    """
    doc management资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        获取文档信息
        :return: json
        """
        self.parser.add_argument("language", type=str, required=True, location="args",
                                 help='Please choose language!')
        self.parser.add_argument("menu", type=str, required=True, location="args", help='Please choose menu')
        args = self.parser.parse_args()
        lang_path = os.path.join(backend_path, args.language)
        try:
            with open(os.path.join(lang_path, args.menu + '.txt'), 'r', encoding="utf-8") as f:
                contentList = f.read().split(split_mark)
                title = contentList[0]
                content = contentList[1]
        except Exception as e:
            title = ""
            content = ""
        data = {"title": title, "language": args.language, "menu": [args.menu], "content": content}
        return pretty_result(code.OK, data=data, msg='get file filed！')

    @login_required
    def post(self):
        """
        创建文档信息
        :return: json
        """
        self.parser.add_argument("language", type=str, required=True, location="json",
                                 help='Please choose language')
        self.parser.add_argument("menu", type=list, required=True, location="json", help='Please choose menu')
        self.parser.add_argument("title", type=str, required=True, location="json", help='Please input title')
        self.parser.add_argument("content", type=str, required=True, location="json", help='Please input content')
        args = self.parser.parse_args()
        lang_path = os.path.join(backend_path, args.language)
        createFile(lang_path)
        with open(os.path.join(lang_path, args.menu[0] + '.txt'), 'w', encoding="utf-8") as f:
            f.write(args.title + split_mark + args.content)
        return pretty_result(code.OK, msg='文档创建成功！')


    @login_required
    def put(self):
        self.parser.add_argument("id", type=int, required=True, location="json", help='id is required')
        self.parser.add_argument("email", type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
                                 required=True, location="json",
                                 help='email format is incorrect')
        self.parser.add_argument("permission", type=str, choices=['test', 'guest', 'user', 'admin', 'superAdmin'],
                                 required=True, location="json",
                                 help='permission is required and only (test,user,admin,superAdmin)')
        self.parser.add_argument("password", type=password_len, location="json", trim=True)
        args = self.parser.parse_args()
        userEmailInfo = UsersModel.query.filter_by(email=args.email).all()
        for item in userEmailInfo:
            if item.id != args.id:
                return pretty_result(code.ERROR, msg='该邮箱已经被注册！')
        userInfo = UsersModel.query.filter_by(id=args.id).first()
        userInfo.email=args.email
        userInfo.permission=args.permission
        if args.password:
            userInfo.password=UsersModel.set_password(UsersModel, args.password)
        UsersModel.update(userInfo)
        return pretty_result(code.OK, msg='用户信息更新成功！')

    @login_required
    def delete(self):
        self.parser.add_argument("ids", type=list, required=True, location="json", help='ids is required')
        args = self.parser.parse_args()
        UsersModel.delete(UsersModel, args.ids)
        return pretty_result(code.OK, msg='用户信息删除成功！')
