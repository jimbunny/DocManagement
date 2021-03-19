
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

