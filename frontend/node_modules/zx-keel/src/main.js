import Vue from "vue";
import App from "./App.vue";
import {Heading, Img, Keel, Text} from "./components/export.js";
import "@/styles/keel-variables.scss";

Vue.component("byui-keel", Keel);
Vue.component("byui-keel-heading", Heading);
Vue.component("byui-keel-img", Img);
Vue.component("byui-keel-text", Text);
Vue.config.productionTip = false;
new Vue({
  render: (h) => h(App),
}).$mount("#app");
