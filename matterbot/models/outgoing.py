from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel, HttpUrl, root_validator

from matterbot.models.attachments import MessageAttachment


class OutgoingWebhookResponseType(StrEnum):
    Comment = "comment"
    Post = "post"
    Reply = "comment"


class OutgoingWebhookBody(BaseModel):
    """https://developers.mattermost.com/integrate/webhooks/outgoing/#use-an-outgoing-webhook"""
    channel_id: str
    channel_name: str
    team_domain: str
    team_id: str
    post_id: str
    text: str
    timestamp: datetime
    token: str
    trigger_word: str
    user_id: str
    user_name: str


class OutgoingWebhookResponseBody(BaseModel, validate_assignment=True):
    """https://developers.mattermost.com/integrate/webhooks/outgoing/#parameters"""
    text: Optional[str] = None
    response_type: Optional[OutgoingWebhookResponseType] = None
    username: Optional[str] = None
    icon_url: Optional[HttpUrl] = None
    attachments: Optional[list[MessageAttachment]] = None
    type: Optional[str] = None
    props: Optional[dict[str, Any]]

    @root_validator(pre=True)
    def validate_content_fields(cls, values):
        txt: str = values.get("text", "")
        att: list = values.get("attachments", [])
        type: str = values.get("type", "")
        if txt in [None, ""]:
            if att in [None, []]:
                raise ValueError(
                    "Either 'text' or 'attachments' must be defined and nonempty"
                )
        elif att not in [None, []]:
            raise ValueError(
                "Only one of 'text' and 'attachments' may be defined and nonempty"
            )
        if type != "" and not type.startswith("custom_"):
            raise ValueError("If 'type' is not blank, it must begin with 'custom_'.")
        return values
