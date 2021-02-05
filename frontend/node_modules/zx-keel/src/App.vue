<template>
  <div id="app">
    <byui-keel v-if="show">
      <byui-keel-heading :img="true" />
      <byui-keel-text :lines="5" />
      <byui-keel-img />
    </byui-keel>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      show: true,
    };
  },
  mounted() {
    /* setTimeout(() => {
              this.show = false;
              alert("加载完成,关闭骨架屏");
            }, 3000);*/
  },
};
</script>

<style lang="scss">
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
  padding: 20px;
  height: 100vh;
}
</style>
