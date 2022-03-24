import datetime
from contextvars import ContextVar
from models.models import Gender
from sanic import Sanic
from sanic.response import text, json, HTTPResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import selectinload, sessionmaker

app = Sanic("MembershipManagementSystem")
bind = create_async_engine("sqlite+aiosqlite:///dev.db", echo=True)
_base_model_session_ctx = ContextVar("session")


@app.middleware("request")
async def inject_session(request):
    request.ctx.session = sessionmaker(bind, AsyncSession, expire_on_commit=False)()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()


@app.post("/gender")
async def create_gender(request) -> HTTPResponse:
    session = request.ctx.session
    async with session.begin():
        gender = Gender(id='3', created_on=datetime.date.today(), created_by="me", name="male1", description="test", valid_flag='Y')
        session.add_all([gender])
    return json(gender)


@app.get("/gender/<pk:int>")
async def get_gender(request, pk) -> HTTPResponse:
    session = request.ctx.session
    async with session.begin():
        stmt = select(Gender).where(Gender.id == pk).options(selectinload(Gender.cars))
        result = await session.execute(stmt)
        gender = result.scalar()

    if not gender:
        return json(dict())

    return json(gender.to_dict())


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
