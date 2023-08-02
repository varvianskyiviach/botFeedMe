from pydantic import BaseModel


class CallbackItem(BaseModel):
    name: str
    callback_data: str
