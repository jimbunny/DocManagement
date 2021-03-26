import ZxCount from './count.vue';
export default ZxCount;
if (typeof window !== 'undefined' && window.Vue) {
	window.Vue.component('zx-count', ZxCount);
}
