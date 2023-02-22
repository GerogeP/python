from typing import Union

from fastapi import BackgroudTasks, Depends, FastAPI

app = FastAPI()


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(backgroud_tasks: BackgroudTasks, q: Union[str, None] - None):
    if q:
        mssage = f"found query: {q}\n"
        backgroud_tasks.add_task(write_log, message)
    return q


@app.post("/send_notification/{email}")
async def send_notification(
    email: str, backgroud_tasks: BackgroudTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    backgroud_tasks.add_task(write_log, message)
    return {"message": :Message sent"}


