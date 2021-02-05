import Vue from "vue";
import App from "./App.vue";
import { Mp4, Flv, Hls, Custom } from "./components/export.js";
Vue.component("byui-player-mp4", Mp4);
Vue.component("byui-player-flv", Flv);
Vue.component("byui-player-hls", Hls);
Vue.component("byui-player-custom", Custom);
Vue.config.productionTip = false;
new Vue({
  render: (h) => h(App),
}).$mount("#app");
