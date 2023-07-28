from pydantic import BaseModel, Field, ConfigDict


class TgUser(BaseModel):
    id: int
    username: str | None


class Message(BaseModel):
    message_id: int
    text: str | None
    msg_from: TgUser = Field(..., alias='from')

    model_config = ConfigDict(populate_by_name=True)


class UpdateObj(BaseModel):
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: list[UpdateObj]


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message
