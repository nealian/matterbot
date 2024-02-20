from enum import StrEnum
from typing import Any, Optional

from pydantic import AnyUrl, BaseModel, HttpUrl, root_validator

from matterbot.models.attachments import MessageAttachment


class SlashWebhookBody(BaseModel):
    """https://developers.mattermost.com/integrate/slash-commands/custom/ step 4"""
    channel_id: str
    channel_name: str
    command: str
    response_url: HttpUrl
    team_domain: str
    team_id: str
    text: str
    token: str
    trigger_id: str
    user_id: str
    user_name: str


class SlashWebhookResponseType(StrEnum):
    Ephemeral = "ephemeral"
    UserOnly = "ephemeral"
    Post = "in_channel"
    InChannel = "in_channel"


class SlashWebhookExtraResponse(BaseModel, validate_assignment=True):
    """https://developers.mattermost.com/integrate/slash-commands/custom/#response-parameters"""
    text: Optional[str] = None
    attachments: Optional[list[MessageAttachment]] = None
    response_type: Optional[SlashWebhookResponseType] = None
    username: Optional[str] = None
    channel_id: Optional[str] = None
    icon_url: Optional[HttpUrl] = None
    type: Optional[str] = None

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


class SlashWebhookResponseBody(BaseModel, validate_assignment=True):
    """https://developers.mattermost.com/integrate/slash-commands/custom/#response-parameters"""
    text: Optional[str] = None
    attachments: Optional[list[MessageAttachment]] = None
    response_type: Optional[SlashWebhookResponseType] = None
    username: Optional[str] = None
    channel_id: Optional[str] = None
    icon_url: Optional[HttpUrl] = None
    goto_location: Optional[AnyUrl] = None
    type: Optional[str] = None
    extra_responses: Optional[list[SlashWebhookExtraResponse]] = None
    skip_slack_parsing: Optional[bool] = None
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
