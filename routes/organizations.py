import datetime
from models.models import Address, AddressType, Email, EmailType, Membership, Organization, Person, Phone, PhoneType
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, HTTPResponse
from sanic.views import HTTPMethodView
from sqlalchemy import select, update
from sqlalchemy.engine import Result, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.dml import Update
from typing import Any, Dict, List, Optional, TypedDict


class OrganizationDataType(TypedDict):
    id: str
    organization_name: str
    parent_organization_id: str
    parent_organization_name: str
    description: str
    accepts_members_flag: str
    establishment_date: str
    termination_date: datetime.date
    notes: str


class AddressDataType(TypedDict):
    id: str
    organization_id: str
    address_type_id: str
    address_type_name: str
    zip: str
    city: str
    address_1: str
    address_2: Optional[str]


class EmailDataType(TypedDict):
    id: str
    organization_id: str
    email_type_id: str
    email_type_name: str
    email: str
    messenger: str
    skype: str


class PhoneDataType(TypedDict):
    id: str
    organization_id: str
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
    person_name: str
    organization_id: str
    active_flag: str
    inactivity_status_id: Optional[int]
    event_date: datetime.date
    notes: Optional[str]


class OrganizationResultType(TypedDict):
    organization: OrganizationDataType
    address: List[AddressDataType]
    email: List[EmailDataType]
    phone: List[PhoneDataType]
    membership: List[MembershipDataType]


parent_organization: AliasedClass = aliased(Organization, name='parent_org')
query_organization: Select = select(
    Organization.id,
    Organization.name.label('organization_name'),
    parent_organization.id.label('parent_organization_id'),
    parent_organization.name.label('parent_organization_name'),
    Organization.description,
    Organization.accepts_members_flag,
    Organization.establishment_date,
    Organization.termination_date,
    Organization.notes,
).join(parent_organization, onclause=Organization.organization_parent_id == parent_organization.id)


query_address: Select = select(
    Address.id,
    Address.organization_id,
    Address.address_type_id,
    AddressType.name.label('address_type_name'),
    Address.zip,
    Address.city,
    Address.address_1,
    Address.address_2,
).join(AddressType)


query_email: Select = select(
    Email.id,
    Email.organization_id,
    Email.email_type_id,
    EmailType.name.label('email_type_name'),
    Email.email,
    Email.messenger,
    Email.skype,
).join(EmailType)


query_phone: Select = select(
    Phone.id,
    Phone.organization_id,
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
    Person.name.label('person_name'),
    Membership.organization_id,
    Membership.active_flag,
    Membership.inactivity_status_id,
    Membership.event_date,
    Membership.notes,
).join(Person)


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
            organization_stmt: Select = query_organization.where(Organization.id == pk)
            organization_result: Result = await session.execute(organization_stmt)
            organization: Row = organization_result.first()

            address_stmt: Select = query_address.where(Address.organization_id == pk)
            address_result: Result = await session.execute(address_stmt)

            email_stmt: Select = query_email.where(Email.organization_id == pk)
            email_result: Result = await session.execute(email_stmt)

            phone_stmt: Select = query_phone.where(Phone.organization_id == pk)
            phone_result: Result = await session.execute(phone_stmt)

            membership_stmt: Select = query_membership.where(Membership.organization_id == pk)
            membership_result: Result = await session.execute(membership_stmt)

        if not organization:
            return json({
                "organization": dict(),
                "address": list(),
                "email": list(),
                "phone": list(),
                "membership": list(),
            })

        result_dict: OrganizationResultType = {
            "organization": dict(organization),
            "address": list(map(dict, address_result)),
            "email": list(map(dict, email_result)),
            "phone": list(map(dict, phone_result)),
            "membership": list(map(dict, membership_result)),
        }

        return json(result_dict, default=str)

    @staticmethod
    async def patch(request: Request, pk: str) -> HTTPResponse:
        """
        Alter specific organization entry in database.

        :param request: `Request` object
        :param pk: primary key of organization table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        payload: OrganizationResultType = request.json
        async with session.begin():
            organization_stmt: Update = update(Organization).where(Organization.id == pk).values(
                **payload['organization']
            )
            await session.execute(organization_stmt)

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
            organization_stmt: Select = query_organization.where(Organization.id == pk)
            organization_result: Result = await session.execute(organization_stmt)
            organization: Row = organization_result.first()

            address_stmt: Select = query_address.where(Address.organization_id == pk)
            address_result: Result = await session.execute(address_stmt)

            email_stmt: Select = query_email.where(Email.organization_id == pk)
            email_result: Result = await session.execute(email_stmt)

            phone_stmt: Select = query_phone.where(Phone.organization_id == pk)
            phone_result: Result = await session.execute(phone_stmt)

            membership_stmt: Select = query_membership.where(Membership.organization_id == pk)
            membership_result: Result = await session.execute(membership_stmt)

        if not organization:
            return json({
                "organization": dict(),
                "address": list(),
                "email": list(),
                "phone": list(),
                "membership": list(),
            })

        result_dict: OrganizationResultType = {
            "organization": dict(organization),
            "address": list(map(dict, address_result)),
            "email": list(map(dict, email_result)),
            "phone": list(map(dict, phone_result)),
            "membership": list(map(dict, membership_result)),
        }

        return json(result_dict, default=str)


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
            results: Result = await session.execute(query_organization)
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
            organization: Organization = Organization(**request.json)
            session.add_all([organization])
        json_data: Dict[str, Any] = organization.to_dict()
        return json(json_data, default=str)


bp_organization = Blueprint("organizations", url_prefix="/organizations/")
bp_organization.add_route(OrganizationView.as_view(), '/<pk:str>')
bp_organization.add_route(OrganizationsView.as_view(), '/')
