import uplink

from matterbot.models import Incoming, SlashExtra


class MattermostClient(uplink.Consumer):
    """A Python client for (some small parts of) the Mattermost API / webhook integration"""

    @uplink.json
    @uplink.post
    def incoming_webhook(
        self,
        hook_url: uplink.Url,
        body: uplink.Body(type=Incoming),  # type: ignore
    ):
        pass

    @uplink.json
    @uplink.post
    def slash_command_delayed_response(
        self,
        response_url: uplink.Url,
        body: uplink.Body(type=SlashExtra),  # type: ignore
    ):
        pass
