from models.models import Address
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


class AddressView(HTTPMethodView):

    @staticmethod
    async def get(request: Request, pk: str) -> HTTPResponse:
        """
        Gets address data based on provided id (pk).

        :param request: `Request` object
        :param pk: primary key of address table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            stmt: Select = select(Address).where(Address.id == pk)
            result: Result = await session.execute(stmt)
            address: Address = result.scalar()

        if not address:
            return json(dict())

        return json(address.to_dict(), default=str)

    @staticmethod
    async def patch(request: Request, pk: str) -> HTTPResponse:
        """
        Alter specific address entry in database.

        :param request: `Request` object
        :param pk: primary key of address table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        payload: Dict[str, Any] = {k: v for k, v in request.json.items() if k not in ['id', 'created_on', 'created_by']}
        async with session.begin():
            stmt: Update = update(Address).where(Address.id == pk).values(**payload)
            await session.execute(stmt)
        async with session.begin():
            stmt: Select = select(Address).where(Address.id == pk)
            result: Result = await session.execute(stmt)
            address: Address = result.scalar()
        return json(address.to_dict(), default=str)


class AddressesView(HTTPMethodView):

    @staticmethod
    async def get(request: Request) -> HTTPResponse:
        """
        Gets address collection from database.

        :param request: `Request` object
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            stmt: Select = select(Address)
            results: Result = await session.execute(stmt)
            addresses: List[Address] = results.scalars().fetchall()

        if not addresses:
            return json(dict())

        return json([row.to_dict() for row in addresses], default=str)

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
            address: Address = Address(**request.json)
            session.add_all([address])
        json_data: Dict[str, Any] = address.to_dict()
        return json(json_data, default=str)


bp_address = Blueprint("addresses", url_prefix="/addresses/")
bp_address.add_route(AddressView.as_view(), '/<pk:str>')
bp_address.add_route(AddressesView.as_view(), '/')
