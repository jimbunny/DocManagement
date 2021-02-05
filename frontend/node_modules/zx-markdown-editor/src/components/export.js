import ZxMarkdownEditor from "./index";
export default ZxMarkdownEditor;
if (typeof window !== "undefined" && window.Vue) {
  window.Vue.component("zx-markdown-editor", ZxMarkdownEditor);
}
