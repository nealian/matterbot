from typing import Literal
import inspect

import fastapi

from matterbot.models import (
    OutgoingWebhookBody,
    OutgoingWebhookResponseBody,
    SlashWebhookBody,
    SlashWebhookResponseBody,
)


class MatterbotServer:
    def __init__(self) -> None:
        self.router = fastapi.APIRouter()
        pass

    def add_outgoing(  # Want to add more fastapi magic path operator arguments
        self,
        fn,  # callable?
        path: str,
        # *args,
        method: Literal["POST", "GET"] = "POST",
        oper_args={},
        # **kwargs,
    ):
        fn_signature = inspect.signature(fn)
        fn_signature.parameters

        def handler():
            pass

        if method == "POST":
            self.router.post(
                fn,
                path=path,
                response_model=OutgoingWebhookResponseBody,
                **oper_args,
            )
        elif method == "GET":
            self.router.get(
                fn,
                path=path,
                response_model=OutgoingWebhookResponseBody,
                **oper_args,
            )

        # self.router.add_api_route(
        #     path=path,
        #     response_model=OutgoingWebhookResponseBody,
        #     status_code=fastapi.status.HTTP_200_OK,
        #     methods=[method],
        #     **oper_args,
        # )
