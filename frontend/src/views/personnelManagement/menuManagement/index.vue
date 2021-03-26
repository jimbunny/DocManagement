<template>
  <div class="menuManagement-container">
    <el-row>
      <el-col :xs="24" :sm="24" :md="8" :lg="6" :xl="6">
        <el-input v-model="filterText" :placeholder="$t('menu.filterText')">
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
              <template>
                <!--<byui-icon :icon="['fas', data.meta.icon]" /> -->
                <span v-if="!data.meta">{{ data.path }}</span>
                <span v-else>{{ generateTitle(data.meta.title) }}</span>
                <span>
                  <el-button
                    v-if="data.alwaysShow"
                    type="text"
                    size="mini"
                    @click="() => append(data)"
                  >
                    {{ $t("menu.add") }}
                  </el-button>
                  <el-button
                    type="text"
                    size="mini"
                    @click="() => remove(node, data)"
                  >
                    {{ $t("menu.delete") }}
                  </el-button>
                </span>
              </template>
            </span>
          </el-tree>
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :md="16" :lg="18" :xl="18">
        <byui-query-form>
          <byui-query-form-left-panel :span="12">
            <el-button icon="el-icon-plus" type="primary" @click="handleEdit">
              {{ $t("menu.add") }}
            </el-button>
          </byui-query-form-left-panel>
        </byui-query-form>
        <el-form
          ref="ruleForm"
          :model="menu"
          status-icon
          :rules="rules"
          label-width="140px"
          class="demo-ruleForm"
        >
          <el-form-item :label="$t('menu.alwaysShow')" prop="alwaysShow">
            <el-switch
              v-model="menu.alwaysShow"
              active-color="#13ce66"
              inactive-color="#ff4949"
              disabled
            >
            </el-switch>
          </el-form-item>
          <el-form-item :label="$t('menu.name')" prop="name">
            <el-input
              v-model="menu.name"
              autocomplete="off"
              disabled
            ></el-input>
          </el-form-item>
          <el-form-item :label="$t('menu.path')" prop="path">
            <el-input v-model="menu.path" disabled></el-input>
          </el-form-item>
          <el-form-item :label="$t('menu.component')" prop="component">
            <el-input v-model="menu.component"></el-input>
          </el-form-item>
          <el-form-item :label="$t('menu.zh')" prop="zh">
            <el-input
              v-model="menu.zh"
              :placeholder="$t('menu.zhTip')"
            ></el-input>
          </el-form-item>
          <el-form-item :label="$t('menu.thai')" prop="thai">
            <el-input
              v-model="menu.thai"
              :placeholder="$t('menu.thaiTip')"
            ></el-input>
          </el-form-item>
          <el-form-item :label="$t('menu.icon')" prop="icon">
            <!-- <el-input v-model="menu.checkPass" type="password" autocomplete="off"></el-input> -->
            <el-autocomplete
              v-model="menu.icon"
              popper-class="my-autocomplete"
              :fetch-suggestions="querySearch"
              :placeholder="$t('menu.iconTip')"
              style="width: 100%;"
              @select="handleSelect"
            >
              <i
                slot="suffix"
                class="el-icon-edit el-input__icon"
                @click="handleIconClick"
              >
              </i>
              <template slot-scope="{ item }">
                <!--      <div class="name">{{ item.value }}</div>
                <span class="addr">{{ item.address }}</span> -->

                <el-card shadow="hover" style="cursor: pointer;">
                  <byui-icon :icon="['fas', item]" />
                </el-card>
                <!--<div class="icon-text">{{ item }}</div>-->
              </template>
            </el-autocomplete>
          </el-form-item>
          <el-form-item :label="$t('menu.permission')" prop="permissions">
            <el-tree
              ref="permissionTree"
              :props="props"
              :data="permissions"
              node-key="permission"
              show-checkbox
              default-expand-all
              @check-change="handleCheckChange"
            >
              <span slot-scope="{ node, data }" class="custom-tree-node">
                <span>{{ node.label }}</span>
              </span>
            </el-tree>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')">{{
              $t("menu.update")
            }}</el-button>
            <el-button @click="resetForm('ruleForm')">{{
              $t("menu.reset")
            }}</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>

    <edit ref="edit" @fetch-data="data"></edit>
  </div>
