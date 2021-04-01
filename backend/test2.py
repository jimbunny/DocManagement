
# import json
#
# with open("test.json", 'r', encoding='utf-8') as load_f:
#     load_dict = json.load(load_f)["data"]
#     print(json.dumps(load_dict))
import requests
import json
from requests.cookies import RequestsCookieJar
from openpyxl import load_workbook
from openpyxl import Workbook
import time
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE


baseUrl = 'http://vipapp.jtexpress.co.th/index.php/admin/parseerr/all_ajax.html?'
cookie_jar = RequestsCookieJar()
cookie_jar.set("PHPSESSID", "s7jr2msrl1oompkcfl5irhni61", domain="vipapp.jtexpress.co.th")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}


def getData(url):
    html = requests.get(url=url,cookies=cookie_jar, headers=headers).content
    data = json.loads(html.decode()).get("data")
    return data


def writeFile(data, file):
    wb1 = Workbook()
    # print(wb1.get_sheet_names())
    # 新建了一个工作表，尚未保存
    sheet = wb1.active
    sheet.title = 'Sheet1'
    # 直接给单元格赋值
    # sheet.append(["fid", "fvipid", 'fadd_time', "fadddr"])
    sheet.append(["fadddr"])
    for item in data:
        # sheet.append([item.get("fid"), item.get("fvipid"), item.get('fadd_time'), ILLEGAL_CHARACTERS_RE.sub(r'', item.get("faddr"))])
        sheet.append([ILLEGAL_CHARACTERS_RE.sub(r'', item.get("faddr"))])
    wb1.save(file)


if __name__ == '__main__':
    pages = 4
    limit = 50000
    data = []
    for i in range(pages):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("开始请求第" + str(i+1) + "页数据")
        url = baseUrl + 'page=' + str(i+1) + '&limit=' + str(limit)
        print("请求的url为：" + str(url))
        data = data + getData(url)
        print("请求第" + str(i + 1) + "页数据结束")
    i = 0
    print("开始写入第" + str(i+1) + "页数据")
    writeFile(data, "data_" + str(i+1) + ".xlsx")
    print("第" + str(i+1) + "页数据写入完成")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


