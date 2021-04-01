<template>
  <div class="userManagement-container">
    <el-row>
      <el-col :xs="24" :sm="24" :md="8" :lg="4" :xl="4">
        <el-tree
          :data="data"
          :props="defaultProps"
          node-key="id"
          default-expand-all
          :default-expanded-keys="['root']"
          @node-click="handleNodeClick"
        ></el-tree>
      </el-col>
      <el-col :xs="24" :sm="24" :md="16" :lg="20" :xl="20">
        <byui-query-form>
          <byui-query-form-left-panel :span="12">
            <el-button icon="el-icon-plus" type="primary" @click="handleEdit"
              >{{ $t("user.add") }}
            </el-button>
            <el-button icon="el-icon-delete" type="danger" @click="handleDelete"
              >{{ $t("user.batchDelete") }}
            </el-button>
          </byui-query-form-left-panel>
          <byui-query-form-right-panel :span="12">
            <el-form :inline="true" :model="queryForm" @submit.native.prevent>
              <el-form-item>
                <el-input
                  v-model.trim="queryForm.username"
                  :placeholder="$t('user.usernameTip')"
                  clearable
                />
              </el-form-item>
              <el-form-item>
                <el-button icon="el-icon-search" type="primary" @click="queryData"
                  >{{ $t("user.search") }}
                </el-button>
              </el-form-item>
            </el-form>
          </byui-query-form-right-panel>
        </byui-query-form>

        <el-table
          v-loading="listLoading"
          :data="Postionlist"
          :element-loading-text="elementLoadingText"
          @selection-change="setSelectRows"
        >
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="name" label="岗位名称"></el-table-column>
          <el-table-column prop="department" label="所属部门"></el-table-column>
          <el-table-column prop="level" label="岗位职级"></el-table-column>
          <el-table-column prop="staff" label="岗位成员"></el-table-column>
          <el-table-column
            prop="description"
            label="职责描述"
          ></el-table-column>
          <el-table-column fixed="right" :label="$t('user.action')" width="200">
            <template v-slot="scope">
              <el-button type="text" @click="handleEdit(scope.row)"
                >{{ $t("user.edit") }}
              </el-button>
              <el-button type="text" @click="handleDelete(scope.row)"
                >{{ $t("user.delete") }}
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
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        >
        </el-pagination>
        <edit ref="edit" @fetchData="fetchData"></edit>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getList, doDelete } from "@/api/userManagement";
import Edit from "./components/UserManagementEdit";
import { okCode, errorCode } from "@/config/settings";

export default {
  name: "UserManagement",
  components: { Edit },
  data() {
    return {
      list: null,
      listLoading: true,
      layout: "total, sizes, prev, pager, next, jumper",
      total: 0,
      selectRows: "",
      elementLoadingText: this.$t("user.loading"),
      queryForm: {
        pageNo: 1,
        pageSize: 10,
        username: "",
      },
      data: [
        {
          label: "J&T HQ",
          children: [
            {
              label: "信息科技部门",
              children: [
                {
                  label: "实习生",
                },
                {
                  label: "产品经理",
                },
                {
                  label: "测试员",
                },
                {
                  label: "开发工程师",
                },
              ],
            },
            {
              label: "财务部门",
              children: [
                {
                  label: "数据分析师",
                },
                {
                  label: "财务助理",
                },
                {
                  label: "会计师",
                },
                {
                  label: "财务主管",
                },
              ],
            },
            {
              label: "人事部门",
              children: [
                {
                  label: "行政主管",
                },
                {
                  label: "人事主管",
                },
                {
                  label: "行政助理",
                },
                {
                  label: "行政实习生",
                },
              ],
            },
            {
              label: "品牌部门",
              children: [
                {
                  label: "品牌主管",
                },
                {
                  label: "会计师",
                },
              ],
            },
            {
              label: "业务部门",
              children: [
                {
                  label: "业务主管",
                },
                {
                  label: "业务经理",
                },
                {
                  label: "门店负责人",
                },
                {
                  label: "网点负责人",
                },
              ],
            },
          ],
        },
      ],
      defaultProps: {
        children: "children",
        label: "label",
      },
      Postionlist: [{"name": "实习生", "department": "信息科技部门", "level": "M4", "staff": "5", "description": "实习生"},
      {"name": "产品经理", "department": "信息科技部门", "level": "S4", "staff": "4", "description": "产品经理"},
      {"name": "测试员", "department": "信息科技部门", "level": "M2", "staff": "2", "description": "测试员"},
      {"name": "开发工程师", "department": "信息科技部门", "level": "M3", "staff": "2", "description": "开发工程师"}]
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
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
          this.$t("user.deleteTip1") +
            row.username +
            this.$t("user.deleteTip2"),
          this.$t("header.tips"),
          this.$t("header.confirm"),
          this.$t("header.cancel"),
          () => {
            doDelete({ ids: [row.id] }).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(
                  this.$t("user.deleteUserSuccessful"),
                  "success"
                );
                // this.$baseMessage(res.msg, "success");
                this.fetchData();
              } else {
                this.$baseMessage(this.$t("user.deleteUserFailed"), "error");
              }
            });
          }
        );
      } else {
        if (this.selectRows.length > 0) {
          const ids = [];
          this.selectRows.map((item) => ids.push(item.id));
          this.$baseConfirm(
            this.$t("user.deleteTip3"),
            this.$t("header.tips"),
            this.$t("header.confirm"),
            this.$t("header.cancel"),
            () => {
              doDelete({ ids: ids }).then((res) => {
                const { code, msg, data } = res;
                if (code === okCode) {
                  this.$baseMessage(
                    this.$t("user.deleteUserSuccessful"),
                    "success"
                  );
                  this.fetchData();
                } else {
                  this.$baseMessage(this.$t("user.deleteUserFailed"), "error");
                }
              });
            }
          );
        } else {
          this.$baseMessage(this.$t("user.deleteTip4"), "error");
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
          this.$baseMessage(this.$t("user.getUserFailed"), "error");
        }
      });
    },
  },
};
</script>
