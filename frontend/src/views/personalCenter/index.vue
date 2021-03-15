<template>
  <div class="personalCenter-container">
    <el-tabs :tab-position="tabPosition">
      <el-tab-pane label="个人简介">
       
      </el-tab-pane>
      <!-- <el-tab-pane label="基本设置">基本设置</el-tab-pane>
      <el-tab-pane label="安全设置">安全设置</el-tab-pane>
      <el-tab-pane label="账户绑定">安全设置</el-tab-pane> -->
    </el-tabs>
  </div>
</template>

<script>
export default {
  name: "PersonalCenter",
  data() {
    return {
      form: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        },
      tabPosition: "left",
    };
  },
  created() {},
  methods: {},
};
</script>
