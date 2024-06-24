# 测试创建消息存储
def test_create_msg_store(client):
    # 定义测试数据
    data = {
        "influencer_id": 1,
        "msg_list": [{"msg": "msg1"}, {"msg": "msg2"}],
        "msg_updated_at": "2023-04-24T12:34:56.789Z",
    }

    # 发送POST请求到/msg_stores/
    response = client.post("/msg_stores/", json=data)

    # 检查响应状态码
    assert response.status_code == 200

    # 检查响应体是否包含创建的消息存储数据
    res = response.json()
    assert res["influencer_id"] == data["influencer_id"]


# 测试更新消息存储
def test_update_msg_store(client):
    # 定义更新的消息存储数据
    updated_data = {
        "influencer_id": 2,
        "msg_list": [{"msg": "msg3"}, {"msg": "msg4"}],
        "msg_updated_at": "2023-04-24T12:34:56.789Z",
    }

    # 发送PUT请求到/msg_stores/{msg_store_id}
    response = client.put("/msg_stores/1", json=updated_data)

    # 检查响应状态码
    assert response.status_code == 200

    # 检查响应体是否包含更新的消息存储数据
    res = response.json()
    assert res["influencer_id"] == updated_data["influencer_id"]
    assert res["msg_list"] == updated_data["msg_list"]


# 测试更新消息列表
def test_update_msg_list(client):
    # 定义更新的消息列表
    updated_msgs = [{"msg": "msg3"}, {"msg": "msg4"}]

    # 发送PATCH请求到/msg_stores/{msg_store_id}
    response = client.patch("/msg_stores/1", json={"msgs": updated_msgs})

    # 检查响应状态码
    assert response.status_code == 200

    # 检查响应体是否包含更新的消息列表
    res = response.json()
    assert res["msg_list"] == updated_msgs


# 测试处理消息存储
def test_process_msg_store(client):
    # 定义处理的消息存储ID
    msg_store_id = 1

    # 发送PATCH请求到/msg_stores/process/{msg_store_id}
    response = client.patch(f"/msg_stores/process/{msg_store_id}", json={})

    # 检查响应状态码
    assert response.status_code == 200

    # 检查响应体是否包含处理后的消息存储数据
    res = response.json()
    assert res["msg_list"] == [
        {"msg": "msg1", "processed": True},
        {"msg": "msg2", "processed": True},
    ]


# 测试添加消息
def test_add_msg(client):
    # 定义添加的消息列表
    added_msgs = [{"msg": "msg5"}, {"msg": "msg6"}]

    # 发送PATCH请求到/msg_stores/{msg_store_id}
    response = client.patch("/msg_stores/1", json={"msgs": added_msgs})

    # 检查响应状态码
    assert response.status_code == 200

    # 检查响应体是否包含添加后的消息列表
    res = response.json()
    assert res["msg_list"] == [
        {"msg": "msg1", "processed": True},
        {"msg": "msg2", "processed": True},
        {"msg": "msg5"},
        {"msg": "msg6"},
    ]
