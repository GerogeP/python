# coding:utf-8
"""Msseage Services.
Filename: messages.py
Author: George Pang
Contact: panglilimcse@139.com
"""

import sys
from datetime import datetime
from pandas import DataFrame as df
from sqlalchemy import text, update
from fastapi import Query
sys.path.append('.')
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../..')
print(sys.path)
from app.models.models import MsgTask
from app.home.schemas.schemas import MsgTaskStates 
from app.dependencies.databases import engine, SessionLocal


class MsgTaskService:
    """Operation services of MsgTask."""   

    async def filtered_msg_tasks(affiliate_account: str, influencer_id: str, state: MsgTaskStates):
        """select message tasks according to affiliate_account, influencer_id and sta."""

        stmt = '''SELECT
            msg_tasks.id,
            msg_tasks.task_type,
            msg_tasks.affiliate_account,
            msg_tasks.influencer_id,
            msg_tasks.state,
            msg_tasks.deleted_at
          FROM msg_tasks
          WHERE
            msg_tasks.affiliate_account = :affiliate_account AND
            msg_tasks.influencer_id = :influencer_id AND 
            msg_tasks.state = :state
        '''
        '''
         msg_tasks.affiliate_account = :affiliate_account AND
         msg_tasks.influencer_id = :influencer_id AND
         msg_tasks.state = :state
    '''
    
        result = SessionLocal().execute(
                text(stmt),
                {'affiliate_account': affiliate_account,
                 'influencer_id': influencer_id,
                 'state': state}
                )
    
        return result

    def change_msg_task_state(affiliate_account: str, influencer_id: int, current_state: MsgTaskStates, state: MsgTaskStates):
        """Set messag tasks's state from current_state to state."""
        
        stmt = (
            update(MsgTask)
            .where(MsgTask.affiliate_account == affiliate_account)
            .where(MsgTask.influencer_id == influencer_id) 
            .where(MsgTask.state == current_state)
            .values(state=state)
            )
            
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()



if __name__ == '__main__':
    
    import asyncio

    async def get(affiliate_account: str, influencer_id: int, state):

        result = await MsgTaskService.filtered_msg_tasks(affiliate_account, influencer_id, state)

        return df(result)


    print(asyncio.run(get('BD', 302, MsgTaskStates.sent)))
    MsgTaskService.change_msg_task_state('BD', 302, MsgTaskStates.sent, MsgTaskStates.in_store)
    print('1'.center(80, '-'))
    print(asyncio.run(get('BD', 302, MsgTaskStates.sent)))
    print('2'.center(80, '-'))
    MsgTaskService.change_msg_task_state('BD', 302, MsgTaskStates.in_store, MsgTaskStates.sent)
    print('3'.center(80, '-'))
    print(asyncio.run(get('BD', 302, MsgTaskStates.sent)))
