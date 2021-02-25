import request from "@/utils/request";

export function getList(data) {
  return request({
    url: "/roleManagement/getList",
    method: "get",
    params: data,
  });
}

export function doAdd(data) {
  return request({
    url: "/roleManagement/doAdd",
    method: "post",
    data,
  });
}

export function doEdit(data) {
  return request({
    url: "/roleManagement/doEdit",
    method: "put",
    data,
  });
}

export function doDelete(data) {
  return request({
    url: "/roleManagement/doDelete",
    method: "delete",
    data,
  });
}
