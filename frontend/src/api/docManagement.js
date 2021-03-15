/* eslint-disable */
import request from "@/utils/request";

export function getFile(data) {
    return request({
        url: "/docManagement/getFile",
        method: "get",
        params: data,
    });
}
export function doAdd(data) {
    return request({
        url: "/docManagement/doAdd",
        method: "post",
        data,
    });
}

export function doEdit(data) {
    return request({
        url: "/docManagement/doEdit",
        method: "put",
        data,
    });
}

export function doDelete(data) {
    return request({
        url: "/docManagement/doDelete",
        method: "delete",
        data,
    });
}