import request from "@/utils/request";

export function getDeptRoot() {
    return request({
        url: "/approval/getDeptRoot",
        method: "get",
        params: data,
    });
}
export function getPageEmployee(data) {
    return request({
        url: "/approval/getPageEmployee",
        method: "post",
        data,
    });
}

export function getDeptTree(data) {
    return request({
        url: "/approval/getDeptTree",
        method: "put",
        data,
    });
}

export function getUserByDept(data) {
    return request({
        url: "/approval/getUserByDept",
        method: "delete",
        data,
    });
}