<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="500px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="部门" prop="department">
        <el-input v-model="form.department" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="部门ID" prop="departmentID">
        <el-input v-model="form.departmentID" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="职位" prop="postion">
        <el-input v-model="form.postion" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item v-if="title == '添加'" label="职位ID" prop="postionID">
        <el-input v-model="form.postionID" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item v-else label="职位ID" prop="postionID">
        <el-input
          v-model="form.postionID"
          autocomplete="off"
          disabled
        ></el-input>
      </el-form-item>
      <el-form-item label="权限码" prop="permission">
        <el-input v-model="form.permission" autocomplete="off"></el-input>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">取 消</el-button>
      <el-button type="primary" @click="save">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { doAdd, doEdit } from "@/api/roleManagement";
import { okCode, errorCode } from "@/config/settings";

export default {
  name: "RoleManagementEdit",
  data() {
    return {
      form: {
        id: "",
        department: "",
        departmentID: "",
        postion: "",
        postionID: "",
        permission: "",
      },
      rules: {
        department: [
          { required: true, trigger: "blur", message: "请输入部门" },
        ],
        departmentID: [
          { required: true, trigger: "blur", message: "请输入部门ID" },
        ],
        postion: [{ required: true, trigger: "blur", message: "请输入职位" }],
        postionID: [
          { required: true, trigger: "blur", message: "请输入职位ID" },
        ],
        permission: [
          { required: true, trigger: "blur", message: "请输入权限码" },
        ],
      },
      title: "",
      dialogFormVisible: false,
    };
  },
  created() {},
  methods: {
    showEdit(row) {
      if (!row) {
        this.title = "添加";
      } else {
        this.title = "编辑";
        this.form = Object.assign({}, row);
      }
      this.dialogFormVisible = true;
    },
    close() {
      this.$refs["form"].resetFields();
      this.form = this.$options.data().form;
      this.dialogFormVisible = false;
    },
    save() {
      this.$refs["form"].validate((valid) => {
        if (valid) {
          if (this.title === "添加") {
            doAdd(this.form).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(res.msg, "success");
                this.$emit("fetchData");
                this.close();
              } else {
                this.$baseMessage(msg || `权限添加失败！`, "error");
              }
            });
          } else {
            doEdit(this.form).then((res) => {
              const { code, msg, data } = res;
              if (code === okCode) {
                this.$baseMessage(res.msg, "success");
                this.$emit("fetchData");
                this.close();
              } else {
                this.$baseMessage(msg || `权限编辑失败！`, "error");
              }
            });
          }
        } else {
          return false;
        }
      });
    },
  },
};
</script>
