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

export function doEdit(data) {
    return request({
        url: "/menuManagement/doEdit",
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