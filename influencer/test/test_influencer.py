
# 测试添加影响者
def test_add_influencer(client):
    data = {
        "site_id": "example_site_id",
        "influencer_account": "example_influencer_account",
        "param": {"example_param": "value"},
    }
    response = client.post("/influencers", json=data)
    assert response.status_code == 200
    res = response.json()
    assert res["site_id"] == data["site_id"]
    assert res["influencer_account"] == data["influencer_account"]


# 测试更新影响者信息
def test_update_influencer(client):
    influencer_id = 1
    data = {
        "site_id": "updated_site_id",
        "influencer_account": "updated_influencer_account",
        "param": {"updated_param": "value"},
    }
    response = client.patch(f"/influencers/{influencer_id}", json=data)
    assert response.status_code == 200
    res = response.json()
    assert res["site_id"] == data["site_id"]
    assert res["influencer_account"] == data["influencer_account"]
