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
from models.roles import RolesModel
from models import db
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common import code, pretty_result
from common.vaild import password_len
from sqlalchemy.exc import SQLAlchemyError
from common.decorators import login_required


class RoleManagementResource(Resource):
    """
    roles management资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @login_required
    def get(self):
        """
        获取权限列表信息
        :return: json
        """
        self.parser.add_argument("pageNo", type=int, required=True, location="args",
                                 help='pageNo is required')
        self.parser.add_argument("pageSize", type=int, required=True, location="args", help='pageSize is required')
        self.parser.add_argument("postion", type=str, location="args", help='postion is required')

        args = self.parser.parse_args()
        role_list = RolesModel.paginate(RolesModel, args.pageNo, args.pageSize)
        items = []
        totalCount = role_list.total
        role_list = role_list.items
        if args.postion:
            role_list = RolesModel.filter_by_postion(RolesModel, args.postion)
            totalCount = len(role_list)
        for role in role_list:
            items.append(
                {
                    'id': role.id,
                    'department': role.department,
                    'departmentID': role.departmentID,
                    'postion': role.postion,
                    'postionID': role.postionID,
                    'permission': role.permission,
                }
            )
        data = {
            'pageNo': args.pageNo,
            'pageSize': args.pageSize,
            'totalCount': totalCount,
            'items': items
        }
        return pretty_result(code.OK, data=data, msg='权限信息获取成功！')

    @login_required
    def post(self):
        """
        创建权限
        :return: json
        """
        self.parser.add_argument("department", type=str, required=True, location="json",
                                 help='department is required')
        self.parser.add_argument("departmentID", type=str, required=True, location="json",
                                 help='departmentID is required')
        self.parser.add_argument("postion", type=str, required=True, location="json", help='postion is required')
        self.parser.add_argument("postionID", type=str, required=True, location="json", help='postionID is required')
        self.parser.add_argument("permission", type=str, required=True, location="json", help='permission is required')
        args = self.parser.parse_args()
        rolePostionIDInfo = RolesModel.query.filter_by(postionID=args.postionID).all()
        if rolePostionIDInfo:
            return pretty_result(code.ERROR, msg='该职位已经被添加！')
        role = RolesModel(department=args.department, departmentID=args.departmentID, postion=args.postion, postionID=args.postionID, permission=args.permission)
        result = RolesModel.add(RolesModel, role)
        if role.id:
            returnUser = {
                'id': role.id,
                'department': role.department,
                'departmentID': role.departmentID,
                'postion': role.postion,
                'postionID': role.postionID,
                'permission': role.permission
            }
            return pretty_result(code.OK, data=returnUser, msg='权限添加成功')
        else:
            return pretty_result(code.ERROR, data='', msg='权限添加失败')

    @login_required
    def put(self):
        self.parser.add_argument("id", type=int, required=True, location="json", help='id is required')
        self.parser.add_argument("department", type=str, required=True, location="json",
                                 help='department is required')
        self.parser.add_argument("departmentID", type=str, required=True, location="json", help='departmentID is required')
        self.parser.add_argument("postion", type=str, required=True, location="json", help='postion is required')
        self.parser.add_argument("postionID", type=str, required=True, location="json", help='postionID is required')
        self.parser.add_argument("permission", type=str, required=True, location="json", help='permission is required')
        args = self.parser.parse_args()
        roleInfo = RolesModel.query.filter_by(id=args.id).first()
        roleInfo.department = args.department
        roleInfo.departmentID = args.departmentID
        roleInfo.postion = args.postion
        roleInfo.postionID = args.postionID
        roleInfo.permission = args.permission
        RolesModel.update(roleInfo)
        return pretty_result(code.OK, msg='权限信息更新成功！')

    @login_required
    def delete(self):
        self.parser.add_argument("ids", type=list, required=True, location="json", help='ids is required')
        args = self.parser.parse_args()
        RolesModel.delete(RolesModel, args.ids)
        return pretty_result(code.OK, msg='权限信息删除成功！')