</template>

<script>
import { getRouterList as getList } from "@/api/router";
import { updateRouter } from "@/api/router";
import { getList as getRoleList } from "@/api/roleManagement";
import { getTree, doDelete } from "@/api/menuManagement";
import Edit from "./components/MenuManagementEdit";
import { okCode, errorCode } from "@/config/settings";
import { generateTitle } from "@/utils/i18n";
import { getIconList } from "@/api/icon";
import {
  getLanguage,
  getTitle,
  updateTitle,
  deleteTitle,
} from "@/api/language";

export default {
  name: "MenuManagement",
  components: { Edit },
  data() {
    var validateName = (rule, value, callback) => {
      if (!value) {
        return callback(new Error(this.$t("menu.nameTip")));
      } else {
        callback();
      }
    };
    var validatePath = (rule, value, callback) => {
      if (!value) {
        return callback(new Error(this.$t("menu.pathTip")));
      } else {
        callback();
      }
    };
    var validateThai = (rule, value, callback) => {
      if (!value) {
        return callback(new Error(this.$t("menu.thaiTip")));
      } else {
        callback();
      }
    };
    var validateZh = (rule, value, callback) => {
      if (!value) {
        return callback(new Error(this.$t("menu.zhTip")));
      } else {
        callback();
      }
    };
    return {
      data: [],
      filterText: "",
      defaultProps: {
        children: "children",
        label: "path",
      },
      props: {
        label: "permission",
        children: "children",
      },
      listLoading: true,
      elementLoadingText: this.$t("menu.loading"),
      menu: {
        name: "",
        path: "",
        icon: "",
        zh: "",
        thai: "",
        alwaysShow: false,
        permissions: [],
        component: "",
      },
      rules: {
        // type: [{ required: true, trigger: "blur", message: "请选择类型" }],
        name: [{ required: true, trigger: "blur", validator: validateName }],
        path: [{ required: true, trigger: "blur", validator: validatePath }],
        thai: [{ required: true, trigger: "blur", validator: validateThai }],
        zh: [{ required: true, trigger: "blur", validator: validateZh }],
        // icon: [{ required: true, trigger: "blur", message: "请选择图标" }],
        // permissions: [
        //   { required: true, trigger: "blur", message: "请选择角色" },
        // ],
      },
      permissions: [],
      queryIcon: [],
      queryForm: {
        pageNo: 1,
        pageSize: 72,
        title: "",
      },
    };
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    },
  },
  async created() {
    // 获取菜单信息
    const res = await getList({ permission: "admin" });
    const { code, msg, data } = res;
    if (code === okCode) {
      this.data = data;
    } else {
      this.$baseMessage(this.$t("menu.getMenuFailed"), "error");
    }
    //获取权限信息
    this.getPermissionData();
    this.fetchIconData();
    // this.getTitleThai();
    // this.getTitleZh();
  },
  methods: {
    generateTitle,
    initData(orgList, menu) {
      if (orgList.length) {
        for (var i = 0; i < orgList.length; i++) {
          if (orgList[i].path == menu.path) {
            if (orgList[i].children) {
              menu.children = orgList[i].children;
            }
            orgList[i]["name"] = menu.name;
            orgList[i]["path"] = menu.path;
            orgList[i]["component"] = menu.component;
            orgList[i]["alwaysShow"] = menu.alwaysShow;
            if (menu.icon) {
              orgList[i]["meta"]["icon"] = menu.icon;
            }
            if (menu.permissions) {
              orgList[i]["meta"]["permissions"] = menu.permissions;
            }
            orgList[i]["meta"]["title"] = menu.name;
            break;
          }
          if (orgList[i].children) {
            // 如果有 children 则继续递归遍历
            this.initData(orgList[i].children, menu);
          }
        }
      }
      return orgList;
    },
    async submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.data = this.initData(this.data, this.menu);
          updateRouter({ router: this.data }).then((res) => {
            if (res.code === okCode) {
              this.data = res.data;
            } else {
              this.$baseMessage(this.$t("menu.editMenuFailed"), "error");
            }
          });
          updateTitle({
            language: "thai",
            name: this.menu.name,
            title: this.menu.thai,
            type: "update",
          }).then((res) => {
            if (res.code === okCode) {
            } else {
              this.$baseMessage(
                this.$t("menu.editThaiMenuTitleFailed"),
                "error"
              );
            }
          });
          updateTitle({
            language: "zh",
            name: this.menu.name,
            title: this.menu.zh,
            type: "update",
          }).then((res) => {
            if (res.code === okCode) {
            } else {
              this.$baseMessage(this.$t("menu.editZhMenuTitleFailed"), "error");
            }
          });
          this.$baseMessage(this.$t("menu.editMenuSuccessful"), "success");
          setTimeout(() => {
            this.$router.go(0);
          }, 1000);
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    resetForm(formName) {
      // this.$refs[formName].resetFields();
      this.menu.zh = "";
      this.menu.thai = "";
      this.menu.icon = "";
      this.menu.permissions = [];
    },
    handleEdit() {
      this.$refs["edit"].showEdit(this.data, "root");
    },
    handleDelete(row) {
      if (row.id) {
        this.$baseConfirm(
          this.$t("menu.deleteTip1"),
          this.$t("header.tips"),
          this.$t("header.confirm"),
          this.$t("header.cancel"),
          async () => {
            const { msg } = await doDelete({ ids: row.id });
            this.$baseMessage(msg, "success");
            this.fetchData();
          }
        );
      }
    },
    async getPermissionData() {
      const res = await getRoleList({
        pageNo: 1,
        pageSize: 10000,
        postion: "",
      });
      const { code, msg, data } = res;
      if (code === okCode) {
        var tmp = [];
        for (var i = 0, len = data.items.length; i < len; i++) {
          if (tmp.indexOf(data.items[i].permission) != -1) {
          } else {
            tmp.push(data.items[i].permission);
          }
        }
        for (var i = 0, len = tmp.length; i < len; i++) {
          this.permissions.push({ permission: tmp[i] });
        }
        // this.permissions = data.items;
      } else {
        this.$baseMessage(this.$t("menu.getMenuPermissionFailed"), "error");
      }
    },
    async fetchData(permission) {
      this.listLoading = true;
      const { code, msg, data } = await getList({ permission: permission });
      if (code === okCode) {
        this.list = data;
        setTimeout(() => {
          this.listLoading = false;
        }, 300);
      } else {
        this.$baseMessage(this.$t("menu.getMenuFailed"), "error");
      }
    },
    async handleNodeClick(data) {
      this.menu.name = data.name;
      this.menu.path = data.path;
      this.menu.alwaysShow = data.alwaysShow;
      this.menu.component = data.component;
      if (data.meta) {
        this.menu.icon = data.meta.icon;
        this.menu.permissions = [];
        getTitle({ language: "thai", title: data.meta.title }).then((res) => {
          if (res.code === okCode) {
            this.menu.thai = res.data.title;
          } else {
            return this.$baseMessage(
              this.$t("menu.getMenuLanguageThaiFailed"),
              "error"
            );
          }
        });
        getTitle({ language: "zh", title: data.meta.title }).then((res) => {
          if (res.code === okCode) {
            this.menu.zh = res.data.title;
          } else {
            return this.$baseMessage(
              this.$t("menu.getMenuLanguageZhFailed"),
              "error"
            );
          }
        });
        // this.menu.thai = this.thai["route"][data.meta.title];
        // this.menu.zh = this.zh["route"][data.meta.title];
        if (data.meta.permissions) {
          this.menu.permissions = data.meta.permissions;
        } else {
          for (var i = 0, len = this.permissions.length; i < len; i++) {
            this.menu.permissions.push(this.permissions[i].permission);
          }
        }
      } else {
        this.menu.icon = "";
        this.menu.permissions = [];
        this.menu.thai = "";
        this.menu.zh = "";
        for (var i = 0, len = this.permissions.length; i < len; i++) {
          this.menu.permissions.push(this.permissions[i].permission);
        }
      }
      this.$refs.permissionTree.setCheckedKeys(this.menu.permissions);
    },
    handleChange(value) {
      console.log(value);
    },
    append(data) {
      this.$refs["edit"].showEdit(this.data, data);
      // const newChild = { value: "testtest", label: "testtest", children: [] };
      // if (!data.children) {
      //   this.$set(data, "children", []);
      // }
      // data.children.push(newChild);
    },

    remove(node, data) {
      if (data) {
        this.$baseConfirm(
          this.$t("menu.deleteTip1"),
          this.$t("header.tips"),
          this.$t("header.confirm"),
          this.$t("header.cancel"),
          async () => {
            const parent = node.parent;
            const children = parent.data.children || parent.data;
            const index = children.findIndex((d) => d.path === data.path);
            children.splice(index, 1);
            updateRouter({ router: this.data }).then((res) => {
              if (res.code === okCode) {
                this.data = res.data;
              } else {
                this.$baseMessage(this.$t("menu.deleteTip2"), "error");
              }
            });
            if (data.name) {
              deleteTitle({
                language: "thai",
                name: data.name,
              }).then((res) => {
                if (res.code === okCode) {
                } else {
                  this.$baseMessage(this.$t("menu.deleteTip3"), "error");
                }
              });
              deleteTitle({
                language: "zh",
                name: data.name,
              }).then((res) => {
                if (res.code === okCode) {
                } else {
                  this.$baseMessage(this.$t("menu.deleteTip4"), "error");
                }
              });
            }
            this.$baseMessage(this.$t("menu.deleteTip5"));
            setTimeout(() => {
              this.$router.go(0);
            }, 1000);
            this.fetchData();
          });
      }
    },

    filterNode(value, data) {
      if (!value) return true;
      if (data.meta) {
        return this.generateTitle(data.meta.title).indexOf(value) !== -1;
      } else {
        return true;
      }
      // generateTitle(data.meta.title)
      // return generateTitle(data.meta).indexOf(value) !== -1;
    },
    querySearch(queryString, cb) {
      var queryIcon = this.queryIcon;
      var results = queryString
        ? queryIcon.filter(this.createFilter(queryString))
        : queryIcon;
      // 调用 callback 返回建议列表的数据
      cb(results);
    },
    createFilter(queryString) {
      return (queryIcon) => {
        return queryIcon.toLowerCase().indexOf(queryString.toLowerCase()) != -1;
      };
    },
    handleSelect(item) {
      this.menu.icon = item;
    },
    handleIconClick(ev) {
      console.log(ev);
    },
    handleSizeChange(val) {
      this.queryForm.pageSize = val;
      this.fetchIconData();
    },
    handleCurrentChange(val) {
      this.queryForm.pageNo = val;
      this.fetchIconData();
    },
    queryData() {
      this.queryForm.pageNo = 1;
      this.fetchIconData();
    },
    fetchIconData() {
      getIconList(this.queryForm).then((res) => {
        const data = res.data.data;
        this.queryIcon = data;
        this.allIcon = data;
        this.total = res.data.totalCount;
      });
    },
    handleCopyIcon(index, event) {
      const copyText = `<byui-icon :icon="['fas', '${this.queryIcon[index]}']"></byui-icon>`;
      this.copyText = copyText;
      clip(copyText, event);
    },
    handleCheckChange(data, checked, indeterminate) {
      this.menu.permissions = this.$refs.permissionTree.getCheckedKeys();
    },
  },
  renderContent(h, { node, data, store }) {
    return (
      <span class="custom-tree-node">
        <span>{node.postion}</span>
      </span>
    );
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
.my-autocomplete {
  li {
    line-height: normal;
    padding: 7px;

    .name {
      text-overflow: ellipsis;
      overflow: hidden;
    }
    .addr {
      font-size: 12px;
    }

    .highlighted .addr {
      color: #ddd;
    }
  }
}
.icon-container {
  ::v-deep {
    .el-card__body {
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center; /* 垂直居中 */
      justify-content: center; /* 水平居中 */

      svg:not(:root).svg-inline--fa {
        font-size: 35px;
        font-weight: bold;
        color: $base-color-gray;
        text-align: center;
        vertical-align: middle;
        pointer-events: none;
        cursor: pointer;
      }
    }
  }

  .icon-text {
    height: 30px;
    margin-top: -15px;
    overflow: hidden;
    font-size: 12px;
    line-height: 30px;
    text-align: center;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
</style>
<style lang="scss">
.el-autocomplete-suggestion li {
    padding: 0 20px;
    margin: 0;
    line-height: 20px;
    width: 90px;
    float: left;
    cursor: pointer;
    color: #606266;
    font-size: 14px;
    list-style: none;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>