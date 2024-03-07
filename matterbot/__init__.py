#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A Mattermost chatops framework library, inspired by (and using) Typer, FastAPI, and Uplink"""

__version__ = "0.1.0"

from matterbot.client import MattermostClient
from matterbot.models.actions import MessageAction as Action
from matterbot.models.actions import MessageActionIntegration as ActionIntegration
from matterbot.models.actions import MessageActionSelectOption as ActionSelect
from matterbot.models.incoming import IncomingWebhookBody as Incoming
from matterbot.models.outgoing import OutgoingWebhookBody as OutgoingRequest
from matterbot.models.outgoing import OutgoingWebhookResponseBody as Outgoing
from matterbot.models.outgoing import OutgoingWebhookResponseType as OutgoingResponseType
from matterbot.models.slash import SlashWebhookBody as SlashRequest
from matterbot.models.slash import SlashWebhookExtraResponse as SlashExtra
from matterbot.models.slash import SlashWebhookResponseBody as Slash
from matterbot.models.slash import SlashWebhookResponseType as SlashResponseType
from matterbot.server import MatterbotServer

__all__ = [
    "Action",
    "ActionIntegration",
    "ActionSelect",
    "Incoming",
    "MattermostClient",
    "MatterbotServer",
    "Outgoing",
    "OutgoingRequest",
    "OutgoingResponseType",
    "Slash",
    "SlashExtra",
    "SlashRequest",
    "SlashResponseType",
]
