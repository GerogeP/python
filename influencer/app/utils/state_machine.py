import json
import sys
from transitions import EventData
from transitions import Machine


# sys.path.append('.')
# sys.path.append('..')
# sys.path.append('../..')
# sys.path.append('../../..')

from app.models.models import (
    Workflow as WorkflowModel,
    MsgTask as MsgTaskModel,
    InfluencerManualTag as InfluencerManualTagModel,
    NewMsg as NewMsgModel,
    MsgStore as MsgStoreModel,
    Influencer as InfluencerModel,
)

from app.utils.chat import send_to_influencer
from app.utils.decide_intention import AI_to_determine
# from datetime import datetime
from app.home.schemas.schemas import MsgTaskStates, Msg2Send, MsgTypes
# from sqlalchemy.orm import Session

class SimpleStates(object):

   
    def __init__(self, name):

        self.name = name

    async def save_state(self, event: EventData):
        self.workflow.state = self.state
        self.workflow.event = event.event.name

    async def do_nothing(self):
        pass

   
if __name__ == '__main__':
    
    workflow = SimpleStates('workflow')

    fsm_path="../fsm_templates/"
    template_id = "达人联络工作流"


    with open(f"{fsm_path}{template_id}.json", encoding="utf-8") as f:
        global data 
        data = json.load(f)

    # print(data)
    states, transitions = data.values()
    # print(f'states: {states}')
    # print(f'transitions: {transitions}')

    model = SimpleStates('workflow')
    workflow = Machine(
        states=states, 
        transitions=transitions, 
        initial='已创建'
        )

    print(workflow.states)
    # print(workflow.transitions)
    
    print(workflow.state)

    workflow.trigger('生成触达需求')

    print(workflow.state)
    # asyncio.get_event_loop().run_until_complete(model.start())


