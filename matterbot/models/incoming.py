from typing import Any, Optional

from pydantic import BaseModel, HttpUrl, root_validator

from matterbot.models.attachments import MessageAttachment


class IncomingWebhookBody(BaseModel, validate_assignment=True):
    text: Optional[str] = None
    channel: Optional[str] = None
    username: Optional[str] = None
    icon_url: Optional[HttpUrl] = None
    icon_emoji: Optional[str] = None
    attachments: Optional[list[MessageAttachment]] = None
    type: Optional[str] = None
    props: Optional[dict[str, Any]] = None

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
