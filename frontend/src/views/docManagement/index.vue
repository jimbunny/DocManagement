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
        <el-input v-model="filterText" placeholder="输入关键字进行过滤">
        </el-input>
        <div class="block">
          <el-tree
            ref="tree"
            class="filter-tree"
            :data="data"
            :props="defaultProps"
            node-key="value"
            default-expand-all
            :expand-on-click-node="false"
            :filter-node-method="filterNode"
            @node-click="handleNodeClick"
          >
            // eslint-disable-next-line vue/no-template-shadow
            <span slot-scope="{ node, data }" class="custom-tree-node">
              <span>{{ node.label }}</span>
              <span>
                <el-button type="text" size="mini" @click="() => append(data)">
                  Append
                </el-button>
                <el-button
                  type="text"
                  size="mini"
                  @click="() => remove(node, data)"
                >
                  Delete
                </el-button>
              </span>
            </span>
          </el-tree>
        </div>
      </el-col>
      <el-col :xs="16" :sm="16" :md="16" :lg="20" :xl="20">
        <el-form ref="form" :model="form" :rules="rules" label-width="80px">
          <el-form-item label="标题" prop="title">
            <el-input v-model="form.title" maxlength="20"></el-input>
          </el-form-item>
          <el-form-item label="菜单" prop="menu">
            <el-cascader
              v-model="form.menu"
              :options="data"
              :props="{ expandTrigger: 'hover' }"
              @change="handleChange"
            >
            </el-cascader>
          </el-form-item>
          <el-form-item label="语言" prop="language">
            <el-select v-model="form.language">
              <el-option label="中文" value="zh"></el-option>
              <el-option label="泰语" value="thai"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="内容" prop="content">
            <quill-editor
              v-model="form.content"
              :style="{
                height: '400px',
                border: '1px solid ' + borderColor,
              }"
              :options="editorOption"
              @blur="onEditorBlur($event)"
              @change="onEditorChange($event)"
            ></quill-editor>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSee">预览效果 </el-button>
            <el-button type="primary" @click="handleSave">保存</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
    <el-dialog title="预览效果" :visible.sync="dialogTableVisible">
      <div style="min-height: 60vh;">
        <h1 class="news-title">{{ form.title }}</h1>
        <div class="news-content" v-html="form.content"></div>
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

export default {
  name: "Editor",
  components: { quillEditor },
  data() {
    return {
      data: [],
      defaultProps: {
        children: "children",
        label: "value",
      },
      list: [],
      listLoading: true,
      elementLoadingText: "正在加载...",
      borderColor: "#dcdfe6",
      dialogTableVisible: false,
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
            message: "请输入标题",
            trigger: "blur",
          },
        ],
        menu: [
          {
            required: true,
            message: "请选择菜单",
            trigger: "change",
          },
        ],
        language: [
          {
            required: true,
            message: "请选择语言",
            trigger: "change",
          },
        ],
        content: [
          {
            required: true,
            message: "请输入内容",
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
  },
  async created() {
    const roleData = await getTree();
    this.data = roleData.data;
    // this.fetchData();
  },
  methods: {
    async fetchData() {
      this.listLoading = true;
      const { data } = await getTree();
      this.list = data;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    handleNodeClick(data) {
      const language = "zh";
      getFile({ language: language, menu: data.value }).then((res) => {
        const { code, msg, data } = res;
        if (code === okCode) {
          this.form = data;
          this.$baseMessage("get doc successful!", "success");
        } else {
          this.$baseMessage(msg || `get doc failed！`, "error");
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
              this.$baseMessage("add doc successful!", "success");
            } else {
              this.$baseMessage(msg || `add doc failed！`, "error");
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
      if (!value) return true;
      return data.label.indexOf(value) !== -1;
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
