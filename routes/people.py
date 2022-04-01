import datetime
from models.models import (
    Address, AddressType, Email, EmailType, Gender, Membership, MembershipFeeCategory, Organization, Person, Phone,
    PhoneType
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
from typing import List, Optional, TypedDict


class PersonDataType(TypedDict):
    id: str
    registration_number: int
    membership_id: str
    person_name: str
    birthdate: datetime.date
    mother_name: str
    gender_id: str
    gender_name: str
    identity_card_number: str
    membership_fee_category_id: str
    membership_fee_category_name: str
    notes: Optional[str]


class AddressDataType(TypedDict):
    id: str
    person_id: str
    address_type_id: str
    address_type_name: str
    zip: str
    city: str
    address_1: str
    address_2: Optional[str]


class EmailDataType(TypedDict):
    id: str
    person_id: str
    email_type_id: str
    email_type_name: str
    email: str
    messenger: str
    skype: str


class PhoneDataType(TypedDict):
    id: str
    person_id: str
    phone_type_id: str
    phone_type_name: str
    phone: str
    phone_extension: Optional[str]
    messenger: str
    skype: str
    viber: str
    whatsapp: str


class MembershipDataType(TypedDict):
    id: str
    person_id: str
    organization_id: str
    organization_name: str
    active_flag: str
    inactivity_status_id: Optional[int]
    event_date: datetime.date
    notes: Optional[str]


class PersonResultType(TypedDict):
    person: PersonDataType
    address: List[AddressDataType]
    email: List[EmailDataType]
    phone: List[PhoneDataType]
    membership: List[MembershipDataType]


query_person: Select = select(
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
).join(Gender).join(MembershipFeeCategory)


query_address: Select = select(
    Address.id,
    Address.person_id,
    Address.address_type_id,
    AddressType.name.label('address_type_name'),
    Address.zip,
    Address.city,
    Address.address_1,
    Address.address_2,
).join(AddressType)


query_email: Select = select(
    Email.id,
    Email.person_id,
    Email.email_type_id,
    EmailType.name.label('email_type_name'),
    Email.email,
    Email.messenger,
    Email.skype,
).join(EmailType)


query_phone: Select = select(
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
).join(PhoneType)


query_membership: Select = select(
    Membership.id,
    Membership.person_id,
    Membership.organization_id,
    Organization.name.label('organization_name'),
    Membership.active_flag,
    Membership.inactivity_status_id,
    Membership.event_date,
    Membership.notes,
).join(Organization)


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
            person_stmt: Select = query_person.where(Person.id == pk)
            person_result: Result = await session.execute(person_stmt)
            person: Row = person_result.first()

            address_stmt: Select = query_address.where(Address.person_id == pk)
            address_result: Result = await session.execute(address_stmt)

            email_stmt: Select = query_email.where(Email.person_id == pk)
            email_result: Result = await session.execute(email_stmt)

            phone_stmt: Select = query_phone.where(Phone.person_id == pk)
            phone_result: Result = await session.execute(phone_stmt)

            membership_stmt: Select = query_membership.where(Membership.person_id == pk)
            membership_result: Result = await session.execute(membership_stmt)

        if not person:
            return json({
                "person": dict(),
                "address": list(),
                "email": list(),
                "phone": list(),
                "membership": list(),
            })

        result_dict: PersonResultType = {
            "person": dict(person),
            "address": list(map(dict, address_result)),
            "email": list(map(dict, email_result)),
            "phone": list(map(dict, phone_result)),
            "membership": list(map(dict, membership_result)),
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
        payload: PersonResultType = request.json
        async with session.begin():
            person_stmt: Update = update(Person).where(Person.id == pk).values(**payload['person'])
            await session.execute(person_stmt)

            for item in payload['address']:
                address_stmt: Update = update(Address).where(Address.id == pk).values(**item)
                await session.execute(address_stmt)
            for item in payload['email']:
                email_stmt: Update = update(Email).where(Email.id == pk).values(**item)
                await session.execute(email_stmt)
            for item in payload['phone']:
                phone_stmt: Update = update(Phone).where(Phone.id == pk).values(**item)
                await session.execute(phone_stmt)
            for item in payload['membership']:
                membership_stmt: Update = update(Membership).where(Membership.id == pk).values(**item)
                await session.execute(membership_stmt)

        async with session.begin():
            person_stmt: Select = query_person.where(Person.id == pk)
            person_result: Result = await session.execute(person_stmt)
            person: Row = person_result.first()

            address_stmt: Select = query_address.where(Address.person_id == pk)
            address_result: Result = await session.execute(address_stmt)

            email_stmt: Select = query_email.where(Email.person_id == pk)
            email_result: Result = await session.execute(email_stmt)

            phone_stmt: Select = query_phone.where(Phone.person_id == pk)
            phone_result: Result = await session.execute(phone_stmt)

            membership_stmt: Select = query_membership.where(Membership.person_id == pk)
            membership_result: Result = await session.execute(membership_stmt)

        if not person:
            return json({
                "person": dict(),
                "address": list(),
                "email": list(),
                "phone": list(),
                "membership": list(),
            })

        result_dict: PersonResultType = {
            "person": dict(person),
            "address": list(map(dict, address_result)),
            "email": list(map(dict, email_result)),
            "phone": list(map(dict, phone_result)),
            "membership": list(map(dict, membership_result)),
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
        async with session.begin():
            results: Result = await session.execute(query_person)
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
            person: Person = Person(**request.json)
            session.add_all([person])
        json_data: PersonDataType = person.to_dict()
        return json(json_data, default=str)


bp_person = Blueprint("people", url_prefix="/people/")
bp_person.add_route(PersonView.as_view(), '/<pk:str>')
bp_person.add_route(PeopleView.as_view(), '/')
