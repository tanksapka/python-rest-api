from contextvars import ContextVar
from routes.addresses import bp_address
from routes.emails import bp_email
from routes.maps import bp_address_type, bp_email_type, bp_gender, bp_membership_fee_category, bp_phone_type
from routes.organizations import bp_organization
from routes.people import bp_person
from sanic import Sanic
from sanic.request import Request
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

app = Sanic("MembershipManagementSystem")
bind = create_async_engine("sqlite+aiosqlite:///dev.db", echo=True)
_base_model_session_ctx = ContextVar("session")


@app.middleware("request")
async def inject_session(request: Request) -> None:
    request.ctx.session = sessionmaker(bind, AsyncSession, expire_on_commit=False)()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)


@app.middleware("response")
async def close_session(request: Request, response) -> None:
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()


app.blueprint(bp_gender)
app.blueprint(bp_membership_fee_category)
app.blueprint(bp_address_type)
app.blueprint(bp_phone_type)
app.blueprint(bp_email_type)
app.blueprint(bp_person)
app.blueprint(bp_organization)
app.blueprint(bp_address)
app.blueprint(bp_email)
