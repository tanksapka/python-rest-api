from models.models import Membership, Organization, Person
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, HTTPResponse
from sanic.views import HTTPMethodView
from sqlalchemy import select, update
from sqlalchemy.engine import Result, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.dml import Update
from typing import Any, Dict


query_membership: Select = select(
    Membership.id,
    Membership.person_id,
    Person.name.label('person_name'),
    Membership.organization_id,
    Organization.name.label('organization_name'),
    Membership.active_flag,
    Membership.inactivity_status_id,
    Membership.event_date,
    Membership.notes,
).join(Person).join(Organization)


class MembershipView(HTTPMethodView):

    @staticmethod
    async def get(request: Request, pk: str) -> HTTPResponse:
        """
        Gets membership data based on provided id (pk).

        :param request: `Request` object
        :param pk: primary key of membership table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            stmt: Select = query_membership.where(Membership.id == pk)
            result: Result = await session.execute(stmt)
            membership: Row = result.first()

        if not membership:
            return json(dict())

        return json(dict(membership), default=str)

    @staticmethod
    async def patch(request: Request, pk: str) -> HTTPResponse:
        """
        Alter specific membership entry in database.

        :param request: `Request` object
        :param pk: primary key of membership table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        payload: Dict[str, Any] = {k: v for k, v in request.json.items() if k not in ['id', 'created_on', 'created_by']}
        async with session.begin():
            stmt: Update = update(Membership).where(Membership.id == pk).values(**payload)
            await session.execute(stmt)
        async with session.begin():
            stmt: Select = select(Membership).where(Membership.id == pk)
            result: Result = await session.execute(stmt)
            membership: Membership = result.scalar()
        return json(membership.to_dict(), default=str)


class MembershipsView(HTTPMethodView):

    @staticmethod
    async def get(request: Request) -> HTTPResponse:
        """
        Gets membership collection from database.

        :param request: `Request` object
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            results: Result = await session.execute(query_membership)

        return json(list(map(dict, results)), default=str)

    @staticmethod
    async def post(request: Request) -> HTTPResponse:
        """
        Inserts the provided JSON payload to corresponding table.

        :param request: `Request` object
        :return: JSON with id and timestamp
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            membership: Membership = Membership(**request.json)
            session.add_all([membership])
        json_data: Dict[str, Any] = membership.to_dict()
        return json(json_data, default=str)


bp_memberships = Blueprint("memberships", url_prefix="/memberships/")
bp_memberships.add_route(MembershipView.as_view(), '/<pk:str>')
bp_memberships.add_route(MembershipsView.as_view(), '/')
