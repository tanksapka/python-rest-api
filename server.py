from sanic import Sanic
from sanic.response import text, json, HTTPResponse

app = Sanic("MyHelloWorldApp")


@app.get("/")
async def hello_world(request) -> HTTPResponse:
    return text("Hello, world.")


@app.get("/test")
async def sample_data(request) -> HTTPResponse:
    return json({
        'data1': 1,
        'data2': 2,
        'data3': 3,
        'data4': 4,
    })
