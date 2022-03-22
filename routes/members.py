from sanic import Sanic
from sanic.response import json, HTTPResponse

app = Sanic.get_app("MembershipManagementSystem")


@app.get("/members/<uuid:str>")
async def members(request):
    return json({
        "test_key": "test_value"
    })
