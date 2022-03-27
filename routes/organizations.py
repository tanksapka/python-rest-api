from models.models import Organization
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


class OrganizationView(HTTPMethodView):

    @staticmethod
    async def get(request: Request, pk: str) -> HTTPResponse:
        """
        Gets organization data based on provided id (pk).

        :param request: `Request` object
        :param pk: primary key of organization table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            stmt: Select = select(Organization).where(Organization.id == pk)
            result: Result = await session.execute(stmt)
            organization: Organization = result.scalar()

        if not organization:
            return json(dict())

        return json(organization.to_dict(), default=str)

    @staticmethod
    async def patch(request: Request, pk: str) -> HTTPResponse:
        """
        Alter specific organization entry in database.

        :param request: `Request` object
        :param pk: primary key of organization table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        payload: Dict[str, Any] = {k: v for k, v in request.json.items() if k not in ['id', 'created_on', 'created_by']}
        async with session.begin():
            stmt: Update = update(Organization).where(Organization.id == pk).values(**payload)
            await session.execute(stmt)
        async with session.begin():
            stmt: Select = select(Organization).where(Organization.id == pk)
            result: Result = await session.execute(stmt)
            organization: Organization = result.scalar()
        return json(organization.to_dict(), default=str)


class OrganizationsView(HTTPMethodView):

    @staticmethod
    async def get(request: Request) -> HTTPResponse:
        """
        Gets organization collection from database.

        :param request: `Request` object
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            stmt: Select = select(Organization)
            results: Result = await session.execute(stmt)
            organizations: List[Organization] = results.scalars().fetchall()

        if not organizations:
            return json(dict())

        return json([row.to_dict() for row in organizations], default=str)

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
            organization: Organization = Organization(**request.json)
            session.add_all([organization])
        json_data: Dict[str, Any] = organization.to_dict()
        return json(json_data, default=str)


bp_organization = Blueprint("organizations", url_prefix="/organizations/")
bp_organization.add_route(OrganizationView.as_view(), '/<pk:str>')
bp_organization.add_route(OrganizationsView.as_view(), '/')
