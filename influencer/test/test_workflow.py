# 测试获取工作流列表
def test_get_workflow_list(client):
    # 假设我们有一个工作流模板ID和状态列表
    template_id = "达人联络工作流"
    states = ["state1", "state2"]

    # 发送GET请求到/workflows/
    response = client.get(
        "/workflows/", params={"template_id": template_id, "states": states}
    )
    assert response.status_code == 200
    # 假设我们有一个工作流，其模板ID和状态符合请求参数
    res = response.json()
    assert len(res) == 1
    assert res[0]["template_id"] == template_id


# 测试获取工作流
def test_get_workflow(client):
    workflow_id = 1
    response = client.get(f"/workflows/{workflow_id}")
    assert response.status_code == 200


# 测试更新工作流
def test_update_workflow(client):
    workflow_id = 1
    data = {
        "template_id": "updated_template_id",
        "state": "updated_state",
        "event": "updated_event",
        "affiliate_account": "updated_affiliate_account",
        "influencer_id": 2,
        "op_id": "updated_op_id",
        # "task_id": 2,
        "workflow_param_id": 2,
    }
    response = client.put(f"/workflows/{workflow_id}", json=data)
    assert response.status_code == 200
    res = response.json()
    assert res["template_id"] == data["template_id"]
    assert res["state"] == data["state"]
    assert res["event"] == data["event"]


# 测试创建工作流
def test_create_workflow(client):
    data = {
        "template_id": "new_template_id",
        "state": "new_state",
        "event": "new_event",
        "affiliate_account": "new_affiliate_account",
        "influencer_id": 3,
        "op_id": "new_op_id",
        # "task_id": 3,
        "workflow_param_id": None,
        "param": {"new_param": "value"},
    }
    response = client.post("/workflows/", json=data)
    assert response.status_code == 200


# 测试触发工作流事件
def test_fire_workflow_event(client):
    workflow_id = 1
    event = "人工处理"

    # 发送请求到/workflows/{workflow_id}/event/{event}
    response = client.patch(f"/workflows/{workflow_id}/event/{event}")
    assert response.status_code == 200
    res = response.json()
    assert res["state"] == "已人工处理"
    assert res["event"] == "人工处理"
