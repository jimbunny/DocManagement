<template>
  <div class="editor-container">
    <el-row>
      <el-col :xs="8" :sm="8" :md="8" :lg="4" :xl="4">
        <!--<el-tree
          :data="data"
          :props="defaultProps"
          node-key="value"
          :default-expanded-keys="['root']"
          @node-click="handleNodeClick"
        ></el-tree>-->
        <el-input v-model="filterText" :placeholder="$t('docs.filterMenu')">
        </el-input>
        <div class="block">
          <el-tree
            ref="tree"
            class="filter-tree"
            :data="data"
            :props="defaultProps"
            node-key="path"
            default-expand-all
            :expand-on-click-node="false"
            :filter-node-method="filterNode"
            @node-click="handleNodeClick"
          >
            // eslint-disable-next-line vue/no-template-shadow
            <span slot-scope="{ node, data }" class="custom-tree-node">
              <!-- <span>{{ generateTitle(data.label) }}</span> -->
              <span v-if="!data.meta">{{ data.path }}</span>
              <span v-else>{{ generateTitle(data.meta.title) }}</span>
            </span>
          </el-tree>
        </div>
      </el-col>
      <el-col :xs="16" :sm="16" :md="16" :lg="20" :xl="20">
        <el-form
          v-if="status"
          ref="form"
          :model="form"
          :rules="rules"
          label-width="80px"
        >
          <el-form-item :label="$t('docs.title')" prop="title">
            <el-input v-model="form.title" maxlength="20"></el-input>
          </el-form-item>
          <!--<el-form-item label="菜单" prop="menu">
            <el-cascader
              v-model="form.menu"
              :options="data"
              :props="{ expandTrigger: 'hover' }"
              @change="handleChange"
            >
            </el-cascader>
          </el-form-item> -->
          <el-form-item :label="$t('docs.language')" prop="language">
            <el-select v-model="form.language">
              <el-option :label="$t('docs.zh')" value="zh"></el-option>
              <el-option :label="$t('docs.thai')" value="thai"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item :label="$t('docs.content')" prop="content">
            <quill-editor
              v-model="form.content"
              :style="{
                height: '600px',
                border: '1px solid ' + borderColor,
              }"
              :options="editorOption"
              @blur="onEditorBlur($event)"
              @change="onEditorChange($event)"
            ></quill-editor>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSee">
              {{ $t("docs.previewEffect") }}
            </el-button>
            <el-button type="primary" @click="handleSave">{{
              $t("docs.save")
            }}</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
    <el-dialog
      :title="$t('docs.previewEffect')"
      :visible.sync="dialogTableVisible"
    >
      <div style="min-height: 60vh;">
        <h1 class="news-title">{{ form.title }}</h1>
        <div class="news-content ql-editor" v-html="form.content"></div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { quillEditor } from "vue-quill-editor";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";
import "quill/dist/quill.bubble.css";
import { getTree } from "@/api/menuManagement";
import { getFile, doAdd as addFile } from "@/api/docManagement";
import { okCode, errorCode } from "@/config/settings";
import { generateTitle } from "@/utils/i18n";
import { getRouterList as getList } from "@/api/router";

