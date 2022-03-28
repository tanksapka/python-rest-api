from models.models import (
    Address, AddressType, Email, EmailType, Gender, MembershipFeeCategory, Person, Phone, PhoneType
)
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, HTTPResponse
from sanic.views import HTTPMethodView
from sqlalchemy import select, update
from sqlalchemy.engine import Result, Row
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
            person_stmt: Select = select(
                Person.id,
                Person.registration_number,
                Person.membership_id,
                Person.name.label('person_name'),
                Person.birthdate,
                Person.mother_name,
                Person.gender_id,
                Gender.name.label('gender_name'),
                Person.identity_card_number,
                Person.membership_fee_category_id,
                MembershipFeeCategory.name.label('membership_fee_category_name'),
                Person.notes,
            ).join(Gender).join(MembershipFeeCategory).where(Person.id == pk)
            person_result: Result = await session.execute(person_stmt)
            person: Row = person_result.first()

            address_stmt: Select = select(
                Address.id,
                Address.person_id,
                Address.address_type_id,
                AddressType.name.label('address_type_name'),
                Address.zip,
                Address.city,
                Address.address_1,
                Address.address_2,
            ).join(AddressType).where(Address.person_id == pk)
            address_result: Result = await session.execute(address_stmt)

            email_stmt: Select = select(
                Email.id,
                Email.person_id,
                Email.email_type_id,
                EmailType.name.label('email_type_name'),
                Email.email,
                Email.messenger,
                Email.skype,
            ).join(EmailType).where(Email.person_id == pk)
            email_result: Result = await session.execute(email_stmt)

            phone_stmt: Select = select(
                Phone.id,
                Phone.person_id,
                Phone.phone_type_id,
                PhoneType.name.label('phone_type_name'),
                Phone.phone_number,
                Phone.phone_extension,
                Phone.messenger,
                Phone.skype,
                Phone.viber,
                Phone.whatsapp,
            ).join(PhoneType).where(Phone.person_id == pk)
            phone_result: Result = await session.execute(phone_stmt)

        if not person:
            return json({
                "person": dict(),
                "address": list(),
                "email": list(),
                "phone": list(),
            })

        return json({
            "person": dict(person),
            "address": tuple(map(dict, address_result)),
            "email": tuple(map(dict, email_result)),
            "phone": tuple(map(dict, phone_result)),
        }, default=str)

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
        async with session.begin():
            person: Person = Person(**request.json)
            session.add_all([person])
        json_data: Dict[str, Any] = person.to_dict()
        return json(json_data, default=str)


bp_person = Blueprint("people", url_prefix="/people/")
bp_person.add_route(PersonView.as_view(), '/<pk:str>')
bp_person.add_route(PeopleView.as_view(), '/')
