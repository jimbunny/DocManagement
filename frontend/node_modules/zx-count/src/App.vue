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
