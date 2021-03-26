import Vue from 'vue'
import App from './App.vue'
import ZxCount from './components/export.js'
Vue.component('byui-count', ZxCount)
Vue.config.productionTip = false
new Vue({
	render: h => h(App),
}).$mount('#app')
