from data_types.data_types import (
    OrganizationAddressDataType, OrganizationEmailDataType, OrganizationPhoneDataType, OrganizationMembershipDataType,
    OrganizationDataType, AddressTypeType, EmailTypeType, PhoneTypeType, ParentOrganizationsType
)
from math import ceil
from models.models import Address, Email, Membership, Organization, Phone
from queries.queries import (
    query_organization_address, query_organization_email, query_organization_phone, query_organization_membership,
    query_organization, query_address_type, query_email_type, query_phone_type, query_organization_count,
    query_parent_organizations
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
from typing import Any, Dict, List, TypedDict, Optional


class OrganizationResultType(TypedDict):
    organization: OrganizationDataType
    address: List[OrganizationAddressDataType]
    email: List[OrganizationEmailDataType]
    phone: List[OrganizationPhoneDataType]
    membership: List[OrganizationMembershipDataType]
    parent_organizations: List[ParentOrganizationsType]
    address_type: List[AddressTypeType]
    email_type: List[EmailTypeType]
    phone_type: List[PhoneTypeType]


class OrganizationDataJavaScriptType(TypedDict):
    organization_name: str
    parent_organization_id: str
    parent_organization_name: str
    description: Optional[str]
    accepts_members_flag: str
    establishment_date: str
    termination_date: Optional[str]
    notes: Optional[str]


class OrganizationAddressDataJavaScriptType(TypedDict):
    address_type_id: str
    address_type_name: str
    zip: str
    city: str
    address_1: str
    address_2: Optional[str]


class OrganizationEmailDataJavaScriptType(TypedDict):
    email_type_id: str
    email_type_name: str
    email: str
    messenger: str
    skype: str


class OrganizationPhoneDataJavaScriptType(TypedDict):
    phone_type_id: str
    phone_type_name: str
    phone: str
    phone_extension: Optional[str]
    messenger: str
    skype: str
    viber: str
    whatsapp: str


def process_organization_data(data: OrganizationDataJavaScriptType) -> OrganizationDataType:
    pass


def process_address_data(data: List[OrganizationAddressDataJavaScriptType]) -> List[OrganizationAddressDataType]:
    pass


def process_email_data(data: List[OrganizationEmailDataJavaScriptType]) -> List[OrganizationEmailDataType]:
    pass


def process_phone_data(data: List[OrganizationPhoneDataJavaScriptType]) -> List[OrganizationPhoneDataType]:
    pass


# TODO: make type names shorter and move them to data types module
# TODO: check optional settings
# TODO: cross-check types with TypeScript types


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

            address_stmt: Select = query_organization_address.where(Address.organization_id == pk)
            address_result: Result = await session.execute(address_stmt)

            email_stmt: Select = query_organization_email.where(Email.organization_id == pk)
            email_result: Result = await session.execute(email_stmt)

            phone_stmt: Select = query_organization_phone.where(Phone.organization_id == pk)
            phone_result: Result = await session.execute(phone_stmt)

            membership_stmt: Select = query_organization_membership.where(Membership.organization_id == pk)
            membership_result: Result = await session.execute(membership_stmt)

            parent_organizations: Result = await session.execute(query_parent_organizations)
            address_type_result: Result = await session.execute(query_address_type)
            email_type_result: Result = await session.execute(query_email_type)
            phone_type_result: Result = await session.execute(query_phone_type)

        if not organization:
            return json({
                "organization": dict(),
                "address": list(),
                "email": list(),
                "phone": list(),
                "membership": list(),
                "parent_organizations": list(),
                "address_type": list(),
                "email_type": list(),
                "phone_type": list(),
            })

        result_dict: OrganizationResultType = {
            "organization": dict(organization),
            "address": list(map(dict, address_result)),
            "email": list(map(dict, email_result)),
            "phone": list(map(dict, phone_result)),
            "membership": list(map(dict, membership_result)),
            "parent_organizations": list(map(dict, parent_organizations)),
            "address_type": list(map(dict, address_type_result)),
            "email_type": list(map(dict, email_type_result)),
            "phone_type": list(map(dict, phone_type_result)),
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

            address_stmt: Select = query_organization_address.where(Address.organization_id == pk)
            address_result: Result = await session.execute(address_stmt)

            email_stmt: Select = query_organization_email.where(Email.organization_id == pk)
            email_result: Result = await session.execute(email_stmt)

            phone_stmt: Select = query_organization_phone.where(Phone.organization_id == pk)
            phone_result: Result = await session.execute(phone_stmt)

            membership_stmt: Select = query_organization_membership.where(Membership.organization_id == pk)
            membership_result: Result = await session.execute(membership_stmt)

            parent_organizations: Result = await session.execute(query_parent_organizations)
            address_type_result: Result = await session.execute(query_address_type)
            email_type_result: Result = await session.execute(query_email_type)
            phone_type_result: Result = await session.execute(query_phone_type)

        if not organization:
            return json({
                "organization": dict(),
                "address": list(),
                "email": list(),
                "phone": list(),
                "membership": list(),
                "parent_organizations": list(),
                "address_type": list(),
                "email_type": list(),
                "phone_type": list(),
            })

        result_dict: OrganizationResultType = {
            "organization": dict(organization),
            "address": list(map(dict, address_result)),
            "email": list(map(dict, email_result)),
            "phone": list(map(dict, phone_result)),
            "membership": list(map(dict, membership_result)),
            "parent_organizations": list(map(dict, parent_organizations)),
            "address_type": list(map(dict, address_type_result)),
            "email_type": list(map(dict, email_type_result)),
            "phone_type": list(map(dict, phone_type_result)),
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
        page = int(request.args.get('page', 0))
        page_size = int(request.args.get("page_size", 20))
        query = query_organization.limit(page_size).offset(page_size * page)
        async with session.begin():
            results: Result = await session.execute(query)
            row_count_result: Result = await session.execute(query_organization_count)
            row_count: int = row_count_result.scalar()
        return json({
            "organizations": list(map(dict, results)),
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
            organization: Organization = Organization(**request.json)
            session.add_all([organization])
        json_data: Dict[str, Any] = organization.to_dict()
        return json(json_data, default=str)


bp_organization = Blueprint("organizations", url_prefix="/organizations/")
bp_organization.add_route(OrganizationView.as_view(), '/<pk:str>')
bp_organization.add_route(OrganizationsView.as_view(), '/')
