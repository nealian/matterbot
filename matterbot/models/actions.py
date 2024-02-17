from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, HttpUrl


class MessageActionIntegration(BaseModel):
    url: HttpUrl
    context: dict


class MessageActionSelectOption(BaseModel):
    text: str
    value: str


class MessageActionStyle(StrEnum):
    Good = "good"
    Warning = "warning"
    Danger = "danger"
    Default = "default"
    Primary = "primary"
    Success = "success"


class MessageActionType(StrEnum):
    Select = "select"
    Button = "button"


class MessageActionDataSource(StrEnum):
    Channels = "channels"
    Users = "users"


class MessageAction(BaseModel):
    id: str
    name: str
    style: Optional[MessageActionStyle] = None
    integration: Optional[MessageActionIntegration] = None
    type: Optional[MessageActionType] = None
    data_source: Optional[MessageActionDataSource] = None
    options: Optional[list[MessageActionSelectOption]] = None
