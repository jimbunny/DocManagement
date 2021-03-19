#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2020/6/7 10:14 下午
# software: PyCharm

from flask import Blueprint
from flask_restful import Api
from resources import profiles, users, login, auths, routers, userManagement, roleManagement, menuManagement, \
    iconManagement, docManagement, language

api_v1 = Blueprint('api_v1', __name__)

api = Api(api_v1)

api.add_resource(profiles.ProfileListResource, '/profiles', endpoint='profiles')
api.add_resource(profiles.ProfileResource, '/profiles/<string:id>')
api.add_resource(users.UserResource, '/user/info')
api.add_resource(login.RegisterResource, '/register')
api.add_resource(login.LoginResource, '/login')
api.add_resource(login.LogoutResource, '/logout')
api.add_resource(auths.AuthorizationResource, '/refresh/token')
# menu management
api.add_resource(routers.RouterResource, '/menu/navigate', endpoint='getRouter')
api.add_resource(routers.RouterResource, '/router/doEdit', endpoint='putRouter')
api.add_resource(menuManagement.MenuManagementResource, '/menuManagement/getCheckedMenu', endpoint='getCheckedMenu')
api.add_resource(menuManagement.MenuManagementResource, '/menuManagement/doPermissionEdit', endpoint='putPermissionEdit')
# user management
api.add_resource(userManagement.UserManagementResource, '/userManagement/getList', endpoint='getUser')
api.add_resource(userManagement.UserManagementResource, '/userManagement/doEdit', endpoint='editUser')
api.add_resource(userManagement.UserManagementResource, '/userManagement/doDelete', endpoint='deleteUser')
api.add_resource(userManagement.UserManagementResource, '/userManagement/doEditUser', endpoint='postUser')
api.add_resource(login.RegisterResource, '/userManagement/doAdd', endpoint='addUser')
# role management
api.add_resource(roleManagement.RoleManagementResource, '/roleManagement/getList', endpoint='getRole')
api.add_resource(roleManagement.RoleManagementResource, '/roleManagement/doAdd', endpoint='addRole')
api.add_resource(roleManagement.RoleManagementResource, '/roleManagement/doEdit', endpoint='editRole')
api.add_resource(roleManagement.RoleManagementResource, '/roleManagement/doDelete', endpoint='deleteRole')
api.add_resource(roleManagement.PermissionResource, '/roleManagement/checkPermission', endpoint='postCheckPermission')

api.add_resource(iconManagement.ColorfulIconResource, '/icon/getList')

api.add_resource(language.LanguageResource, '/language/i18n', endpoint='getLanguage')
api.add_resource(language.LanguageResource, '/language/getTitle', endpoint='getTitle')
api.add_resource(language.LanguageResource, '/language/doEdit', endpoint='putTitle')
api.add_resource(language.LanguageResource, '/language/doDelete', endpoint='deleteTitle')
api.add_resource(language.LanguageFileResource, '/language/doEditFile', endpoint='putLanguageFile')
# doc management
api.add_resource(docManagement.DocManagementResource, '/docManagement/getFile', endpoint='deleteFile')
api.add_resource(docManagement.DocManagementResource, '/docManagement/doAdd', endpoint='addFile')
