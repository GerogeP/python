from app.models.models import (
    Workflow as WorkflowModel,
    MsgStore as MsgStoreModel,
    Influencer as InfluencerModel
)

from app.utils.chat import send_to_influencer

async def AI_to_determine(workflow: WorkflowModel, msg: MsgStoreModel, influencer: InfluencerModel):
    if not isinstance(workflow.workflow_param_id, int) or workflow.workflow_param_id is None:
        return 8
    materials = """
    Material 1: Product-related information: {product_name}
    Material 2: The commission rate is {commission_rate}%
    """.format(product_name = workflow.work_flow_param.param["product_card"]["product_name"], commission_rate = workflow.work_flow_param.param["product_card"]["commission_rate"])
    dialog = []
    if msg.msg_list[-1]['account_type'] == "affiliate":
        return 9
    for msg in msg.msg_list:
        # print(msg)
        # TODO: 修改逻辑
        if msg['type'] != "text" or msg['processed']:
            continue
        msg['processed'] = True
        text = "<{}>: {}".format("BD" if msg['account_type'] == "affiliate" else msg['account_type'], msg['content'])
        dialog.append(text)
    # attributes.flag_modified(msg, "msg_list")
    message = await send_to_influencer(
        influencer.param["name"],
        influencer.param.get("tags", ""),
        materials,
        "\n".join(dialog),
    )
    # 配置个enum？
    if "Agree to collaborate" in message['intent_category']:
        return 1
    elif "Request higher commission" in message['intent_category']:
        return 2
    elif "Request for samples" in message['intent_category']:
        return 3
    elif "Specification request" in message['intent_category']:
        return 4
    elif "Confirm the specification" in message['intent_category']:
        return 5
    elif "Refuse to collaborate" in message['intent_category']:
        return 6
    elif "Shipment status inquiry" in message['intent_category']:
        return 7
    else:
        return 8