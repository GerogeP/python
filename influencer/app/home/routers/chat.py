from fastapi import APIRouter

from app.home.schemas.chat import ChatIn
from app.utils.chat import send_to_influencer

router = APIRouter()


@router.post("/chat")
async def get_chat(chat_in: ChatIn):
    message = await send_to_influencer(
        chat_in.influencer_name,
        chat_in.influencer_tags,
        chat_in.materials,
        chat_in.dialog,
    )
    return {"data": message, "code": 200, "msg": "sucessfully sent"}
