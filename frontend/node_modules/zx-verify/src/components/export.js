import ZxVerify from "./index";
export default ZxVerify;
if (typeof window !== "undefined" && window.Vue) {
  window.Vue.component("zx-verify", ZxVerify);
}
