import uplink

from matterbot.models import IncomingWebhookBody, SlashWebhookResponseBody


@uplink.json
class MattermostClient(uplink.Consumer):
    """A Python client for (some small parts of) the Mattermost API / webhook integration"""

    @uplink.post("/hooks/{key}")
    def incoming_webhook(
        self,
        key: uplink.Path(type=str),  # type: ignore # VSCode insists that you can't call here, for some reason
        body: uplink.Body(type=IncomingWebhookBody),  # type: ignore
    ):
        pass

    @uplink.post
    def slash_command_delayed_response(
        self,
        response_url: uplink.Url,
        body: uplink.Body(type=SlashWebhookResponseBody),  # type: ignore
    ):
        pass