export default {
  name: "Editor",
  components: { quillEditor },
  data() {
    return {
      data: [],
      defaultProps: {
        children: "children",
        label: "path",
      },
      list: [],
      listLoading: true,
      elementLoadingText: this.$t("docs.loading"),
      borderColor: "#dcdfe6",
      dialogTableVisible: false,
      path: "",
      status: false,
      form: {
        title: "",
        menu: [],
        language: "",
        content: "",
      },
      filterText: "",
      editorOption: {
        placeholder: "",
        modules: {
          // clipboard: {
          //   matchers: [["img", this.handleCustomMatcher]],
          // },
          toolbar: [
            [{ header: [1, 2, 3, 4, 5, 6, false] }],
            [{ size: ["small", false, "large", "huge"] }],
            ["bold", "italic", "underline", "strike"],
            ["blockquote", "code-block"],
            [{ list: "ordered" }, { list: "bullet" }],
            [{ script: "sub" }, { script: "super" }],
            [{ indent: "-1" }, { indent: "+1" }],
            [{ direction: "rtl" }],
            [{ color: [] }, { background: [] }],
            [{ align: [] }],
            ["clean"],
            ["link", "image", "video"],
          ],
        },
      },
      rules: {
        title: [
          {
            required: true,
            message: this.$t("docs.titleTip"),
            trigger: "blur",
          },
        ],
        menu: [
          {
            required: true,
            message: this.$t("docs.menuTip"),
            trigger: "change",
          },
        ],
        language: [
          {
            required: true,
            message: this.$t("docs.languageTip"),
            trigger: "change",
          },
        ],
        content: [
          {
            required: true,
            message: this.$t("docs.contentTip"),
            trigger: "blur",
          },
        ],
      },
    };
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    },
    "form.language"(language) {
      getFile({ language: language, menu: this.path.replace("/", "") }).then(
        (res) => {
          const { code, msg, data } = res;
          if (code === okCode) {
            this.form = data;
            // this.$baseMessage("get doc successful!", "success");
          } else {
            this.$baseMessage(this.$t("docs.getDocFailed"), "error");
          }
        }
      );
      // console.log(this.checkName(this.data, val, false));
    },
  },
  async created() {
    const res = await getList({ permission: "admin" });
    const { code, msg, data } = res;
    if (code === okCode) {
      this.data = data;
    } else {
      this.$baseMessage(this.$t("docs.getMenuFailed"), "error");
    }
    // const roleData = await getTree();
    // this.data = roleData.data;
    // this.fetchData();
  },
  methods: {
    handleCustomMatcher(node, Delta) {
      // let ops = []
      // Delta.ops.forEach(op => {
      //   if (op.insert && typeof op.alt === 'string') {
      //     ops.push({insert:op.insert})
      //   }
      // })
      // Delta.ops = ops
      // console.log(Delta.ops)
      return Delta;
    },
    generateTitle,
    async fetchData() {
      this.listLoading = true;
      const { data } = await getTree();
      this.list = data;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    handleNodeClick(data) {
      if (!data.alwaysShow) {
        this.status = true;
      } else {
        this.status = false;
      }
      const language = "zh";
      this.path = data.path.replace("/", "");
      getFile({ language: language, menu: this.path }).then((res) => {
        const { code, msg, data } = res;
        if (code === okCode) {
          this.form = data;
          // this.$baseMessage("get doc successful!", "success");
        } else {
          this.$baseMessage(this.$t("docs.getDocFailed"), "error");
        }
      });
    },
    onEditorBlur(quill) {
      // 失去焦点事件

      this.$refs.form.validateField("content", (errorMsg) => {
        this.borderColor = "#dcdfe6";
        if (errorMsg) {
          this.borderColor = "#F56C6C";
        }
      });
    },
    onEditorChange({ quill, html, text }) {
      // 内容改变事件
      this.form.content = html;
    },
    handleSee() {
      this.$refs["form"].validate((valid) => {
        this.$refs.form.validateField("content", (errorMsg) => {
          this.borderColor = "#dcdfe6";
          if (errorMsg) {
            this.borderColor = "#F56C6C";
          }
        });
        if (valid) {
          this.dialogTableVisible = true;
        } else {
          return false;
        }
      });
    },
    handleSave() {
      this.$refs["form"].validate((valid) => {
        this.$refs.form.validateField("content", (errorMsg) => {
          this.borderColor = "#dcdfe6";
          if (errorMsg) {
            this.borderColor = "#F56C6C";
          }
        });
        if (valid) {
          addFile(this.form).then((res) => {
            const { code, msg, data } = res;
            if (code === okCode) {
              this.$baseMessage(this.$t("docs.saveDocSuccessful"), "success");
            } else {
              this.$baseMessage(this.$t("docs.saveDocFailed"), "error");
            }
          });
        } else {
          return false;
        }
      });
    },
    handleChange(value) {
      console.log(value);
    },
    append(data) {
      const newChild = { value: "testtest", label: "testtest", children: [] };
      if (!data.children) {
        this.$set(data, "children", []);
      }
      data.children.push(newChild);
    },

    remove(node, data) {
      const parent = node.parent;
      const children = parent.data.children || parent.data;
      const index = children.findIndex((d) => d.id === data.id);
      children.splice(index, 1);
    },

    filterNode(value, data) {
      // if (!value) return true;
      // return data.label.indexOf(value) !== -1;
      if (!value) return true;
      if (data.meta) {
        return this.generateTitle(data.meta.title).indexOf(value) !== -1;
      } else {
        return true;
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.news {
  &-title {
    text-align: center;
  }

  &-content {
    ::v-deep {
      p {
        line-height: 30px;

        img {
          display: block;
          margin-right: auto;
          margin-left: auto;
        }
      }
    }
  }
}
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
</style>
