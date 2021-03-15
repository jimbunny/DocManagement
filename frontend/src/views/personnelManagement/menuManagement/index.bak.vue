<template>
  <div class="menuManagement-container">
    <el-row>
      <el-col :xs="24" :sm="24" :md="8" :lg="4" :xl="4">
        <el-tree
          :data="data"
          :props="defaultProps"
          node-key="id"
          :default-expanded-keys="['root']"
          @node-click="handleNodeClick"
        ></el-tree>
      </el-col>
      <el-col :xs="24" :sm="24" :md="16" :lg="20" :xl="20">
        <byui-query-form>
          <byui-query-form-left-panel :span="12">
            <el-button icon="el-icon-plus" type="primary" @click="handleEdit">
              添加
            </el-button>
          </byui-query-form-left-panel>
        </byui-query-form>
        <el-table
          v-loading="listLoading"
          :data="list"
          :element-loading-text="elementLoadingText"
          row-key="path"
          border
          default-expand-all
          :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
        >
          <el-table-column
            show-overflow-tooltip
            prop="name"
            label="name"
          ></el-table-column>
          <el-table-column
            show-overflow-tooltip
            prop="path"
            label="路径"
          ></el-table-column>
          <el-table-column show-overflow-tooltip label="是否隐藏">
            <template #default="{ row }">
              <span>
                {{ row.hidden ? "是" : "否" }}
              </span>
            </template>
          </el-table-column>
          <el-table-column show-overflow-tooltip label="是否一直显示当前节点">
            <template #default="{ row }">
              <span>
                {{ row.alwaysShow ? "是" : "否" }}
              </span>
            </template>
          </el-table-column>
          <el-table-column
            show-overflow-tooltip
            prop="component"
            label="vue文件路径"
          ></el-table-column>
          <el-table-column
            show-overflow-tooltip
            prop="redirect"
            label="重定向"
          ></el-table-column>
          <el-table-column
            show-overflow-tooltip
            prop="meta.title"
            label="标题"
          ></el-table-column>
          <el-table-column show-overflow-tooltip label="图标">
            <template #default="{ row }">
              <span v-if="row.meta">
                <byui-icon
                  v-if="row.meta.icon"
                  :icon="['fas', row.meta.icon]"
                ></byui-icon>
              </span>
            </template>
          </el-table-column>
          <el-table-column show-overflow-tooltip label="是否固定">
            <template #default="{ row }">
              <span v-if="row.meta">
                {{ row.meta.affix ? "是" : "否" }}
              </span>
            </template>
          </el-table-column>
          <el-table-column show-overflow-tooltip label="是否无缓存">
            <template #default="{ row }">
              <span v-if="row.meta">
                {{ row.meta.noKeepAlive ? "是" : "否" }}
              </span>
            </template>
          </el-table-column>
          <el-table-column show-overflow-tooltip label="badge">
            <template #default="{ row }">
              <span v-if="row.meta">
                {{ row.meta.badge }}
              </span>
            </template>
          </el-table-column>
          <el-table-column show-overflow-tooltip label="操作" width="200">
            <template #default="{ row }">
              <el-button type="text" @click="handleEdit(row)">编辑</el-button>
              <el-button type="text" @click="handleDelete(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>

    <edit ref="edit" @fetch-data="fetchData"></edit>
  </div>
</template>

<script>
import { getRouterList as getList } from "@/api/router";
import { getList as getRoleList } from "@/api/roleManagement";
import { getTree, doDelete } from "@/api/menuManagement";
import Edit from "./components/MenuManagementEdit";
import { okCode, errorCode } from "@/config/settings";

export default {
  name: "MenuManagement",
  components: { Edit },
  data() {
    return {
      data: [],
      defaultProps: {
        children: "children",
        label: "postion",
      },
      list: [],
      listLoading: true,
      elementLoadingText: "正在加载...",
    };
  },
  async created() {
    const res = await getRoleList({
      pageNo: 1,
      pageSize: 10000,
      postion: "",
    });
    const { code, msg, data } = res;
    if (code === okCode) {
      this.data = [
        {
          id: "root",
          postion: "全部角色",
          postionID: "admin",
          department: "admin",
          departmentID: "admin",
          permission: "admin",
          children: data.items,
        },
      ];
    } else {
      this.$baseMessage(msg || `获取菜单权限信息失败！`, "error");
    }
    this.fetchData(data.items[0].permission);
  },
  methods: {
    handleEdit(row) {
      if (row.path) {
        this.$refs["edit"].showEdit(row);
      } else {
        this.$refs["edit"].showEdit();
      }
    },
    handleDelete(row) {
      if (row.id) {
        this.$baseConfirm("你确定要删除当前项吗", null, async () => {
          const { msg } = await doDelete({ ids: row.id });
          this.$baseMessage(msg, "success");
          this.fetchData();
        });
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
        this.$baseMessage(msg || `获取权限菜单信息失败！`, "error");
      }
    },
    handleNodeClick(data) {
      this.fetchData(data.permission);
    },
  },
};
</script>
