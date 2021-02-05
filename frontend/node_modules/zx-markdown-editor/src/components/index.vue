<template>
  <div class="simple-mde" :class="classes">
    <textarea ref="mde"></textarea>
  </div>
</template>
<script>
import "font-awesome/css/font-awesome.min.css";
import SimpleMDE from "simplemde";
import "simplemde/dist/simplemde.min.css";
import marked from "marked";
import "github-markdown-css/github-markdown.css";

export default {
  name: "MarkdownEditor",
  props: {
    value: {
      type: String,
      default: "",
    },
    border: {
      type: Boolean,
      default: false,
    },
    config: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      mde: null,
      defaultConfig: {},
    };
  },
  computed: {
    classes() {
      return [
        {
          "i-mde-no-border": !this.border,
        },
      ];
    },
  },
  mounted() {
    this.init();
  },
  beforeDestroy() {
    this.mde = null;
  },
  methods: {
    init() {
      const config = Object.assign({}, this.defaultConfig, this.config);
      this.mde = new SimpleMDE({
        ...config,
        initialValue: this.value,
        element: this.$refs.mde,
        autoDownloadFontAwesome: false,
      });
      this.mde.codemirror.on("change", () => {
        this.$emit("input", this.mde.value());
        this.$emit("on-change", this.mde.value());

        const mdHtml = marked(this.mde.value() || "", {
          renderer: new marked.Renderer(),
          gfm: true,
          tables: true,
          breaks: false,
          pedantic: false,
          sanitize: false,
          smartLists: true,
          smartypants: false,
        });

        this.$emit(
          "show-html",
          '<div class="markdown-body" >' + mdHtml + "</div>"
        );
      });
    },
    add(val) {
      if (this.mde) {
        this.mde.value(this.value + val);
      }
    },
    replace(val) {
      if (this.mde) {
        this.mde.value(val);
      }
    },
  },
};
</script>
