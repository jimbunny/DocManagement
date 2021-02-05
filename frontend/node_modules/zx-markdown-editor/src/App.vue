<template>
  <div id="app">
    <byui-markdown-editor
      ref="mde"
      v-model="value"
      @show-html="handleShowHtml"
    ></byui-markdown-editor>
    <button @click="handleAddText">增加文本</button>&nbsp;&nbsp;&nbsp;
    <button @click="handleAddImg">增加图片</button>&nbsp;&nbsp;&nbsp;
    <a
      target="_blank"
      href="https://chu1204505056.gitee.io/vue-admin-beautiful/#/byui/markdownEditor"
      ><button>
        在线演示地址点击这里
      </button></a
    >
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
