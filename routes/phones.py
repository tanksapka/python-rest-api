from models.models import Phone
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


class PhoneView(HTTPMethodView):

    @staticmethod
    async def get(request: Request, pk: str) -> HTTPResponse:
        """
        Gets phone data based on provided id (pk).

        :param request: `Request` object
        :param pk: primary key of phone table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            stmt: Select = select(Phone).where(Phone.id == pk)
            result: Result = await session.execute(stmt)
            phone: Phone = result.scalar()

        if not phone:
            return json(dict())

        return json(phone.to_dict(), default=str)

    @staticmethod
    async def patch(request: Request, pk: str) -> HTTPResponse:
        """
        Alter specific phone entry in database.

        :param request: `Request` object
        :param pk: primary key of phone table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        payload: Dict[str, Any] = {k: v for k, v in request.json.items() if k not in ['id', 'created_on', 'created_by']}
        async with session.begin():
            stmt: Update = update(Phone).where(Phone.id == pk).values(**payload)
            await session.execute(stmt)
        async with session.begin():
            stmt: Select = select(Phone).where(Phone.id == pk)
            result: Result = await session.execute(stmt)
            phone: Phone = result.scalar()
        return json(phone.to_dict(), default=str)


class PhonesView(HTTPMethodView):

    @staticmethod
    async def get(request: Request) -> HTTPResponse:
        """
        Gets phone collection from database.

        :param request: `Request` object
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            stmt: Select = select(Phone)
            results: Result = await session.execute(stmt)
            phones: List[Phone] = results.scalars().fetchall()

        if not phones:
            return json(dict())

        return json([row.to_dict() for row in phones], default=str)

    @staticmethod
    async def post(request: Request) -> HTTPResponse:
        """
        Inserts the provided JSON payload to corresponding table.

        :param request: `Request` object
        :return: JSON with id and timestamp
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            phone: Phone = Phone(**request.json)
            session.add_all([phone])
        json_data: Dict[str, Any] = phone.to_dict()
        return json(json_data, default=str)


bp_phone = Blueprint("phones", url_prefix="/phones/")
bp_phone.add_route(PhoneView.as_view(), '/<pk:str>')
bp_phone.add_route(PhonesView.as_view(), '/')
