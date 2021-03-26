# zx-count(作者:初志鑫<1204505056@qq.com>)

## 注意事项

```
只能用于Vue CLI项目

```

## 鸣谢

```
努力了这么久,终于成了一名合格的代码搬运工,我只是有幸站在了巨人的肩膀上,感谢自己,感谢巨人...

```

## 实现功能

```
1.实现了数字自增长
2.实现了数字前后可自定义修饰
3.实现了数字逗号隔断
4.实现了数字小数点位数自定义

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
cnpm i -S zx-count

```

### count 组件 main.js 全局引入

```
import Vue from 'vue'
import ZxCount from 'zx-count'
Vue.component('byui-count', ZxCount)

```

### template 完整示例

```
<template>
	<div id="app"><byui-count :startVal="startVal" :endVal="endVal" :duration="duration" :separator="separator" :prefix="prefix" :suffix="suffix" :decimals="decimals" /></div>
</template>

<script>
export default {
	name: 'app',
	data() {
		return {
			startVal: 0,
			endVal: 111,
			decimals: 2,
			prefix: '$',
			suffix: '美元',
			separator: ',',
			duration: 3000
		};
	}
};
</script>

<style>
body {
	margin: 0;
	padding: 0;
}
#app {
	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
}
span {
	display: block;
	margin-top: 100px;
	color: red;
	line-height: 40px;
	font-size: 60px;
}
</style>

```
