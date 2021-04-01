<template>
  <el-dialog
    title="查看数据修改申请详情"
    :visible.sync="dialogFormVisible"
    width="70%"
    @close="close"
  >
  <el-row :gutter="20">
      <el-col :xs="4" :sm="4" :md="4" :lg="4" :xl="4">
        <el-timeline>
          <el-timeline-item
            v-for="(activity, index) in activities"
            :key="index"
            :icon="activity.icon"
            :type="activity.type"
            :color="activity.color"
            :size="activity.size"
            :timestamp="activity.timestamp">
            {{activity.content}}
          </el-timeline-item>
        </el-timeline>
      </el-col>
      <div  id="printMe" ref="printContent">
      <el-col :xs="20" :sm="20" :md="20" :lg="20" :xl="20">
        <el-row :gutter="15">
        <el-form ref="elForm" :model="formData" :rules="rules" size="medium" label-width="100px">
          <el-col :span="12">
            <el-form-item label-width="120px" label="申请部门" prop="department">
              <el-input v-model="formData.department" placeholder="财务部门" clearable
                :style="{width: '100%'}" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label-width="120px" label="申请人" prop="person">
              <el-input v-model="formData.person" placeholder="张三" clearable :style="{width: '100%'}" disabled>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label-width="120px" label="申请日期" prop="date">
               <el-date-picker
                v-model="value1"
                type="datetime"
                placeholder="2021-03-22 10:00:11" :style="{width: '100%'}" disabled>
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label-width="120px" label="涉及页面" prop="page">
              <el-input v-model="formData.page" placeholder="基础资料" clearable :style="{width: '100%'}" disabled>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label-width="120px" label="数据调整类型" prop="type">
              <el-select v-model="formData.type" placeholder="数据调整" clearable :style="{width: '100%'}" disabled>
                <el-option v-for="(item, index) in typeOptions" :key="index" :label="item.label"
                  :value="item.value" :disabled="item.disabled"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label-width="120px" label="数据处理原因" prop="reason">
              <el-input v-model="formData.reason" type="textarea" placeholder="业务需要，需要修改部分数据！"
                :autosize="{minRows: 4, maxRows: 4}" :style="{width: '100%'}" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label-width="120px" label="申请要求" prop="apply">
              <el-input v-model="formData.apply" type="textarea" placeholder="紧急"
                :autosize="{minRows: 4, maxRows: 4}" :style="{width: '100%'}" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label-width="120px" label="审批意见" prop="approval">
              <el-input v-model="formData.approval" type="textarea" placeholder="同意 Jerry 2021-03-29 10:00:00"
                :autosize="{minRows: 4, maxRows: 4}" :style="{width: '100%'}" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label-width="120px" label="审批意见" prop="approval">
              <el-input v-model="formData.field112" type="textarea" placeholder="同意 Allen 2021-03-29 10:00:00"
                :autosize="{minRows: 4, maxRows: 4}" :style="{width: '100%'}" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-form>
      </el-row>
      </el-col>
      </div>
  </el-row>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">{{ $t("user.close") }}</el-button>
      <el-button v-print="printObj" type="primary">打印</el-button>
              
      <!--<el-button type="primary" @click="toImg">转图片打印</el-button> -->
    </div>
  </el-dialog>
</template>

<script>
import { isPassword } from "@/utils/validate";
import { doEdit, doAdd } from "@/api/userManagement";
import { okCode, errorCode } from "@/config/settings";
import { getList } from "@/api/roleManagement";
import html2canvas from 'html2canvas'  // 转图片打印需要先安装html2Canvas和print-js
import printJS from 'print-js'

