from contextvars import ContextVar
from cors import add_cors_headers
from options import setup_options
from routes.addresses import bp_address
from routes.emails import bp_email
from routes.maps import bp_address_type, bp_email_type, bp_gender, bp_membership_fee_category, bp_phone_type
from routes.memberships import bp_memberships
from routes.organizations import bp_organization
from routes.people import bp_person
from routes.phones import bp_phone
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


app.blueprint([
    bp_gender, bp_membership_fee_category, bp_address_type, bp_phone_type, bp_email_type, bp_person, bp_organization,
    bp_address, bp_email, bp_phone, bp_memberships
])

# Add OPTIONS handlers to any route that is missing it
app.register_listener(setup_options, "before_server_start")

# Fill in CORS headers
app.register_middleware(add_cors_headers, "response")
