<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="920px"
    @close="close"
  >
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
        >
        </el-switch>
        <!-- <el-radio-group v-model="menu.type">
          <el-radio label="single"></el-radio>
          <el-radio label="multi"></el-radio>
        </el-radio-group> -->
      </el-form-item>
      <el-form-item :label="$t('menu.name')" prop="name">
        <el-input v-model="menu.name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item :label="$t('menu.path')" prop="path">
        <el-input v-model="menu.path" disabled></el-input>
      </el-form-item>
      <el-form-item :label="$t('menu.zh')" prop="zh">
        <el-input v-model="menu.zh" :placeholder="$t('menu.zhTip')"></el-input>
      </el-form-item>
      <el-form-item :label="$t('menu.thai')" prop="thai">
        <el-input
          v-model="menu.thai"
          :placeholder="$t('menu.thaiTip')"
        ></el-input>
      </el-form-item>
      <el-form-item label="icon" prop="icon">
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
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">{{ $t("menu.close") }}</el-button>
      <el-button type="primary" @click="submitForm('ruleForm')"
        >{{ $t("menu.save") }}
      </el-button>
    </div>
  </el-dialog>
</template>

<script>
import { getRouterList as getList } from "@/api/router";
import { updateRouter } from "@/api/router";
import { getList as getRoleList } from "@/api/roleManagement";
import { getTree, doDelete } from "@/api/menuManagement";
import { okCode, errorCode } from "@/config/settings";
import { generateTitle } from "@/utils/i18n";
import { getIconList } from "@/api/icon";
import { getLanguage, getTitle, updateTitle } from "@/api/language";

