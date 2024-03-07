from matterbot import MatterbotServer, SlashRequest, SlashResponseType
from fastapi import FastAPI

fastapp = FastAPI()
server = MatterbotServer(fastapiapp=fastapp)

echo_token = "abcde"

@server.slash("/echo", token=echo_token)
def echo(request: SlashRequest) -> dict:
    echo_icon = "https://m.media-amazon.com/images/I/41U7UzQyiJL._AC_SL1000_.jpg"  # Amazon Echo Dot (5th gen), Deep Sea Blue
    return {
        "text": request.text,
        "response_type": SlashResponseType.Post,
        "username": "echobot",
        "icon_url": echo_icon,
    }

server()
