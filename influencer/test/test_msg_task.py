
# 测试创建消息发送任务
def test_create_msg_task(client):
    # 定义创建的消息发送任务数据
    data = {
        "task_type": "task_type",
        "affiliate_account": "affiliate_account",
        "influencer_id": 1,
        "state": "state",
        "msg_list": ["msg1", "msg2"],
        "workflow_id": 1,
        "workflow_event": "event",
    }

    # 发送POST请求到/msg_tasks/
    response = client.post("/msg_tasks/", json=data)

    # 检查响应状态码
    assert response.status_code == 200

    res = response.json()
    assert res["task_type"] == data["task_type"]
    assert res["affiliate_account"] == data["affiliate_account"]
    assert res["influencer_id"] == data["influencer_id"]
    assert res["state"] == data["state"]
    assert res["msg_list"] == data["msg_list"]


# 测试获取消息发送任务列表
def test_get_msg_task_list(client):
    # 定义查询参数
    params = {"task_type": "task_type", "state": "state"}

    # 发送GET请求到/msg_tasks/
    response = client.get("/msg_tasks/", params=params)

    # 检查响应状态码
    assert response.status_code == 200

    # 检查响应体是否包含获取的消息发送任务列表数据
    res = response.json()
    assert len(res) == 1
    assert res[0]["task_type"] == "task_type"
    assert res[0]["affiliate_account"] == "affiliate_account"
    assert res[0]["influencer_id"] == 1


# 测试更新消息发送任务状态
def test_update_msg_task_state(client):
    # 定义更新的消息发送任务状态
    updated_state = "sent"

    # 发送PATCH请求到/msg_tasks/{task_id}
    response = client.patch("/msg_tasks/1", json=updated_state)

    # 检查响应状态码
    assert response.status_code == 200

    # 检查响应体是否包含更新的消息发送任务状态数据
    res = response.json()
    assert res["state"] == updated_state
