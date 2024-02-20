from typing import Optional

from pydantic import BaseModel, HttpUrl
from pydantic_extra_types.color import Color

from matterbot.models.actions import MessageAction


class MessageAttachmentField(BaseModel):
    """https://developers.mattermost.com/integrate/reference/message-attachments/#fields"""
    title: str
    value: str
    short: Optional[bool] = None


class MessageAttachment(BaseModel):
    """https://developers.mattermost.com/integrate/reference/message-attachments/
    and
    https://developers.mattermost.com/integrate/plugins/interactive-messages/"""

    ## Attachment options
    fallback: str
    color: Optional[Color] = None
    pretext: Optional[str] = None
    text: str
    ## Author details
    author_name: Optional[str] = None
    author_link: Optional[HttpUrl] = None
    author_icon: Optional[HttpUrl] = None
    ## Titles
    title: Optional[str] = None
    title_link: Optional[HttpUrl] = None
    ## Fields
    fields: Optional[list[MessageAttachmentField]] = None
    ## Images
    image_url: Optional[HttpUrl] = None
    thumb_url: Optional[HttpUrl] = None
    ## Footer
    footer: Optional[str] = None
    footer_icon: Optional[HttpUrl] = None
    ## interactive-messages
    actions: Optional[list[MessageAction]] = None
