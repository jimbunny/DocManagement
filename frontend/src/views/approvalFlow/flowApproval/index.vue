<template>
  <div class="data-update-approval-container">
    <el-row :gutter="20" type="flex" justify="center" align="middle">
      <el-col :xs="4" :sm="4" :md="4" :lg="4" :xl="4">
      <el-tree :data="data" :props="defaultProps" default-expand-all @node-click="handleNodeClick"></el-tree>
      </el-col>
      <el-col :xs="20" :sm="20" :md="20" :lg="16" :xl="16">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>数据修改申请</span>
          </div>
          <el-row :gutter="15">
            <el-form ref="elForm" :model="formData" :rules="rules" size="medium" label-width="100px">
              <el-col :span="12">
                <el-form-item label-width="120px" label="申请部门" prop="department">
                  <el-input v-model="formData.department" placeholder="请输入申请部门" clearable :style="{width: '100%'}">
                  </el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label-width="120px" label="申请人" prop="person">
                  <el-input v-model="formData.person" placeholder="请输入申请人" clearable :style="{width: '100%'}">
                  </el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label-width="120px" label="申请日期" prop="date">
                  <el-date-picker
                v-model="value1"
                type="datetime"
                placeholder="2021-03-22 10:00:11" :style="{width: '100%'}">
              </el-date-picker>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label-width="120px" label="涉及页面" prop="page">
                  <el-input v-model="formData.page" placeholder="请输入涉及页面" clearable :style="{width: '100%'}">
                  </el-input>
                </el-form-item>
              </el-col>
              <el-col :span="24">
                <el-form-item label-width="120px" label="数据调整类型" prop="type">
                  <el-select v-model="formData.type" placeholder="请选择数据调整类型" clearable :style="{width: '100%'}">
                    <el-option v-for="(item, index) in typeOptions" :key="index" :label="item.label"
                      :value="item.value" :disabled="item.disabled"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="24">
                <el-form-item label-width="120px" label="数据处理原因" prop="reason">
                  <el-input v-model="formData.reason" type="textarea" placeholder="请输入数据处理原因"
                    :autosize="{minRows: 4, maxRows: 4}" :style="{width: '100%'}"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="24">
                <el-form-item label-width="120px" label="申请要求" prop="apply">
                  <el-input v-model="formData.apply" type="textarea" placeholder="请输入申请要求"
                    :autosize="{minRows: 4, maxRows: 4}" :style="{width: '100%'}"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="24">
                <el-form-item size="large">
                  <el-button type="primary" @click="submitForm">提交</el-button>
                  <el-button @click="resetForm">重置</el-button>
                </el-form-item>
              </el-col>
            </el-form>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
export default {
  components: {},
  props: [],
  data() {
    return {
      data: [{
          label: '数据申请',
          children: [{
            label: '数据修改'
          },{
            label: '权限调整'
          },{
            label: '数据移除'
          }]
        }, {
          label: '人事申请',
          children: [{
            label: '入职申请'
          }, {
            label: '转正申请'
          }, {
            label: '离职申请'
          }]
        }, {
          label: '行政申请',
          children: [{
            label: '采购申请'
          }, {
            label: '用车申请'
          }, {
            label: '资产领用'
          }, {
            label: '资产维护'
          }, {
            label: '资产入库'
          }]
        }],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
      formData: {
        department: undefined,
        person: undefined,
        date: "13:34:40",
        page: undefined,
        type: undefined,
        reason: undefined,
        apply: undefined,
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
      value1: ""
    }
  },
  computed: {},
  watch: {},
  created() {},
  mounted() {},
  methods: {
    handleNodeClick(data) {
        console.log(data);
      },
    submitForm() {
      this.$refs['elForm'].validate(valid => {
        if (!valid) return
        // TODO 提交表单
      })
    },
    resetForm() {
      this.$refs['elForm'].resetFields()
    },
  }
}

</script>
<style>
</style>
