<template>
  <div class="editor-container" style="background-color:#f6f8f9;">
    <div style="min-height: 60vh;background-color:#ffffff;width: calc(70%);margin: -15px auto;padding: 15px;">
      <h1 class="news-title" style="margin-left: 10%; margin-right: 10%; text-align: center;">{{ form.title }}</h1>
      <div
        class="news-content ql-editor"
        style="margin-left: 10%; margin-right: 10%;"
        v-html="form.content"
      ></div>
    </div>
  </div>
</template>
<script>
import { getFile } from "@/api/docManagement";
import { okCode, errorCode } from "@/config/settings";
import Cookies from "js-cookie";
export default {
  name: "ShowDoc",
  data() {
    return {
      dialogTableVisible: true,
      form: {
        title: "",
        menu: [],
        language: "",
        content: "",
      },
    };
  },
  created() {
    const { meta } = this.$route;
    const title = meta.title;
    this.getDoc(title);
  },
  methods: {
    getDoc(menu) {
      const language = Cookies.get("language") || "zh";
      getFile({ language: language, menu: menu }).then((res) => {
        const { code, msg, data } = res;
        if (code === okCode) {
          this.form = data;
          // this.$baseMessage("get doc successful!", "success");
        } else {
          this.$baseMessage(msg || `get doc failed！`, "error");
        }
      });
    },
  },
};
</script>
<style lang="scss">
.app-main-container {
    width: calc(100% - 300px);
    min-height: calc(100vh - 127px);
    margin: 15px auto;
    background: #fff;
    border-radius: 2px;
    box-shadow: 0 0px 0px rgb(0 21 41 / 8%) !important;
}
</style>