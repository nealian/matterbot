import functools
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, thread
from enum import Enum
from typing import Annotated, Any, Callable, Literal, Optional, Sequence, Type

import fastapi
import starlette
from typing_extensions import Dict, Doc, List, Union

from matterbot.client import MattermostClient
from matterbot.models import Outgoing, OutgoingRequest, Slash, SlashExtra, SlashRequest


def _cdquit(fn_name):
    """
    Interrupt current thread.
    From https://gist.github.com/aaronchall/6331661fe0185c30a0b4
    """
    print(f"{fn_name} took too long", file=sys.stderr, flush=True)
    thread.interrupt_main()  # raises KeyboardInterrupt


def _exit_after(s):
    """
    use as decorator to exit process if function takes longer than s seconds
    from https://gist.github.com/aaronchall/6331661fe0185c30a0b4
    """

    def outer(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            timer = threading.Timer(interval=s, function=_cdquit, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            except KeyboardInterrupt:
                pass
            finally:
                timer.cancel()
            return result

        return inner

    return outer


class MatterbotServer:
    def __init__(self, fastapiapp: fastapi.FastAPI) -> None:
        self.router = fastapi.APIRouter()
        self.fastapp = fastapiapp
        self.executor = ThreadPoolExecutor()
        self.client = MattermostClient()

    def __call__(self) -> None:
        self.fastapp.include_router(self.router)

    def outgoing(
        self,
        callable: Callable,
        path: str,
        method: Literal["POST", "GET"] = "POST",
        status_code: Annotated[
            Optional[int],
            Doc(
                """
                The default status code to be used for the response.

                You could override the status code by returning a response directly.

                Read more about it in the
                [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
                """
            ),
        ] = None,
        tags: Annotated[
            Optional[List[Union[str, Enum]]],
            Doc(
                """
                A list of tags to be applied to the *path operation*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
                """
            ),
        ] = None,
        dependencies: Annotated[
            Optional[Sequence[fastapi.params.Depends]],
            Doc(
                """
                A list of dependencies (using `Depends()`) to be applied to the
                *path operation*.

                Read more about it in the
                [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
                """
            ),
        ] = None,
        summary: Annotated[
            Optional[str],
            Doc(
                """
                A summary for the *path operation*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                """
            ),
        ] = None,
        description: Annotated[
            Optional[str],
            Doc(
                """
                A description for the *path operation*.

                If not provided, it will be extracted automatically from the docstring
                of the *path operation function*.

                It can contain Markdown.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                """
            ),
        ] = None,
        response_description: Annotated[
            str,
            Doc(
                """
                The description for the default response.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = "Successful Response",
        responses: Annotated[
            Optional[Dict[Union[int, str], Dict[str, Any]]],
            Doc(
                """
                Additional responses that could be returned by this *path operation*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = None,
        deprecated: Annotated[
            Optional[bool],
            Doc(
                """
                Mark this *path operation* as deprecated.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = None,
        operation_id: Annotated[
            Optional[str],
            Doc(
                """
                Custom operation ID to be used by this *path operation*.

                By default, it is generated automatically.

                If you provide a custom operation ID, you need to make sure it is
                unique for the whole API.

                You can customize the
                operation ID generation with the parameter
                `generate_unique_id_function` in the `FastAPI` class.

                Read more about it in the
                [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                """
            ),
        ] = None,
        response_model_include: Annotated[
            Optional[fastapi.types.IncEx],
            Doc(
                """
                Configuration passed to Pydantic to include only certain fields in the
                response data.

                Read more about it in the
                [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                """
            ),
        ] = None,
        response_model_exclude: Annotated[
            Optional[fastapi.types.IncEx],
            Doc(
                """
                Configuration passed to Pydantic to exclude certain fields in the
                response data.

                Read more about it in the
                [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                """
            ),
        ] = None,
        response_model_by_alias: Annotated[
            bool,
            Doc(
                """
                Configuration passed to Pydantic to define if the response model
                should be serialized by alias when an alias is used.

                Read more about it in the
                [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                """
            ),
        ] = True,
        response_model_exclude_unset: Annotated[
            bool,
            Doc(
                """
                Configuration passed to Pydantic to define if the response data
                should have all the fields, including the ones that were not set and
                have their default values. This is different from
                `response_model_exclude_defaults` in that if the fields are set,
                they will be included in the response, even if the value is the same
                as the default.

                When `True`, default values are omitted from the response.

                Read more about it in the
                [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                """
            ),
        ] = False,
        response_model_exclude_defaults: Annotated[
            bool,
            Doc(
                """
                Configuration passed to Pydantic to define if the response data
                should have all the fields, including the ones that have the same value
                as the default. This is different from `response_model_exclude_unset`
                in that if the fields are set but contain the same default values,
                they will be excluded from the response.

                When `True`, default values are omitted from the response.

                Read more about it in the
                [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                """
            ),
        ] = False,
        response_model_exclude_none: Annotated[
            bool,
            Doc(
                """
                Configuration passed to Pydantic to define if the response data should
                exclude fields set to `None`.

                This is much simpler (less smart) than `response_model_exclude_unset`
                and `response_model_exclude_defaults`. You probably want to use one of
                those two instead of this one, as those allow returning `None` values
                when it makes sense.

                Read more about it in the
                [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none).
                """
            ),
        ] = False,
        include_in_schema: Annotated[
            bool,
            Doc(
                """
                Include this *path operation* in the generated OpenAPI schema.

                This affects the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).
                """
            ),
        ] = True,
        response_class: Annotated[
            Type[starlette.responses.Response],
            Doc(
                """
                Response class to be used for this *path operation*.

                This will not be used if you return a response directly.

                Read more about it in the
                [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
                """
            ),
        ] = fastapi.datastructures.Default(starlette.responses.JSONResponse),
        name: Annotated[
            Optional[str],
            Doc(
                """
                Name for this *path operation*. Only used internally.
                """
            ),
        ] = None,
        callbacks: Annotated[
            Optional[List[starlette.routing.BaseRoute]],
            Doc(
                """
                List of *path operations* that will be used as OpenAPI callbacks.

                This is only for OpenAPI documentation, the callbacks won't be used
                directly.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                """
            ),
        ] = None,
        openapi_extra: Annotated[
            Optional[Dict[str, Any]],
            Doc(
                """
                Extra metadata to be included in the OpenAPI schema for this *path
                operation*.

                Read more about it in the
                [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
                """
            ),
        ] = None,
        generate_unique_id_function: Annotated[
            Callable[[fastapi.routing.APIRoute], str],
            Doc(
                """
                Customize the function used to generate unique IDs for the *path
                operations* shown in the generated OpenAPI.

                This is particularly useful when automatically generating clients or
                SDKs for your API.

                Read more about it in the
                [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                """
            ),
        ] = fastapi.datastructures.Default(fastapi.utils.generate_unique_id),
    ) -> Callable[[fastapi.types.DecoratedCallable], fastapi.types.DecoratedCallable]:
        """Create a new "outgoing" webhook; the callable should have a "request" named arg.  (All other callable args && kwargs are passed through to the callable.)
        The request will have the following attributes:
          channel_id, channel_name, team_domain, team_id, post_id, text, token, trigger_word, user_id, user_name as str,
          and timestamp as datetime.datetime.

        Adds a new FastAPI *path operation* using an HTTP GET or POST (default) operation, depending on the method selected.
        Uses the Outgoing model to validate the response type.

        Effectively a wrapper around fastapi.APIRouter.get / .post

        ## Example

        ```python
        from matterbot import MatterbotServer
        from fastapi import FastAPI

        fastapp = FastAPI()
        server = MatterbotServer(fastapp)

        @server.outgoing("/echo")
        def echo(request) -> dict:
            echo_icon = "https://m.media-amazon.com/images/I/41U7UzQyiJL._AC_SL1000_.jpg"  # Amazon Echo Dot (5th gen), Deep Sea Blue
            return {
                "text": request.text,
                "response_type": "comment",
                "username": "echobot",
                "icon_url": echo_icon,
            }

        server()
        ```
        """

        @functools.wraps(callable)
        def handler(request: OutgoingRequest, *args, **kwargs):
            callable(*args, request=request, **kwargs)

        return self.router.api_route(
            handler,
            path=path,
            response_model=Outgoing,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            methods=[method],
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def slash_delayed_response(
        self,
        callable: Callable,
        path: str,
        token: str,
        method: Literal["POST", "GET"] = "POST",
        hooks: Annotated[
            Optional[Callable | List[Callable]],
            Doc(
                """A callable (or list of up to five callables) that will return additional responses when complete
                (time limit 30 minutes).

                These will be expected to still be of the same response class as the decorated callable, and will be
                validated against the SlashExtra response model.
                """
            ),
        ] = None,
        null_response: Annotated[
            bool,
            Doc(
                """
                When expecting to use the "response_url" of the request for delayed responses, you may wish to return an empty body.  Set this to True in this case.
                """
            ),
        ] = False,
        status_code: Annotated[
            Optional[int],
            Doc(
                """
                The default status code to be used for the response.

                You could override the status code by returning a response directly.

                Read more about it in the
                [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
                """
            ),
        ] = None,
        tags: Annotated[
            Optional[List[Union[str, Enum]]],
            Doc(
                """
                A list of tags to be applied to the *path operation*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
                """
            ),
        ] = None,
        dependencies: Annotated[
            Optional[Sequence[fastapi.params.Depends]],
            Doc(
                """
                A list of dependencies (using `Depends()`) to be applied to the
                *path operation*.

                Read more about it in the
                [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
                """
            ),
        ] = None,
        summary: Annotated[
            Optional[str],
            Doc(
                """
                A summary for the *path operation*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                """
            ),
        ] = None,
        description: Annotated[
            Optional[str],
            Doc(
                """
                A description for the *path operation*.

                If not provided, it will be extracted automatically from the docstring
                of the *path operation function*.

                It can contain Markdown.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                """
            ),
        ] = None,
        response_description: Annotated[
            str,
            Doc(
                """
                The description for the default response.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = "Successful Response",
        responses: Annotated[
            Optional[Dict[Union[int, str], Dict[str, Any]]],
            Doc(
                """
                Additional responses that could be returned by this *path operation*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = None,
        deprecated: Annotated[
            Optional[bool],
            Doc(
                """
                Mark this *path operation* as deprecated.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = None,
        operation_id: Annotated[
            Optional[str],
            Doc(
                """
                Custom operation ID to be used by this *path operation*.

                By default, it is generated automatically.

                If you provide a custom operation ID, you need to make sure it is
                unique for the whole API.

                You can customize the
                operation ID generation with the parameter
                `generate_unique_id_function` in the `FastAPI` class.

                Read more about it in the
                [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                """
            ),
        ] = None,
        response_model_include: Annotated[
            Optional[fastapi.types.IncEx],
            Doc(
                """
                Configuration passed to Pydantic to include only certain fields in the
                response data.

                Read more about it in the
                [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                """
            ),
        ] = None,
        response_model_exclude: Annotated[
            Optional[fastapi.types.IncEx],
            Doc(
                """
                Configuration passed to Pydantic to exclude certain fields in the
                response data.

                Read more about it in the
                [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                """
            ),
        ] = None,
        response_model_by_alias: Annotated[
            bool,
            Doc(
                """
                Configuration passed to Pydantic to define if the response model
                should be serialized by alias when an alias is used.

                Read more about it in the
                [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
                """
            ),
        ] = True,
        response_model_exclude_unset: Annotated[
            bool,
            Doc(
                """
                Configuration passed to Pydantic to define if the response data
                should have all the fields, including the ones that were not set and
                have their default values. This is different from
                `response_model_exclude_defaults` in that if the fields are set,
                they will be included in the response, even if the value is the same
                as the default.

                When `True`, default values are omitted from the response.

                Read more about it in the
                [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                """
            ),
        ] = False,
        response_model_exclude_defaults: Annotated[
            bool,
            Doc(
                """
                Configuration passed to Pydantic to define if the response data
                should have all the fields, including the ones that have the same value
                as the default. This is different from `response_model_exclude_unset`
                in that if the fields are set but contain the same default values,
                they will be excluded from the response.

                When `True`, default values are omitted from the response.

                Read more about it in the
                [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
                """
            ),
        ] = False,
        response_model_exclude_none: Annotated[
            bool,
            Doc(
                """
                Configuration passed to Pydantic to define if the response data should
                exclude fields set to `None`.

                This is much simpler (less smart) than `response_model_exclude_unset`
                and `response_model_exclude_defaults`. You probably want to use one of
                those two instead of this one, as those allow returning `None` values
                when it makes sense.

                Read more about it in the
                [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none).
                """
            ),
        ] = False,
        include_in_schema: Annotated[
            bool,
            Doc(
                """
                Include this *path operation* in the generated OpenAPI schema.

                This affects the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).
                """
            ),
        ] = True,
        response_class: Annotated[
            Type[starlette.responses.Response],
            Doc(
                """
                Response class to be used for this *path operation*.

                This will not be used if you return a response directly.

                Read more about it in the
                [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
                """
            ),
        ] = fastapi.datastructures.Default(starlette.responses.JSONResponse),
        name: Annotated[
            Optional[str],
            Doc(
                """
                Name for this *path operation*. Only used internally.
                """
            ),
        ] = None,
        callbacks: Annotated[
            Optional[List[starlette.routing.BaseRoute]],
            Doc(
                """
                List of *path operations* that will be used as OpenAPI callbacks.

                This is only for OpenAPI documentation, the callbacks won't be used
                directly.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                """
            ),
        ] = None,
        openapi_extra: Annotated[
            Optional[Dict[str, Any]],
            Doc(
                """
                Extra metadata to be included in the OpenAPI schema for this *path
                operation*.

                Read more about it in the
                [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
                """
            ),
        ] = None,
        generate_unique_id_function: Annotated[
            Callable[[fastapi.routing.APIRoute], str],
            Doc(
                """
                Customize the function used to generate unique IDs for the *path
                operations* shown in the generated OpenAPI.

                This is particularly useful when automatically generating clients or
                SDKs for your API.

                Read more about it in the
                [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                """
            ),
        ] = fastapi.datastructures.Default(fastapi.utils.generate_unique_id),
    ) -> Callable[[fastapi.types.DecoratedCallable], fastapi.types.DecoratedCallable]:
        """Create a new "slash" webhook; the callable should have a "request" named arg.  (All other callable args && kwargs are passed through to the callable.)
        The request will have the following attributes:
          channel_id, channel_name, command, response_url, team_domain, team_id, text, token, trigger_id, user_id, user_name as str.

        Adds a new FastAPI *path operation* using an HTTP GET or POST (default) operation, depending on the method selected.
        Optionally uses the Slash model to validate the response type; you can use `null_response=True` in conjunction with `hooks` to send no response now and
        send one (or more) responses later.

        The callables in `hooks` should take exactly one argument (request), should expect the return value to be validated by SlashExtra,
        and will be executed using a concurrent.futures.ThreadPoolExecutor.

        Effectively a wrapper around fastapi.APIRouter.get / .post with MM integration token validation.

        ## Example

        ```python
        from matterbot import MatterbotServer
        from fastapi import FastAPI

        fastapp = FastAPI()
        server = MatterbotServer(fastapp)

        echo_mm_token = "abcdefg"

        @server.slash("/echo", token=echo_mm_token)
        def echo(request) -> dict:
            echo_icon = "https://m.media-amazon.com/images/I/41U7UzQyiJL._AC_SL1000_.jpg"  # Amazon Echo Dot (5th gen), Deep Sea Blue
            return {
                "text": request.text,
                "response_type": "comment",
                "username": "echobot",
                "icon_url": echo_icon,
            }

        server() # Registers router && routes with the FastAPI app
        ```
        """

        @functools.wraps(callable, updated=["__dict__", "request"])
        def handler(request: SlashRequest, *args, **kwargs):
            if request.token != token:
                raise fastapi.HTTPException(
                    status_code=401, detail="Unauthorized: provided token did not match"
                )

            # Response URL is only valid for 30 minutes, so don't run any longer than that
            @_exit_after(60 * 30)
            def run_hook(hook: Callable):
                url = request.response_url
                response = hook(request)
                self.client.slash_command_delayed_response(
                    response_url=url,
                    body=response,
                )

            if __builtins__.callable(hooks):
                hooks = [hooks]
            elif hooks is not None:
                for hook in hooks:
                    self.executor.submit(run_hook, hook)

            return callable(*args, request=request, **kwargs)

        return self.router.api_route(
            handler,
            path=path,
            response_model=None if null_response else Slash,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            methods=[method],
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    slash = functools.partialmethod(
        slash_delayed_response, hooks=None, null_response=False
    )
    slash.__doc__ = """Create a new "slash" webhook; the callable should have a "request" named arg.  (All other callable args && kwargs are passed through to the callable.)
        The request will have the following attributes:
            channel_id, channel_name, command, response_url, team_domain, team_id, text, token, trigger_id, user_id, user_name as str.

        Adds a new FastAPI *path operation* using an HTTP GET or POST (default) operation, depending on the method selected.
        Uses the Slash model to validate the response type.

        Effectively a wrapper around fastapi.APIRouter.get / .post with MM integration token validation.

        ## Example

        ```python
        from matterbot import MatterbotServer
        from fastapi import FastAPI

        fastapp = FastAPI()
        server = MatterbotServer(fastapp)

        echo_mm_token = "abcdefg"

        @server.slash("/echo", token=echo_mm_token)
        def echo(request) -> dict:
            echo_icon = "https://m.media-amazon.com/images/I/41U7UzQyiJL._AC_SL1000_.jpg"  # Amazon Echo Dot (5th gen), Deep Sea Blue
            return {
                "text": request.text,
                "response_type": "comment",
                "username": "echobot",
                "icon_url": echo_icon,
            }

        server() # Registers router && routes with the FastAPI app
        ```
        """
