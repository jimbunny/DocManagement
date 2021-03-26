<template>
  <div class="approval-container">
      <div slot="header" class="clearfix">
        <el-row>
          <el-col :xs="2" :sm="2" :md="4" :lg="4" :xl="4">
            <span>{{ title }}</span>
          </el-col>
          <el-col :xs="20" :sm="20" :md="16" :lg="16" :xl="16">
            <el-steps :active="active" simple finish-status="success">
              <el-step title="基础设置" icon="el-icon-edit"></el-step>
              <el-step title="表单设计" icon="el-icon-document"></el-step>
              <el-step title="流程设计" icon="el-icon-set-up"></el-step>
              <el-step title="高级设置" icon="el-icon-s-tools"></el-step>
            </el-steps>
          </el-col>
          <el-col :xs="2" :sm="2" :md="4" :lg="4" :xl="4">
            <el-button
              style="float: right; padding: 3px 0;"
              type="text"
              @click="publish"
              >发布</el-button
            >
          </el-col>
        </el-row>
      </div>
      <el-divider></el-divider>
      <BasicSetting
        v-show="activeStep === 'basicSetting'"
        ref="basicSetting"
        :conf="mockData.basicSetting"
        tab-name="basicSetting"
        @initiatorChange="onInitiatorChange"
      />

      <DynamicForm
        v-show="activeStep === 'formDesign'"
        ref="formDesign"
        :conf="mockData.formData"
        tab-name="formDesign"
      />

      <Process
        v-show="activeStep === 'processDesign'"
        ref="processDesign"
        :conf="mockData.processData"
        tab-name="processDesign"
        @startNodeChange="onStartChange"
      />

      <AdvancedSetting
        v-show="activeStep === 'advancedSetting'"
        ref="advancedSetting"
        :conf="mockData.advancedSetting"
      />
      <el-button style="float: right;;margin-bottom: 12px;" @click="next">下一步</el-button>
  </div>
</template>
<script>
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
  name: "Home",
  props: {
    title: {
      type: String,
      default: '补卡申请'
    }
  },
  components: {
    Process,
    DynamicForm,
    BasicSetting,
    AdvancedSetting
  },
  data() {
    return {
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
  created() {},
  mounted() {},
  methods: {
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