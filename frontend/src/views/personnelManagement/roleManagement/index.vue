<template>
  <div class="roleManagement-container">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
        <byui-query-form>
          <byui-query-form-left-panel :span="12">
            <el-button icon="el-icon-plus" type="primary" @click="handleEdit"
              >添加</el-button
            >
            <el-button icon="el-icon-delete" type="danger" @click="handleDelete"
              >批量删除
            </el-button>
          </byui-query-form-left-panel>
          <byui-query-form-right-panel :span="12">
            <el-form :inline="true" :model="queryForm" @submit.native.prevent>
              <el-form-item>
                <el-input
                  v-model.trim="queryForm.postion"
                  placeholder="请输入职位"
                  clearable
                />
              </el-form-item>
              <el-form-item>
                <el-button icon="el-icon-search" type="primary" @click="queryData"
                  >查询
                </el-button>
              </el-form-item>
            </el-form>
          </byui-query-form-right-panel>
        </byui-query-form>
        <el-table
          v-loading="listLoading"
          :data="list"
          :element-loading-text="elementLoadingText"
          highlight-current-row
          @selection-change="setSelectRows"
          @current-change="handleSignleChange"
        >
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="id" label="id"></el-table-column>
          <!--<el-table-column prop="department" label="部门"></el-table-column>
          <el-table-column prop="departmentID" label="部门ID"></el-table-column>
          <el-table-column prop="postion" label="职位"></el-table-column>
          <el-table-column prop="postionID" label="职位ID"></el-table-column> -->
          <el-table-column prop="permission" label="权限码"></el-table-column>
          <el-table-column prop="postionID" label="描述"></el-table-column> 
          <el-table-column fixed="right" label="操作" width="200">
            <template v-slot="scope">
              <el-button type="text" @click="handleEdit(scope.row)"
                >编辑
              </el-button>
              <el-button type="text" @click="handleDelete(scope.row)"
                >删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          background
          :current-page="queryForm.pageNo"
          :page-size="queryForm.pageSize"
          :layout="layout"
          :total="total"
          node-key="name"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        >
        </el-pagination>
      </el-col>
      <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
        <byui-query-form style="margin-top: 5px;">
          <byui-query-form-left-panel :span="12">
            <el-input v-model="filterText" placeholder="输入关键字进行过滤">
            </el-input>
          </byui-query-form-left-panel>
          <byui-query-form-right-panel :span="12">
            <el-button icon="el-icon-edit" type="primary" @click="updatePermissionMenu"
              >更新
            </el-button>
          </byui-query-form-right-panel>
        </byui-query-form>
        <div class="block">
          <el-tree
            ref="tree"
            :data="data"
            show-checkbox
            node-key="name"
            default-expand-all
            :props="defaultProps"
            :filter-node-method="filterNode"
          >
            <span slot-scope="{ node, data }" class="custom-tree-node">
              <template>
                <!--<byui-icon :icon="['fas', data.meta.icon]" /> -->
                <span v-if="!data.meta">{{ data.path }}</span>
                <span v-else>{{ generateTitle(data.meta.title) }}</span>
              </template>
            </span>
          </el-tree>
        </div>
      </el-col>
    </el-row>
    <edit ref="edit" @fetchData="fetchData"></edit>
  </div>
</template>

<script>
import { getList, doDelete } from "@/api/roleManagement";
import Edit from "./components/RoleManagementEdit";
import { okCode, errorCode } from "@/config/settings";
import { getRouterList } from "@/api/router";
import { generateTitle } from "@/utils/i18n";
import { getCheckedMenu, doPermissionEdit } from "@/api/menuManagement";

export default {
  name: "RoleManagement",
  components: { Edit },
  data() {
    return {
      list: null,
      listLoading: true,
      layout: "total, sizes, prev, pager, next, jumper",
      total: 0,
      selectRows: "",
      elementLoadingText: "正在加载...",
      queryForm: {
        pageNo: 1,
        pageSize: 10,
        postion: "",
      },
      data: [],
      filterText: "",
      defaultProps: {
        children: "children",
        label: "path",
      },
      currentRow: null,
    };
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    },
  },
  async created() {
    const res = await getRouterList({ permission: "admin" });
    const { code, msg, data } = res;
    if (code === okCode) {
      this.data = data;
    } else {
      this.$baseMessage(msg || `获取菜单信息失败！`, "error");
    }
    this.fetchData();
  },
  methods: {
    generateTitle,
    updatePermissionMenu() {
      if (this.currentRow == null) {
        this.$baseMessage(`请选择权限码！`, "error");
        return;
      }
      doPermissionEdit({
        permission: this.currentRow.permission,
        names: this.$refs.tree.getCheckedKeys(),
      }).then((res) => {
        if (res.code === okCode) {
          this.$baseMessage(`修改权限菜单信息成功！`, "success");
        } else {
          this.$baseMessage(`修改权限菜单信息失败！`, "error");
        }
      });
    },
    handleSignleChange(val) {
      this.currentRow = val;
      getCheckedMenu({ permission: val.permission }).then((res) => {
        if (res.code === okCode) {
          this.$refs.tree.setCheckedKeys(res.data);
        } else {
          this.$baseMessage(`获取权限菜单信息失败！`, "error");
        }
      });
    },
    setSelectRows(val) {
      this.selectRows = val;
    },
    handleEdit(row) {
      if (row.id) {
        this.$refs["edit"].showEdit(row);
      } else {
        this.$refs["edit"].showEdit();
      }
    },
    handleDelete(row) {
      if (row.id) {
        this.$baseConfirm(
          "你确定要删除当前职位为" + row.postion + "的数据吗",
          null,
          () => {
            doDelete({ ids: [row.id] }).then((res) => {
              this.$baseMessage(res.msg, "success");
              this.fetchData();
            });
          }
        );
      } else {
        if (this.selectRows.length > 0) {
          const ids = [];
          this.selectRows.map((item) => ids.push(item.id));
          // const ids = this.selectRows.map((item) => item.id).join();
          this.$baseConfirm("你确定要删除选中项吗", null, () => {
            doDelete({ ids: ids }).then((res) => {
              this.$baseMessage(res.msg, "success");
              this.fetchData();
            });
          });
        } else {
          this.$baseMessage("未选中任何行", "error");
          return false;
        }
      }
    },
    handleSizeChange(val) {
      this.queryForm.pageSize = val;
      this.fetchData();
    },
    handleCurrentChange(val) {
      this.queryForm.pageNo = val;
      this.fetchData();
    },
    queryData() {
      this.queryForm.pageNo = 1;
      this.fetchData();
    },
    fetchData() {
      this.listLoading = true;
      getList(this.queryForm).then((res) => {
        const { code, msg, data } = res;
        if (code === okCode) {
          this.list = data.items;
          this.total = data.totalCount;
          setTimeout((_) => {
            this.listLoading = false;
          }, 300);
        } else {
          this.$baseMessage(msg || `获取权限信息失败！`, "error");
        }
      });
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
  },
};
</script>
