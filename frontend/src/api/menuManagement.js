/* eslint-disable */
import request from "@/utils/request";

export function getTree(data) {
    return request({
        url: "/menuManagement/getTree",
        method: "get",
        params: data,
    });
}
export function doAdd(data) {
    return request({
        url: "/menuManagement/doAdd",
        method: "post",
        data,
    });
}

export function doPermissionEdit(data) {
    return request({
        url: "/menuManagement/doPermissionEdit",
        method: "put",
        data,
    });
}

export function doDelete(data) {
    return request({
        url: "/menuManagement/doDelete",
        method: "delete",
        data,
    });
}

export function getCheckedMenu(data) {
    return request({
        url: "/menuManagement/getCheckedMenu",
        method: "get",
        params: data,
    });
}