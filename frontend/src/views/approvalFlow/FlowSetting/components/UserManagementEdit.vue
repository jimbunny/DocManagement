<template>
  <el-dialog
    title="数据修改流程设计"
    :visible.sync="dialogFormVisible"
    width="80%"
    @close="close"
  >
   <div slot="title" class="header-title">
    <el-tabs v-model="activeName" @tab-click="handleClick">
              <el-tab-pane name="basicSetting">
              <span slot="label"><i class="el-icon-edit"></i> 基础设置</span>
              <BasicSetting
                v-show="activeStep === 'basicSetting'"
                ref="basicSetting"
                :conf="mockData.basicSetting"
                tab-name="basicSetting"
                @initiatorChange="onInitiatorChange"
              />
              </el-tab-pane>
              <el-tab-pane name="formDesign">
              <span slot="label"><i class="el-icon-document"></i> 表单设计</span>
              <DynamicForm
                v-show="activeStep === 'formDesign'"
                ref="formDesign"
                :conf="mockData.formData"
                tab-name="formDesign"
              /></el-tab-pane>
              <el-tab-pane name="processDesign">
              <span slot="label"><i class="el-icon-set-up"></i> 流程设计</span>
              <Process
                v-show="activeStep === 'processDesign'"
                ref="processDesign"
                :conf="mockData.processData"
                tab-name="processDesign"
                @startNodeChange="onStartChange"
              /></el-tab-pane>
              <el-tab-pane name="advancedSetting">
              <span slot="label"><i class="el-icon-s-tools"></i> 高级设置</span>
              <AdvancedSetting
                v-show="activeStep === 'advancedSetting'"
                ref="advancedSetting"
                :conf="mockData.advancedSetting"
              /></el-tab-pane>
            </el-tabs>
            
        </div>
    <div style="margin-top:-10px; margin-bottom:-10px; text-align: right;" >
      <el-button @click="close">{{ $t("user.close") }}</el-button>
      <el-button type="primary"  @click="publish">保存</el-button>
              
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
import Process from "@/components/Process";
import DynamicForm from "@/components/DynamicForm";
import BasicSetting from '@/components/BasicSetting'
import AdvancedSetting from '@/components/AdvancedSetting'
import MockData from './mockData.js'
const beforeUnload = function (e) {
  var confirmationMessage = '离开网站可能会丢失您编辑得内容';
  (e || window.event).returnValue = confirmationMessage;     // Gecko and Trident
  return confirmationMessage;                                // Gecko and WebKit 
}

