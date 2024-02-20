#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A Mattermost chatops framework library, inspired by (and using) Typer, FastAPI, and Uplink"""

__version__ = "0.1.0"

from matterbot.models.actions import MessageAction as Action
from matterbot.models.actions import MessageActionIntegration as ActionIntegration
from matterbot.models.actions import MessageActionSelectOption as ActionSelect
from matterbot.models.incoming import IncomingWebhookBody as Incoming
from matterbot.models.outgoing import OutgoingWebhookResponseBody as Outgoing
from matterbot.models.slash import SlashWebhookExtraResponse as SlashExtra
from matterbot.models.slash import SlashWebhookResponseBody as Slash
from matterbot.server import MatterbotServer

__all__ = [
    "Action",
    "ActionIntegration",
    "ActionSelect",
    "Incoming",
    "MatterbotServer",
    "Outgoing",
    "Slash",
    "SlashExtra",
]
