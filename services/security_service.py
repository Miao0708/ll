from typing import List

import requests
from loguru import logger




def get_ids(taskId,headers,cookies):
    session = requests.session()
    session.headers.update(headers)
    session.cookies.update(cookies)
    url = "https://isec.iflytek.com/sec/project/report/target/findPage/1/1000"
    params = {"page": 1,
              "pageSize": 1000,
              "taskId": str(taskId),
              "threatCategory": "no_permissions_list",
              "prop": None, "order": None, "relation": "and"}
    response = session.post(url, headers=headers, json=params)
    logger.info(response.text)
    res = response.json()
    records = res["data"]["records"]
    ids = []
    for record in records:
        if str(record["riskLevel"]) == "2" or str(record["riskLevel"]) == "1":
            ids.append(record["id"])
    return ids


def change_status(tasks: list[int], status=4) -> dict:
    result = {}
    for taskId in tasks:
        res = {"success": 0, "fail": 0}
        ids = get_ids(taskId)
        for lid in ids:
            url = f"https://isec.iflytek.com/sec/project/report/target/updateVulStatus/{lid}/{status}"
            params = {
                "id": lid,
                "status": status
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                res["success"] += 1
            else:
                res["fail"] += 1
            result[taskId] = res
    return result