export default {
  name: "MenuManagementEdit",
  data() {
    var validateName = (rule, value, callback) => {
      if (!value) {
        return callback(new Error(this.$t("menu.nameEmptyTip")));
      }
      if (this.checkName(this.data, value, false)) {
        return callback(new Error(this.$t("menu.nameExitTip")));
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
        // type: "",
        alwaysShow: true,
        permissions: ["superAdmin"],
      },
      rules: {
        // type: [{ required: true, trigger: "blur", message: "请选择类型" }],
        name: [
          {
            validator: validateName,
            required: true,
            trigger: "blur",
          },
        ],
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
      title: this.$t("menu.add"),
      data: [],
      dialogFormVisible: false,
      status: false,
      tmp: {},
    };
  },
  watch: {
    "menu.name"(val) {
      this.menu.path = "/" + val;
      // console.log(this.checkName(this.data, val, false));
    },
  },
  async created() {
    // 获取菜单信息
    const res = await getList();
    const { code, msg, data } = res;
    if (code === okCode) {
      this.data = data;
    } else {
      this.$baseMessage(this.$t("menu.getMenuFailed"), "error");
    }
    //获取权限信息
    this.getPermissionData();
    this.fetchIconData();
  },
  methods: {
    handleCheckChange(data, checked, indeterminate) {
      this.menu.permissions = this.$refs.permissionTree.getCheckedKeys();
    },
    showEdit(menuData, data) {
      this.tmp = data;
      // const newChild = { value: "testtest", label: "testtest", children: [] };
      // if (!data.children) {
      //   this.$set(data, "children", []);
      // }
      // data.children.push(newChild);
      this.title = this.$t("menu.add");
      this.data = menuData;
      this.dialogFormVisible = true;
    },
    close() {
      this.$refs["ruleForm"].resetFields();
      // this.menu = this.$options.data().form;
      this.dialogFormVisible = false;
    },
    initData(orgList, menu) {
      if (orgList.length) {
        for (var i = 0; i < orgList.length; i++) {
          if (orgList[i].path == menu.path) {
            if (orgList[i].children) {
              menu.children = orgList[i].children;
            }
            orgList[i]["name"] = menu.name;
            orgList[i]["path"] = menu.path;
            orgList[i]["alwaysShow"] = menu.alwaysShow;
            if (menu.icon) {
              orgList[i]["meta"]["icon"] = menu.icon;
            }
            if (menu.permissions) {
              orgList[i]["meta"]["permissions"] = menu.permissions;
            }
            orgList[i]["meta"]["title"] = menu.name;
            orgList[i]["meta"]["component"] = "showDoc/index";
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
    checkName(orgList, name, status) {
      if (orgList.length) {
        for (var i = 0; i < orgList.length; i++) {
          if (orgList[i].name == name) {
            status = true;
            break;
          }
          if (orgList[i].children) {
            // 如果有 children 则继续递归遍历
            status = this.checkName(orgList[i].children, name, status);
          }
        }
      }
      return status;
    },
    async submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.tmp == "root") {
            if (!this.menu.alwaysShow) {
              const addData = {
                path: this.menu.path + "_menu",
                component: "Layout",
                redirect: "noRedirect",
                alwaysShow: false,
                name: this.menu.name,
                children: [
                  {
                    path: this.menu.path,
                    name: this.menu.name,
                    alwaysShow: false,
                    component: "showDoc/index",
                    meta: {
                      title: this.menu.name,
                      permissions: this.menu.permissions,
                      icon: this.menu.icon,
                    },
                  },
                ],
              };
              this.data.push(addData);
            } else {
              const addData = {
                path: this.menu.path + "_menu",
                component: "Layout",
                redirect: "noRedirect",
                alwaysShow: true,
                name: this.menu.name,
                meta: {
                  title: this.menu.name,
                  permissions: this.menu.permissions,
                  icon: this.menu.icon,
                },
              };
              this.data.push(addData);
            }
          } else {
            if (!this.menu.alwaysShow) {
              const newChild = {
                path: this.menu.path,
                name: this.menu.name,
                alwaysShow: false,
                component: "showDoc/index",
                meta: {
                  title: this.menu.name,
                  permissions: this.menu.permissions,
                  icon: this.menu.icon,
                },
              };
              if (!this.tmp.children) {
                this.$set(this.tmp, "children", []);
              }
              this.tmp.children.push(newChild);
            } else {
              const newChild = {
                path: this.menu.path,
                name: this.menu.name,
                alwaysShow: true,
                component: "showDoc/index",
                meta: {
                  title: this.menu.name,
                  permissions: this.menu.permissions,
                  icon: this.menu.icon,
                },
              };
              if (!this.tmp.children) {
                this.$set(this.tmp, "children", []);
              }
              this.tmp.children.push(newChild);
            }
          }
          // this.data = this.initData(this.data, this.menu);
          updateRouter({ router: this.data }).then((res) => {
            if (res.code === okCode) {
              this.data = res.data;
            } else {
              this.$baseMessage(this.$t("menu.addMenuFailed"), "error");
            }
          });
          updateTitle({
            language: "thai",
            name: this.menu.name,
            title: this.menu.thai,
            type: "create",
          }).then((res) => {
            if (res.code === okCode) {
            } else {
              this.$baseMessage(
                this.$t("menu.addMenuTitleThaiFailed"),
                "error"
              );
            }
          });
          updateTitle({
            language: "zh",
            name: this.menu.name,
            title: this.menu.zh,
            type: "create",
          }).then((res) => {
            if (res.code === okCode) {
            } else {
              this.$baseMessage(this.$t("menu.addMenuTitleZhFailed"), "error");
            }
          });
          this.$baseMessage(this.$t("menu.addMenuSuccessful"), "success");
          setTimeout(() => {
            this.$router.go(0);
          }, 1000);
        } else {
          console.log("error submit!!");
          return false;
        }
      });
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
        this.$baseMessage(this.$t("menu.getMenuPermissionFailed"), "error");
      }
    },
    async handleNodeClick(data) {
      this.menu.name = data.name;
      this.menu.path = data.path;
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
