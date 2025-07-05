from pydantic import BaseModel


class SendMessage(BaseModel):
    chat_id: str
    from_user: str
    to_user: str
    content: str
