import data_types.data_types as t
import models.models as m
from math import ceil
from queries.queries import (
    query_person_address, query_person_email, query_person_phone, query_person, query_person_membership, query_gender,
    query_membership_fee_category, query_address_type, query_email_type, query_phone_type, query_people_count
)
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, HTTPResponse
from sanic.views import HTTPMethodView
from sqlalchemy import update
from sqlalchemy.engine import Result, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.dml import Update


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
            person_stmt: Select = query_person.where(m.Person.id == pk)
            person_result: Result = await session.execute(person_stmt)
            person: Row = person_result.first()

            address_stmt: Select = query_person_address.where(m.Address.person_id == pk)
            address_result: Result = await session.execute(address_stmt)

            email_stmt: Select = query_person_email.where(m.Email.person_id == pk)
            email_result: Result = await session.execute(email_stmt)

            phone_stmt: Select = query_person_phone.where(m.Phone.person_id == pk)
            phone_result: Result = await session.execute(phone_stmt)

            membership_stmt: Select = query_person_membership.where(m.Membership.person_id == pk)
            membership_result: Result = await session.execute(membership_stmt)

            gender_type_result: Result = await session.execute(query_gender)
            membership_fee_type_result: Result = await session.execute(query_membership_fee_category)
            address_type_result: Result = await session.execute(query_address_type)
            email_type_result: Result = await session.execute(query_email_type)
            phone_type_result: Result = await session.execute(query_phone_type)

        if not person:
            return json({
                "person": dict(),
                "address": list(),
                "email": list(),
                "phone": list(),
                "membership": list(),
                "gender_type": list(),
                "membership_fee_type": list(),
                "address_type": list(),
                "email_type": list(),
                "phone_type": list(),
            })

        result_dict: t.PersonResult = {
            "person": dict(person),
            "address": list(map(dict, address_result)),
            "email": list(map(dict, email_result)),
            "phone": list(map(dict, phone_result)),
            "membership": list(map(dict, membership_result)),
            "gender_type": list(map(dict, gender_type_result)),
            "membership_fee_type": list(map(dict, membership_fee_type_result)),
            "address_type": list(map(dict, address_type_result)),
            "email_type": list(map(dict, email_type_result)),
            "phone_type": list(map(dict, phone_type_result)),
        }

        return json(result_dict, default=str)

    @staticmethod
    async def patch(request: Request, pk: str) -> HTTPResponse:
        """
        Alter specific person entry in database.

        :param request: `Request` object
        :param pk: primary key of person table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        payload: t.PersonResult = request.json
        async with session.begin():
            person_stmt: Update = update(m.Person).where(m.Person.id == pk).values(**payload['person'])
            await session.execute(person_stmt)

            for item in payload['address']:
                address_stmt: Update = update(m.Address).where(m.Address.id == pk).values(**item)
                await session.execute(address_stmt)
            for item in payload['email']:
                email_stmt: Update = update(m.Email).where(m.Email.id == pk).values(**item)
                await session.execute(email_stmt)
            for item in payload['phone']:
                phone_stmt: Update = update(m.Phone).where(m.Phone.id == pk).values(**item)
                await session.execute(phone_stmt)
            for item in payload['membership']:
                membership_stmt: Update = update(m.Membership).where(m.Membership.id == pk).values(**item)
                await session.execute(membership_stmt)

        async with session.begin():
            person_stmt: Select = query_person.where(m.Person.id == pk)
            person_result: Result = await session.execute(person_stmt)
            person: Row = person_result.first()

            address_stmt: Select = query_person_address.where(m.Address.person_id == pk)
            address_result: Result = await session.execute(address_stmt)

            email_stmt: Select = query_person_email.where(m.Email.person_id == pk)
            email_result: Result = await session.execute(email_stmt)

            phone_stmt: Select = query_person_phone.where(m.Phone.person_id == pk)
            phone_result: Result = await session.execute(phone_stmt)

            membership_stmt: Select = query_person_membership.where(m.Membership.person_id == pk)
            membership_result: Result = await session.execute(membership_stmt)

            gender_type_result: Result = await session.execute(query_gender)
            membership_fee_type_result: Result = await session.execute(query_membership_fee_category)
            address_type_result: Result = await session.execute(query_address_type)
            email_type_result: Result = await session.execute(query_email_type)
            phone_type_result: Result = await session.execute(query_phone_type)

        if not person:
            return json({
                "person": dict(),
                "address": list(),
                "email": list(),
                "phone": list(),
                "membership": list(),
                "gender_type": list(),
                "membership_fee_type": list(),
                "address_type": list(),
                "email_type": list(),
                "phone_type": list(),
            })

        result_dict: t.PersonResult = {
            "person": dict(person),
            "address": list(map(dict, address_result)),
            "email": list(map(dict, email_result)),
            "phone": list(map(dict, phone_result)),
            "membership": list(map(dict, membership_result)),
            "gender_type": list(map(dict, gender_type_result)),
            "membership_fee_type": list(map(dict, membership_fee_type_result)),
            "address_type": list(map(dict, address_type_result)),
            "email_type": list(map(dict, email_type_result)),
            "phone_type": list(map(dict, phone_type_result)),
        }

        return json(result_dict, default=str)


class PeopleView(HTTPMethodView):

    @staticmethod
    async def get(request: Request) -> HTTPResponse:
        """
        Gets person collection from database.

        :param request: `Request` object
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        page = int(request.args.get('page', 0))
        page_size = int(request.args.get("page_size", 20))
        query = query_person.limit(page_size).offset(page_size * page)
        async with session.begin():
            results: Result = await session.execute(query)
            row_count_result: Result = await session.execute(query_people_count)
            row_count: int = row_count_result.scalar()
        return json({
            "people": list(map(dict, results)),
            "page": page,
            "page_size": page_size,
            "row_count": row_count,
            "page_count": ceil(row_count / page_size)
        }, default=str)

    @staticmethod
    async def post(request: Request) -> HTTPResponse:
        """
        Inserts the provided JSON payload to corresponding table.

        :param request: `Request` object
        :return: JSON with id and timestamp
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            person: m.Person = m.Person(**request.json)
            session.add_all([person])
        json_data: t.Person = person.to_dict()
        return json(json_data, default=str)


bp_person = Blueprint("people", url_prefix="/people/")
bp_person.add_route(PersonView.as_view(), '/<pk:str>')
bp_person.add_route(PeopleView.as_view(), '/')
