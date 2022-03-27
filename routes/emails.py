from models.models import Email
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, HTTPResponse
from sanic.views import HTTPMethodView
from sqlalchemy import select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.dml import Update
from typing import Any, Dict, List


class EmailView(HTTPMethodView):

    @staticmethod
    async def get(request: Request, pk: str) -> HTTPResponse:
        """
        Gets email data based on provided id (pk).

        :param request: `Request` object
        :param pk: primary key of email table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            stmt: Select = select(Email).where(Email.id == pk)
            result: Result = await session.execute(stmt)
            email: Email = result.scalar()

        if not email:
            return json(dict())

        return json(email.to_dict(), default=str)

    @staticmethod
    async def patch(request: Request, pk: str) -> HTTPResponse:
        """
        Alter specific email entry in database.

        :param request: `Request` object
        :param pk: primary key of email table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        payload: Dict[str, Any] = {k: v for k, v in request.json.items() if k not in ['id', 'created_on', 'created_by']}
        async with session.begin():
            stmt: Update = update(Email).where(Email.id == pk).values(**payload)
            await session.execute(stmt)
        async with session.begin():
            stmt: Select = select(Email).where(Email.id == pk)
            result: Result = await session.execute(stmt)
            email: Email = result.scalar()
        return json(email.to_dict(), default=str)


class EmailsView(HTTPMethodView):

    @staticmethod
    async def get(request: Request) -> HTTPResponse:
        """
        Gets email collection from database.

        :param request: `Request` object
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            stmt: Select = select(Email)
            results: Result = await session.execute(stmt)
            emails: List[Email] = results.scalars().fetchall()

        if not emails:
            return json(dict())

        return json([row.to_dict() for row in emails], default=str)

    @staticmethod
    async def post(request: Request) -> HTTPResponse:
        """
        Inserts the provided JSON payload to corresponding table.

        :param request: `Request` object
        :return: JSON with id and timestamp
        """
        session: AsyncSession = request.ctx.session
        print(request.json)
        async with session.begin():
            email: Email = Email(**request.json)
            session.add_all([email])
        json_data: Dict[str, Any] = email.to_dict()
        return json(json_data, default=str)


bp_email = Blueprint("emails", url_prefix="/emails/")
bp_email.add_route(EmailView.as_view(), '/<pk:str>')
bp_email.add_route(EmailsView.as_view(), '/')
