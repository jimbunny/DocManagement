# zx-markdown-editor(作者:初志鑫<1204505056@qq.com>)

这是一款基于 simpleMde 封装的 vue markdown 编辑器，在此基础上丰富了实时预览功能

## 鸣谢

```
努力了这么久,终于成了一名合格的代码搬运工,我只是有幸站在了巨人的肩膀上,感谢自己,感谢巨人...

```

## 实现功能

```
1.markdown编辑器的全部功能
2.支持实时预览
```

### 商务合作与赞赏

```
邮箱  1204505056@qq.com
QQ 1204505056

如果你觉得这个项目帮助到了你，你可以赞赏一下作者:
```

![image](https://raw.githubusercontent.com/chuzhixin/donate/master/donation.png)

## 安装方法

```
cnpm i -S zx-markdown-editor

```

### 组件 main.js 全局引入

```
import Vue from "vue";
import App from "./App.vue";
import ZxMarkdownEditor from "./components/export.js";
Vue.component("byui-markdown-editor", ZxMarkdownEditor);
Vue.config.productionTip = false;
new Vue({
  render: (h) => h(App),
}).$mount("#app");
```

```
<template>
  <div id="app">
    <byui-markdown-editor
      ref="mde"
      v-model="value"
      @show-html="handleShowHtml"
    ></byui-markdown-editor>
    <button @click="handleAddText">增加文本</button>&nbsp;&nbsp;&nbsp;
    <button class="ivu-ml" @click="handleAddImg">增加图片</button>
    <div v-html="html"></div>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      value: "# vue-admin-beautiful",
      html: '<h1 id="vue-admin-beautiful">vue-admin-beautiful</h1>',
    };
  },
  methods: {
    handleAddText() {
      this.$refs.mde.add("\n### 新增加的内容");
    },
    handleAddImg() {
      this.$refs.mde.add(
        "\n![](https://chu1204505056.gitee.io/byui-bookmarks/img/ewm.png)"
      );
    },
    handleShowHtml(html) {
      this.html = html;
    },
  },
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
}
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
button {
  display: inline-block;
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
  background: #ffffff;
  border: 1px solid #dcdfe6;
  border-color: #dcdfe6;
  color: #606266;
  -webkit-appearance: none;
  text-align: center;
  box-sizing: border-box;
  outline: none;
  margin: 0;
  transition: 0.1s;
  font-weight: 500;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  padding: 12px 20px;
  font-size: 14px;
  border-radius: 2px;
}
</style>

```
