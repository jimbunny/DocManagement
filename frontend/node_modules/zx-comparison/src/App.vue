<template>
	<div id="app">
		<byui-comparison :width="comparison.width" :height="comparison.height" :src1="comparison.src1" :src2="comparison.src2"></byui-comparison>
	</div>
</template>

<script>
export default {
	name: 'App',
	data() {
		return {
			comparison: {
				width: '400px',
				height: 'auto',
				src1: require('@/assets/img/aa.png'),
				src2: require('@/assets/img/bb.png')
			}
		};
	},
	created() {},
	mounted() {},
	methods: {}
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
</style>
