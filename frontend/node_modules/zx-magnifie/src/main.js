import Vue from 'vue'
import App from './App.vue'
import zxMagnifie from '../components/export.js'
Vue.component('byui-magnifie', zxMagnifie)
Vue.config.productionTip = false
new Vue({
	render: h => h(App),
}).$mount('#app')
