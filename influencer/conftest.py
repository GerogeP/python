from datetime import datetime
from unittest import mock
from fastapi.testclient import TestClient
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
import pytest
from app.dependencies.databases import get_db
from app.models.models import (
    Influencer as InfluencerModel,
    InfluencerManualTag as InfluencerManualTagModel,
    MsgStore as MsgStoreModel,
    MsgTask as MsgTaskModel,
    Workflow as WorkflowModel,
)
from asgi import app


def override_get_db():
    data = InfluencerModel(
        id=1,
        site_id="example_site_id",
        influencer_account="example_influencer_account",
        param={"example_param": "value"},
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    param = InfluencerManualTagModel(
        influencer_id=1,
        tags=["tag1", "tag2"],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    msg_store = MsgStoreModel(
            influencer_id=1,
            msg_list=[{"msg": "msg1", "processed": False}, {"msg": "msg2", "processed": False}],
            msg_updated_at="2023-04-24T12:34:56.789Z",
            created_at="2023-04-24T12:34:56.789Z",
            updated_at="2023-04-24T12:34:56.789Z",
        )
    msg_task = MsgTaskModel(
            task_type="task_type",
            # affiliate_account="affiliate_account",
            affiliate_id=1,
            influencer_id=1,
            state="state",
            msg_list=["msg1", "msg2"],
            workflow_id=1,
            workflow_event="event",
            created_at="2023-04-24T12:34:56.789Z",
            updated_at="2023-04-24T12:34:56.789Z",
        )
    workflow = WorkflowModel(
            id=1,
            template_id='达人联络工作流',
            state='人工/达人无档期',
            event='达人：无档期',
            # affiliate_account='example_affiliate_account',
            affiliate_id=1,
            influencer_id=1,
            op_id='example_op_id',
            task_id=1,
            workflow_param_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    try:
        yield UnifiedAlchemyMagicMock(
            data=[
                ([mock.call.query(InfluencerModel)], [data]),
                ([mock.call.refresh(InfluencerModel)], [data]),
                ([mock.call.query(InfluencerManualTagModel)], [param]),
                ([mock.call.query(MsgStoreModel)], [msg_store]),
                ([mock.call.query(MsgTaskModel)], [msg_task]),
                ([mock.call.query(WorkflowModel)], [workflow]),
            ]
        )
    finally:
        pass


def mock_check_user():
    return True


@pytest.fixture
def client():
    # 创建一个测试客户端
    app.dependency_overrides[get_db] = override_get_db
    # app.dependency_overrides[check_user] = mock_check_user
    return TestClient(app)