{
  "code": 200,
  "msg": "success",
  "data": [
    {
      "path": "/",
      "component": "Layout",
      "redirect": "/index",
      "children": [
        {
          "path": "/index",
          "name": "Index",
          "component": "personalCenter/index",
          "meta": {
            "title": "personalCenter",
            "icon": "home",
            "affix": true,
            "noKeepAlive": true
          }
        }
      ]
    },
    {
      "path": "/doc",
      "component": "Layout",
      "redirect": "/docManagement",
      "children": [
        {
          "path": "/docManagement",
          "name": "DocManagement",
          "component": "docManagement/index",
          "meta": {
            "title": "docManagement",
            "icon": "marker",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          }
        }
      ]
    },
    {
      "path": "/test",
      "component": "Layout",
      "redirect": "/test",
      "children": [
        {
          "path": "/test",
          "name": "Test",
          "component": "test/index",
          "meta": {
            "title": "test",
            "icon": "bookmark",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          }
        }
      ]
    },
    {
      "path": "/approvalFlow",
      "component": "Layout",
      "name": "ApprovalFlow",
      "alwaysShow": true,
      "meta": {
        "title": "approvalFlow",
        "icon": "calculator",
        "permissions": [
          "SuperAdmin",
          "admin"
        ]
      },
      "children": [
        {
          "path": "/flowApproval",
          "name": "FlowApproval",
          "component": "approvalFlow/flowApproval/index",
          "meta": {
            "title": "flowApproval",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          },
          "children": [
            {
              "path": "/dataUpdateApproval",
              "name": "DataUpdateApproval",
              "component": "approvalFlow/flowApproval/dataUpdateApproval/index",
              "meta": {
                "title": "dataUpdateApproval",
                "permissions": [
                  "SuperAdmin",
                  "admin"
                ]
              }
            },
            {
              "path": "/permissionUpdateApproval",
              "name": "PermissionUpdateApproval",
              "component": "approvalFlow/flowApproval/permissionUpdateApproval/index",
              "meta": {
                "title": "permissionUpdateApproval",
                "permissions": [
                  "SuperAdmin",
                  "admin"
                ]
              }
            }
          ]
        },
        {
          "path": "/myApproval",
          "name": "MyApproval",
          "component": "approvalFlow/myApproval/index",
          "alwaysShow": true,
          "meta": {
            "title": "myApproval",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          },
          "children": [
            {
              "path": "/myApprovalDetail",
              "name": "MyApprovalDetail",
              "component": "approvalFlow/flowApproval/myApprovalDetail/index",
              "meta": {
                "title": "myApprovalDetail",
                "permissions": [
                  "SuperAdmin",
                  "admin"
                ]
              }
            }
          ]
        },
        {
          "path": "/waitMyApproval",
          "name": "WaitMyApproval",
          "component": "approvalFlow/waitMyApproval/index",
          "alwaysShow": true,
          "meta": {
            "title": "waitMyApproval",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          },
          "children": [
            {
              "path": "/waitMyApprovalDetail",
              "name": "WaitMyApprovalDetail",
              "component": "approvalFlow/flowApproval/waitMyApprovalDetail/index",
              "meta": {
                "title": "waitMyApprovalDetail",
                "permissions": [
                  "SuperAdmin",
                  "admin"
                ]
              }
            }
          ]
        },
        {
          "path": "/approvalByMe",
          "name": "ApprovalByMe",
          "component": "approvalFlow/approvalByMe/index",
          "alwaysShow": true,
          "meta": {
            "title": "approvalByMe",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          },
          "children": [
            {
              "path": "/approvalByMeDetail",
              "name": "ApprovalByMeDetail",
              "component": "approvalFlow/flowApproval/approvalByMeDetail/index",
              "meta": {
                "title": "approvalByMeDetail",
                "permissions": [
                  "SuperAdmin",
                  "admin"
                ]
              }
            }
          ]
        },
        {
          "path": "/ccToMe",
          "name": "CcToMe",
          "component": "approvalFlow/ccToMe/index",
          "alwaysShow": true,
          "meta": {
            "title": "ccToMe",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          },
          "children": [
            {
              "path": "/ccToMeDetail",
              "name": "CcToMeDetail",
              "component": "approvalFlow/flowApproval/ccToMeDetail/index",
              "meta": {
                "title": "ccToMeDetail",
                "permissions": [
                  "SuperAdmin",
                  "admin"
                ]
              }
            }
          ]
        },
        {
          "path": "/flowSearch",
          "name": "FlowSearch",
          "component": "approvalFlow/flowSearch/index",
          "alwaysShow": true,
          "meta": {
            "title": "flowSearch",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          },
          "children": [
            {
              "path": "/flowSearchDetail",
              "name": "FlowSearchDetail",
              "component": "approvalFlow/flowApproval/flowSearchDetail/index",
              "meta": {
                "title": "flowSearchDetail",
                "permissions": [
                  "SuperAdmin",
                  "admin"
                ]
              }
            }
          ]
        },{
          "path": "/flowSetting",
          "name": "FlowSetting",
          "component": "approvalFlow/FlowSetting/index",
          "alwaysShow": true,
          "meta": {
            "title": "flowSetting",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          },
          "children": [
            {
              "path": "/defineFlow",
              "name": "DefineFlow",
              "component": "approvalFlow/flowApproval/defineFlow/index",
              "meta": {
                "title": "defineFlow",
                "permissions": [
                  "SuperAdmin",
                  "admin"
                ]
              }
            }
          ]
        },
        {
          "path": "/approvalConfig",
          "name": "ApprovalConfig",
          "component": "approvalFlow/approvalConfig/index",
          "meta": {
            "title": "approvalConfig",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          }
        },
        {
          "path": "/approvalTask",
          "name": "ApprovalTask",
          "component": "approvalFlow/approvalTask/index",
          "meta": {
            "title": "approvalTask",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          }
        }
      ]
    },
    {
      "path": "/personnelManagement",
      "component": "Layout",
      "redirect": "noRedirect",
      "name": "PersonnelManagement",
      "alwaysShow": false,
      "meta": {
        "title": "configManagement",
        "icon": "users-cog",
        "permissions": [
          "SuperAdmin",
          "admin"
        ]
      },
      "children": [
        {
          "path": "/userManagement",
          "name": "UserManagement",
          "component": "personnelManagement/userManagement/index",
          "meta": {
            "title": "userManagement",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          }
        },
        {
          "path": "/departmentManagement",
          "name": "DepartmentManagement",
          "component": "personnelManagement/departmentManagement/index",
          "meta": {
            "title": "departmentManagement",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          }
        },
        {
          "path": "/roleManagement",
          "name": "RoleManagement",
          "component": "personnelManagement/roleManagement/index",
          "meta": {
            "title": "roleManagement",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          }
        },
        {
          "path": "/menuManagement",
          "name": "MenuManagement",
          "component": "personnelManagement/menuManagement/index",
          "meta": {
            "title": "menuManagement",
            "permissions": [
              "SuperAdmin",
              "admin"
            ]
          }
        },
        {
          "path": "/permission",
          "name": "PermissionTest",
          "component": "personnelManagement/permissionTest/index",
          "meta": {
            "title": "permissionTest",
            "permissions": [
              "SuperAdmin"
            ]
          }
        },
        {
          "path": "awesomeIcon",
          "name": "AwesomeIcon",
          "component": "byui/icon/index",
          "meta": {
            "title": "icon",
            "permissions": [
              "SuperAdmin"
            ]
          }
        },
        {
          "path": "routerManagement",
          "name": "RouterManagement",
          "component": "configManagement/routerManagement/index",
          "meta": {
            "title": "routeManagement",
            "permissions": [
              "SuperAdmin"
            ]
          }
        },
        {
          "path": "languageManagement",
          "name": "LanguageManagement",
          "component": "configManagement/languageManagement/index",
          "meta": {
            "title": "languageManagement",
            "permissions": [
              "SuperAdmin"
            ]
          }
        }
      ]
    }
  ]
}
