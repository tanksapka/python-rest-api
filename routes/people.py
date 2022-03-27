from models.models import Person
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


class PersonView(HTTPMethodView):

    @staticmethod
    async def get(request: Request, pk: str) -> HTTPResponse:
        """
        Gets person data based on provided id (pk).

        :param request: `Request` object
        :param pk: primary key of person table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            stmt: Select = select(Person).where(Person.id == pk)
            result: Result = await session.execute(stmt)
            person: Person = result.scalar()

        if not person:
            return json(dict())

        return json(person.to_dict(), default=str)

    @staticmethod
    async def patch(request: Request, pk: str) -> HTTPResponse:
        """
        Alter specific person entry in database.

        :param request: `Request` object
        :param pk: primary key of person table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        payload: Dict[str, Any] = {k: v for k, v in request.json.items() if k not in ['id', 'created_on', 'created_by']}
        async with session.begin():
            stmt: Update = update(Person).where(Person.id == pk).values(**payload)
            await session.execute(stmt)
        async with session.begin():
            stmt: Select = select(Person).where(Person.id == pk)
            result: Result = await session.execute(stmt)
            person: Person = result.scalar()
        return json(person.to_dict(), default=str)


class PeopleView(HTTPMethodView):

    @staticmethod
    async def get(request: Request) -> HTTPResponse:
        """
        Gets person collection from database.

        :param request: `Request` object
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            stmt: Select = select(Person)
            results: Result = await session.execute(stmt)
            people: List[Person] = results.scalars().fetchall()

        if not people:
            return json(dict())

        return json([row.to_dict() for row in people], default=str)

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
            person: Person = Person(**request.json)
            session.add_all([person])
        json_data: Dict[str, Any] = person.to_dict()
        return json(json_data, default=str)


bp_person = Blueprint("people", url_prefix="/people/")
bp_person.add_route(PersonView.as_view(), '/<pk:str>')
bp_person.add_route(PeopleView.as_view(), '/')