export default {
  inheritAttrs: false,
  components: {},
  props: [],
  name: "UserManagementEdit",
  data() {
    const validateUserName = (rule, value, callback) => {
      if ("" == value) {
        callback(new Error(this.$t("user.usernameEmptyTip")));
      } else {
        callback();
      }
    };
    const validatePassword = (rule, value, callback) => {
      if (!isPassword(value)) {
        callback(new Error(this.$t("user.passowrdLengthTip")));
      } else {
        callback();
      }
    };
    const validateEditPassword = (rule, value, callback) => {
      if (value && !isPassword(value)) {
        callback(new Error(this.$t("user.passowrdLengthTip")));
      } else {
        callback();
      }
    };
    const validateEmail = (rule, value, callback) => {
      if (value === "") {
        callback(new Error(this.$t("user.emailEmpty")));
      } else {
        if (value !== "") {
          var reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
          if (!reg.test(value)) {
            callback(new Error(this.$t("user.emailVerification")));
          }
        }
        callback();
      }
    };
    const validatePermission = (rule, value, callback) => {
      if (value === "") {
        callback(new Error(this.$t("user.permissionTip")));
      } else {
        callback();
      }
    };
    return {
      formData: {
        department: undefined,
        person: undefined,
        date: "13:34:40",
        page: undefined,
        type: undefined,
        reason: undefined,
        apply: undefined,
        approval: undefined,
        field112: undefined,
      },
      rules: {
        department: [{
          required: true,
          message: '请输入申请部门',
          trigger: 'blur'
        }],
        person: [{
          required: true,
          message: '请输入申请人',
          trigger: 'blur'
        }],
        date: [{
          required: true,
          message: '请选择申请日期',
          trigger: 'change'
        }],
        page: [{
          required: true,
          message: '请输入涉及页面',
          trigger: 'blur'
        }],
        type: [{
          required: true,
          message: '请选择数据调整类型',
          trigger: 'change'
        }],
        reason: [{
          required: true,
          message: '请输入数据处理原因',
          trigger: 'blur'
        }],
        apply: [{
          required: true,
          message: '请输入申请要求',
          trigger: 'blur'
        }],
        approval: [],
        field112: [],
      },
      typeOptions: [{
        "label": "数据调整",
        "value": 1
      }, {
        "label": "数据更改",
        "value": 2
      }, {
        "label": "数据删除",
        "value": 3
      }, {
        "label": "数据导出",
        "value": 4
      }, {
        "label": "数据导入",
        "value": 5
      }, {
        "label": "数据覆盖",
        "value": 6
      }, {
        "label": "权限调整",
        "value": 7
      }],
       activities: [{
          content: 'Refrain 新建申请',
          timestamp: '2018-04-12 20:46',
          size: 'large',
          type: 'primary',
          icon: 'el-icon-more'
        }, {
          content: 'Pony 同意',
          timestamp: '2018-04-03 20:46',
          color: '#0bbd87'
        }, {
          content: 'Allen 同意',
          timestamp: '2018-04-03 20:46',
          color: '#0bbd87'
        },  {
          content: '归档',
          timestamp: '2018-04-03 20:46',
          color: '#0bbd87'
        }],
      form: {
        username: "",
        password: "12345678",
        email: "",
        permission: "",
      },
      addRules: {
        username: [
          { required: true, trigger: "blur", validator: validateUserName },
        ],
        password: [
          { required: true, trigger: "blur", validator: validatePassword },
        ],
        email: [{ required: true, trigger: "blur", validator: validateEmail }],
        permission: [
          {
            required: true,
            trigger: "blur",
            validator: validatePermission,
          },
        ],
      },
      editRules: {
        username: [
          { required: true, trigger: "blur", validator: validateUserName },
        ],
        password: [{ trigger: "blur", validator: validateEditPassword }],
        email: [{ required: true, trigger: "blur", validator: validateEmail }],
        permission: [
          {
            required: true,
            trigger: "blur",
            validator: validatePermission,
          },
        ],
      },
      title: "",
      status: "",
      dialogFormVisible: false,
      list: [],
      img: '',
      checked: true,
      printObj: {
        id: 'printMe',
        popTitle: '打印',
        extraCss: 'https://www.google.com,https://www.google.com',
        extraHead: '<meta http-equiv="Content-Language"content="zh-cn"/>'
      },
      value1: ""
    };
  },
  created() {
    getList({
      pageNo: 1,
      pageSize: 100000,
      description: "",
    }).then((res) => {
      const { code, msg, data } = res;
      if (code === okCode) {
        this.list = data.items;
      } else {
        this.$baseMessage(this.$t("user.getPermissionFailed"), "error");
      }
    });
  },
  methods: {
    toImg() { // 转图片打印
      html2canvas(this.$refs.printContent, {
        backgroundColor: null,
        useCORS: true,
        windowHeight: document.body.scrollHeight
      }).then((canvas) => {
        // let url = canvas.toDataURL('image/jpeg', 1.0)
        console.log(canvas);
        const url = canvas.toDataURL()
        this.img = url
        printJS({
          printable: url,
          type: 'image',
          documentTitle: '打印图片'
        })
        console.log(url)
      })
    },
    onOpen() {},
    onClose() {
      this.$refs['elForm'].resetFields()
    },
    // close() {
    //   this.$emit('update:visible', false)
    // },
    handelConfirm() {
      this.$refs['elForm'].validate(valid => {
        if (!valid) return
        this.close()
      })
    },
    showEdit(row) {
      if (!row) {
        this.title = this.$t("user.add");
        this.status = "add";
      } else {
        this.title = this.$t("user.edit");
        this.status = "edit";
        this.form = Object.assign({}, row);
      }
      this.dialogFormVisible = true;
    },
    close() {
      // this.$refs["form"].resetFields();
      this.dialogFormVisible = false;
    },
    save() {
      this.$refs["form"].validate((valid) => {
        if (valid) {
          // if (this.title === "添加") {
          if (this.status === "add") {
            doAdd(this.form).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(this.$t("user.addUserSuccessful"), "success");
                this.$emit("fetchData");
                this.close();
              } else {
                this.$baseMessage(this.$t("user.addUserFailed"), "error");
              }
            });
          } else {
            doEdit(this.form).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(
                  this.$t("user.editUserSuccessful"),
                  "success"
                );
                this.$emit("fetchData");
                this.close();
              } else {
                this.$baseMessage(this.$t("user.editUserFailed"), "error");
              }
            });
          }
        } else {
          return false;
        }
      });
    },
  },
};
</script>
