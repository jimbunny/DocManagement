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
