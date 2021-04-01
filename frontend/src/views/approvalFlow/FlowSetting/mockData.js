export default {
    "basicSetting": {
        "flowName": "数据修改申请",
        "flowImg": 0,
        "flowGroup": 2,
        "flowRemark": "数据处理",
        "initiator": {
            "dep&user": [{
                "nodeId": 3,
                "deptId": 3,
                "deptName": "xxx行政部",
                "parentDeptId": 1
            }]
        }
    },
    "processData": {
        "type": "start",
        "content": "所有人",
        "properties": {
            "title": "发起人",
            "initiator": "ALL",
            "formOperates": [{
                    "formId": 1,
                    "formOperate": 1
                },
                {
                    "formId": 2,
                    "formOperate": 2
                },
                {
                    "formId": 3,
                    "formOperate": 2
                },
                {
                    "formId": 4,
                    "formOperate": 2
                },
                {
                    "formId": 5,
                    "formOperate": 2
                },
                {
                    "formId": 6,
                    "formOperate": 2
                },
                {
                    "formId": 7,
                    "formOperate": 2
                }
            ]
        },
        "nodeId": "Gb2",
        "childNode": {
            "type": "approver",
            "content": "张三",
            "properties": {
                "title": "审批人",
                "approvers": [{
                    "nodeId": 20,
                    "userId": 20,
                    "userName": "张三",
                    "deptId": 1
                }],
                "assigneeType": "user",
                "formOperates": [{
                        "formId": 2,
                        "formOperate": 1
                    },
                    {
                        "formId": 3,
                        "formOperate": 1
                    },
                    {
                        "formId": 4,
                        "formOperate": 1
                    },
                    {
                        "formId": 5,
                        "formOperate": 1
                    },
                    {
                        "formId": 6,
                        "formOperate": 1
                    },
                    {
                        "formId": 7,
                        "formOperate": 1
                    },
                    {
                        "formId": 8,
                        "formOperate": 1
                    },
                    {
                        "formId": 9,
                        "formOperate": 1
                    }
                ],
                "counterSign": true,
                "optionalMultiUser": false,
                "optionalRange": "ALL"
            },
            "nodeId": "Wb2",
            "prevId": "Gb2",
            "childNode": {
                "type": "copy",
                "content": "xxx研发部",
                "properties": {
                    "title": "抄送人",
                    "menbers": {
                        "dep": [{
                            "nodeId": 4,
                            "deptId": 4,
                            "deptName": "xxx研发部",
                            "parentDeptId": 1
                        }]
                    },
                    "userOptional": true
                },
                "nodeId": "Yb2",
                "prevId": "Wb2",
                "childNode": {
                    "type": "approver",
                    "content": "李四",
                    "properties": {
                        "title": "审批人",
                        "assigneeType": "user",
                        "formOperates": [{
                                "formId": 1,
                                "formOperate": 1
                            },
                            {
                                "formId": 2,
                                "formOperate": 1
                            },
                            {
                                "formId": 3,
                                "formOperate": 1
                            },
                            {
                                "formId": 4,
                                "formOperate": 1
                            },
                            {
                                "formId": 5,
                                "formOperate": 1
                            },
                            {
                                "formId": 6,
                                "formOperate": 1
                            },
                            {
                                "formId": 7,
                                "formOperate": 1
                            }
                        ],
                        "counterSign": true,
                        "optionalMultiUser": false,
                        "optionalRange": "ALL",
                        "approvers": [{
                            "nodeId": 30,
                            "userId": 30,
                            "userName": "李四",
                            "deptId": 1
                        }]
                    },
                    "nodeId": "Nb2",
                    "prevId": "Yb2"
                }
            }
        }
    },
    "formData": {
        "formRef": "elForm",
        "formModel": "formData",
        "size": "medium",
        "labelPosition": "right",
        "labelWidth": 100,
        "formRules": "rules",
        "gutter": 15,
        "disabled": false,
        "span": 12,
        "formBtns": true,
        "fields": [{
                "cmpType": "common",
                "label": "申请部门",
                "tag": "el-input",
                "tagIcon": "input",
                "placeholder": "请输入申请部门",
                "span": 12,
                "labelWidth": 0,
                "style": {
                    "width": "100%"
                },
                "clearable": true,
                "prepend": "",
                "append": "",
                "prefix-icon": "",
                "suffix-icon": "",
                "maxlength": null,
                "show-word-limit": false,
                "readonly": false,
                "disabled": false,
                "required": false,
                "regList": [],
                "changeTag": true,
                "proCondition": false,
                "asSummary": false,
                "formId": 1,
                "renderKey": 1617076559948,
                "layout": "colFormItem",
                "vModel": "field1"
            },
            {
                "cmpType": "common",
                "label": "申请人",
                "tag": "el-input",
                "tagIcon": "input",
                "placeholder": "请输入申请人",
                "span": 12,
                "labelWidth": 0,
                "style": {
                    "width": "100%"
                },
                "clearable": true,
                "prepend": "",
                "append": "",
                "prefix-icon": "",
                "suffix-icon": "",
                "maxlength": null,
                "show-word-limit": false,
                "readonly": false,
                "disabled": false,
                "required": false,
                "regList": [],
                "changeTag": true,
                "proCondition": false,
                "asSummary": false,
                "formId": 2,
                "renderKey": 1617076685371,
                "layout": "colFormItem",
                "vModel": "field2"
            },
            {
                "cmpType": "common",
                "label": "申请日期",
                "tag": "el-time-picker",
                "tagIcon": "time",
                "placeholder": "请选择申请日期",
                "defaultValue": null,
                "span": 12,
                "labelWidth": 0,
                "style": {
                    "width": "100%"
                },
                "disabled": false,
                "clearable": true,
                "required": false,
                "picker-options": {
                    "selectableRange": "00:00:00-23:59:59"
                },
                "format": "HH:mm:ss",
                "value-format": "HH:mm:ss",
                "regList": [],
                "changeTag": true,
                "proCondition": false,
                "asSummary": false,
                "formId": 3,
                "renderKey": 1617076761461,
                "layout": "colFormItem",
                "vModel": "field3"
            },
            {
                "cmpType": "common",
                "label": "涉及页面",
                "tag": "el-input",
                "tagIcon": "input",
                "placeholder": "请输入设计页面",
                "span": 12,
                "labelWidth": 0,
                "style": {
                    "width": "100%"
                },
                "clearable": true,
                "prepend": "",
                "append": "",
                "prefix-icon": "",
                "suffix-icon": "",
                "maxlength": null,
                "show-word-limit": false,
                "readonly": false,
                "disabled": false,
                "required": false,
                "regList": [],
                "changeTag": true,
                "proCondition": false,
                "asSummary": false,
                "formId": 4,
                "renderKey": 1617076842817,
                "layout": "colFormItem",
                "vModel": "field4"
            },
            {
                "cmpType": "common",
                "label": "数据调整类型",
                "tag": "el-select",
                "tagIcon": "select",
                "placeholder": "请选择数据调整类型",
                "style": {
                    "width": "100%"
                },
                "span": 24,
                "labelWidth": 0,
                "clearable": true,
                "disabled": false,
                "required": false,
                "filterable": false,
                "multiple": false,
                "options": [{
                        "label": "数据调整",
                        "value": "数据调整"
                    },
                    {
                        "label": "数据更改",
                        "value": "数据更改"
                    },
                    {
                        "label": "数据删除",
                        "value": "数据删除"
                    },
                    {
                        "label": "数据导出",
                        "value": "数据导出"
                    },
                    {
                        "label": "数据导入",
                        "value": "数据导入"
                    },
                    {
                        "label": "数据覆盖",
                        "value": "数据覆盖"
                    },
                    {
                        "label": "权限调整",
                        "value": "权限调整"
                    }
                ],
                "regList": [],
                "changeTag": true,
                "proCondition": true,
                "formId": 5,
                "renderKey": 1617076897538,
                "layout": "colFormItem",
                "vModel": "field5"
            },
            {
                "cmpType": "common",
                "label": "数据处理原因",
                "tag": "el-input",
                "tagIcon": "textarea",
                "type": "textarea",
                "placeholder": "请输入数据申请原因",
                "span": 24,
                "labelWidth": 0,
                "autosize": {
                    "minRows": 4,
                    "maxRows": 4
                },
                "style": {
                    "width": "100%"
                },
                "maxlength": null,
                "show-word-limit": false,
                "readonly": false,
                "disabled": false,
                "required": false,
                "regList": [],
                "changeTag": true,
                "proCondition": false,
                "asSummary": false,
                "formId": 6,
                "renderKey": 1617077060435,
                "layout": "colFormItem",
                "vModel": "field6"
            },
            {
                "cmpType": "common",
                "label": "申请要求",
                "tag": "el-input",
                "tagIcon": "textarea",
                "type": "textarea",
                "placeholder": "请输入申请要求",
                "span": 24,
                "labelWidth": 0,
                "autosize": {
                    "minRows": 4,
                    "maxRows": 4
                },
                "style": {
                    "width": "100%"
                },
                "maxlength": null,
                "show-word-limit": false,
                "readonly": false,
                "disabled": false,
                "required": false,
                "regList": [],
                "changeTag": true,
                "proCondition": false,
                "asSummary": false,
                "formId": 7,
                "renderKey": 1617077527948,
                "layout": "colFormItem",
                "vModel": "field7"
            }
        ]
    },
    "advancedSetting": {
        "autoRepeat": true,
        "myAuditAutoPass": true,
        "remarkTip": "这里是填写提示",
        "remarkRequired": true,
        "notVisibleForSponsor": true
    }
}