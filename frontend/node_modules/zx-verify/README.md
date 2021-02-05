# zx-verify(作者:初志鑫<1204505056@qq.com>)

这是一款 vue 图形验证码插件

## 鸣谢

```
努力了这么久,终于成了一名合格的代码搬运工,我只是有幸站在了巨人的肩膀上,感谢自己,感谢巨人...

```

## 商务合作与赞赏

```
邮箱  1204505056@qq.com
QQ 1204505056

如果你觉得这个项目帮助到了你，你可以赞赏一下作者:
```

![image](https://chu1204505056.gitee.io/byui-bookmarks/img/donation.png)

## 安装方法

```
cnpm i -S zx-verify

```

## verify 组件 main.js 全局引入

```
import Vue from 'vue'
import ZxVerify from 'zx-verify'
Vue.component('byui-verify', ZxVerify)

```

## template 完整示例

```
<template>
  <div id="app">
    <byui-verify
      ref="slideDiv"
      :w="350"
      :slider-text="text"
      :h="175"
      @success="handleSuccess"
      @fail="handleError"
    ></byui-verify>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      text: "向右滑动",
    };
  },
  created() {},
  mounted() {},
  methods: {
    handleSuccess() {
      alert("校验成功");
    },
    handleError() {
      alert("校验失败");
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
  color: #2c3e50;
}
</style>


```
