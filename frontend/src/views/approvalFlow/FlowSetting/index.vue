<template>
  <div class="userManagement-container">
    <el-row :gutter="20">
      <el-col :xs="4" :sm="4" :md="4" :lg="4" :xl="4">
      <el-tree :data="data" :props="defaultProps" default-expand-all @node-click="handleNodeClick"></el-tree>
      </el-col>
      <el-col :xs="20" :sm="20" :md="20" :lg="20" :xl="20">
    <byui-query-form>
      <byui-query-form-left-panel :span="12">
        <el-button type="primary" icon="el-icon-plus" @click="handleEdit({'id': '1'})"
          >新增流程
        </el-button>
      </byui-query-form-left-panel>
      <byui-query-form-right-panel :span="12">
        <el-form :inline="true">
          <el-form-item>
            <el-input
              placeholder="流程名称"
              clearable
            />
          </el-form-item>
          <el-form-item>
            <el-button icon="el-icon-search" type="primary"
              >{{ $t("user.search") }}
            </el-button>
          </el-form-item>
        </el-form>
      </byui-query-form-right-panel>
    </byui-query-form>

    <el-table
      v-loading="listLoading"
      :data="dataList"
      :element-loading-text="elementLoadingText"
      @selection-change="setSelectRows"
    >
      <el-table-column prop="title" label="流程名称"></el-table-column>
      <el-table-column prop="description" label="流程说明"></el-table-column>
      <el-table-column fixed="right" :label="$t('user.action')" width="300">
        <template v-slot="scope">
        <el-button type="text" @click="handleEdit(scope.row)"
            >设计
          </el-button>
          <el-button type="text" @click='$baseMessage("同意成功！","success")' style="color:#67c23a;"
            >发布
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
      dataList: [{"number": "QJ12313131241", "title": "JTS数据修改", "description": "修改JTS基础资料", "date": "2021-11-22 10:00", "status": "部门主管（李四）"},
      {"number": "QJ12313131241", "title": "JTS数据修改", "description": "修改JTS基础资料", "date": "2021-11-22 10:00", "status": "部门主管（李四）"},
      {"number": "QJ12313131241", "title": "JTS数据修改", "description": "修改JTS基础资料", "date": "2021-11-22 10:00", "status": "部门主管（李四）"},
      {"number": "QJ12313131241", "title": "JTS数据修改", "description": "修改JTS基础资料", "date": "2021-11-22 10:00", "status": "部门主管（李四）"},
      {"number": "QJ12313131241", "title": "JTS数据修改", "description": "修改JTS基础资料", "date": "2021-11-22 10:00", "status": "部门主管（李四）"},
      {"number": "QJ12313131241", "title": "JTS数据修改", "description": "修改JTS基础资料", "date": "2021-11-22 10:00", "status": "部门主管（李四）"}],
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
      data: [{
          label: '数据申请',
          children: [{
            label: '数据修改'
          },{
            label: '权限调整'
          },{
            label: '数据移除'
          }]
        }, {
          label: '人事申请',
          children: [{
            label: '入职申请'
          }, {
            label: '转正申请'
          }, {
            label: '离职申请'
          }]
        }, {
          label: '行政申请',
          children: [{
            label: '采购申请'
          }, {
            label: '用车申请'
          }, {
            label: '资产领用'
          }, {
            label: '资产维护'
          }, {
            label: '资产入库'
          }]
        }],
        defaultProps: {
          children: 'children',
          label: 'label'
        }
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    handleNodeClick(data) {
        console.log(data);
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