export default {
  inheritAttrs: false,
  props: {
    title: {
      type: String,
      default: '数据修改申请'
    }
  },
  components: {
    Process,
    DynamicForm,
    BasicSetting,
    AdvancedSetting
  },
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
          content: '待审批',
          timestamp: '已等待51分钟',
          size: 'large'
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
      activeName: 'basicSetting',
      active: 0,
      tabPosition: "top",
      mockData: MockData, // 可选择诸如 $route.param，Ajax获取数据等方式自行注入
      activeStep: "basicSetting", // 激活的步骤面板
      steps: [
        { label: "基础设置", key: "basicSetting" },
        { label: "表单设计", key: "formDesign" },
        { label: "流程设计", key: "processDesign" },
        { label: "高级设置", key: "advancedSetting" }
      ],
      value1: ""
    };
  },
   beforeRouteEnter(to, from, next){
    window.addEventListener('beforeunload', beforeUnload)
    next()
  },
  beforeRouteLeave(to, from, next){
    window.removeEventListener('beforeunload', beforeUnload)
    next()
  },
  computed:{
    translateX () {
      return `translateX(${this.steps.findIndex(t => t.key === this.activeStep) * 100}%)`
    }
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
    handleClick(tab, event) {
      if (this.activeName == "basicSetting") {
        this.activeStep = "basicSetting";
      }
      if (this.activeName == "formDesign") {
        this.activeStep = "formDesign";
      }
      if (this.activeName == "processDesign") {
        this.activeStep = "processDesign";
      }
      if (this.activeName == "advancedSetting") {
        this.activeStep = "advancedSetting";
      }
      },
    next() {
      if (this.active++ > 3) this.active = 0;
      if (this.active == 0) {
        this.activeStep = "basicSetting";
      }
      if (this.active == 1) {
        this.activeStep = "formDesign";
      }
      if (this.active == 2) {
        this.activeStep = "processDesign";
      }
      if (this.active == 3) {
        this.activeStep = "advancedSetting";
      }
    },
    changeSteps(item) {
      this.activeStep = item.key;
    },
    publish() {
      const getCmpData = name => this.$refs[name].getData()
      // basicSetting  formDesign processDesign 返回的是Promise 因为要做校验
      // advancedSetting返回的就是值
      const p1 = getCmpData('basicSetting') 
      const p2 = getCmpData('formDesign')
      const p3 = getCmpData('processDesign')
      Promise.all([p1, p2, p3])
      .then(res => {
        const param = {
          basicSetting: res[0].formData,
          processData: res[2].formData,
          formData: res[1].formData,
          advancedSetting: getCmpData('advancedSetting')
        }
        this.sendToServer(param)
      })
      .catch(err => {
        err.target && (this.activeStep = err.target)
        err.msg && this.$message.warning(err.msg)
      })
    },
    sendToServer(param){
      this.$notify({
        title: '数据已整合完成',
        message: '请在控制台中查看数据输出',
        position: 'bottom-right'
      });
      console.log('配置数据', param)
    },
    exit() {
      this.$confirm('离开此页面您得修改将会丢失, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$message({
            type: 'success',
            message: '模拟返回!'
          });
        }).catch(() => { });
    },
    /**
     * 同步基础设置发起人和流程节点发起人
     */
    onInitiatorChange (val, labels) {
      const processCmp = this.$refs.processDesign
      const startNode = processCmp.data
      startNode.properties.initiator = val['dep&user']
      startNode.content =  labels  || '所有人'
      processCmp.forceUpdate()
    },
    /**
     * 监听 流程节点发起人改变 并同步到基础设置 发起人数据
     */
    onStartChange(node){
      const basicSetting = this.$refs.basicSetting
      basicSetting.formData.initiator = { 'dep&user': node.properties.initiator }
    }
  },
};
</script>
<style lang="scss" scoped>
/** iframe样式 */
#iframeContain {
  width: 100%;
  height: 800px;
}
</style>
<style lang="stylus" scoped>
$header-height = 54px;
.page {
  width: 100vw;
  height: 100vh;
  padding-top: $header-height;
  box-sizing: border-box;

  .page__header {
    width: 100%;
    height: $header-height;
    flex-center()
    justify-content: space-between;
    box-sizing: border-box;
    color: white;
    background: #3296fa;
    font-size: 14px;
    position: fixed;
    top: 0;

    .page-actions {
      height: 100%;
      text-align: center;
      line-height: $header-height;

      > div {
        height: 100%;
        padding-left: 20px;
        padding-right: 20px;
        display: inline-block;
      }

      i {
        font-size: 22px;
        vertical-align: middle;
      }
    }

    .step-tab {
      display: flex;
      justify-content: center;
      height: 100%;
      position: relative;

      >.step {
        width: 140px;
        line-height: $header-height;
        padding-left: 30px;
        padding-right: 30px;
        cursor: pointer;
        position: relative;

        &.ghost-step{
          position: absolute;
          height: $header-height;
          left: 0;
          z-index: -1;
          background: #4483f2;
          transition: transform .5s;

          &::after {
            content: '';
            border-width: 6px 6px 6px;
            border-style: solid;
            border-color: transparent transparent white;
            position: absolute;
            bottom: 0;
            left: 50%;
            margin-left: -6px;
          }
        }

        &.active >.step-index  {
          background: white;
          color: #4483f2;
        }

        >.step-index {
          display: inline-block;
          width: 18px;
          height: 18px;
          border: 1px solid #fff;
          border-radius: 8px;
          line-height: 18px;
          text-align: center;
          box-sizing: border-box;
        }
      }
    }
  }

  .page__content {
    width: 100%;
    height: 100%;
    overflow: hidden;
    box-sizing: border-box;
    background #f5f5f7
  }
}

.publish-btn {
  margin-right: 20px;
  color: #3296fa;
  padding: 7px 20px;
  border-radius: 4px;
  font-size: 14px;
}

.github{
  position fixed
  bottom 10px
  left 20px
}
</style>

<style>
.el-divider--horizontal {
    display: block;
    height: 1px;
    width: 100%;
    margin: 0px 0;
    margin-top: 15px;
}
.el-steps--simple {
    padding: 1px 1%;
    border-radius: 4px;
    background: #f5f7fa;
}
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 100%;
  }
</style>