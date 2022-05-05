import datetime
import uuid
from models.models import AddressType, EmailType, Gender, MembershipFeeCategory, PhoneType
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, HTTPResponse
from sanic.views import HTTPMethodView
from sqlalchemy import select, update
from sqlalchemy.dialects.sqlite import insert, Insert
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.dml import Update
from typing import Any, Dict, List, Optional, TypedDict


class MapJavaScriptType(TypedDict):
    id: Optional[str]
    created_on: str
    created_by: str
    name: str
    description: Optional[str]
    valid_flag: str


class MapPythonType(TypedDict):
    id: str
    created_on: datetime.datetime
    created_by: str
    name: str
    description: str
    valid_flag: str


def process_map_item(map_item: MapJavaScriptType) -> MapPythonType:
    map_item.setdefault('id', str(uuid.uuid1()))
    return {
        k: v if k != 'created_on' else datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ')
        for k, v in map_item.items()
    }


class GenderView(HTTPMethodView):
    DBObject: Gender = Gender

    async def get(self, request: Request, pk: str) -> HTTPResponse:
        """
        Gets gender data based on provided id (pk).

        :param request: `Request` object
        :param pk: primary key of gender table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            stmt: Select = select(self.DBObject).where(self.DBObject.id == pk)
            result: Result = await session.execute(stmt)
            gender: GenderView.DBObject = result.scalar()

        if not gender:
            return json(dict())

        return json(gender.to_dict(), default=str)

    async def patch(self, request: Request, pk: str) -> HTTPResponse:
        """
        Alter specific gender entry in database.

        :param request: `Request` object
        :param pk: primary key of gender table
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        payload: Dict[str, Any] = {k: v for k, v in request.json.items() if k not in ['id', 'created_on', 'created_by']}
        async with session.begin():
            stmt: Update = update(self.DBObject).where(self.DBObject.id == pk).values(**payload)
            await session.execute(stmt)
        async with session.begin():
            stmt: Select = select(self.DBObject).where(self.DBObject.id == pk)
            result: Result = await session.execute(stmt)
            gender: GenderView.DBObject = result.scalar()
        return json(gender.to_dict(), default=str)


class GendersView(HTTPMethodView):
    DBObject: Gender = Gender

    async def get(self, request: Request) -> HTTPResponse:
        """
        Gets gender collection from database.

        :param request: `Request` object
        :return: JSON object with results
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            stmt: Select = select(self.DBObject)
            results: Result = await session.execute(stmt)
            genders: List[GenderView.DBObject] = results.scalars().fetchall()

        if not genders:
            return json(dict())

        return json([row.to_dict() for row in genders], default=str)

    async def post(self, request: Request) -> HTTPResponse:
        """
        Inserts the provided JSON payload to corresponding table.

        :param request: `Request` object
        :return: JSON with id and timestamp
        """
        session: AsyncSession = request.ctx.session
        items: List[MapPythonType] = [process_map_item(row) for row in request.json.get('data', [])]
        async with session.begin():
            for item in items:
                upsert_stmt: Insert = insert(self.DBObject).values(item).on_conflict_do_update(
                    index_elements=['id'], set_=item
                )
                # print(upsert_stmt, type(upsert_stmt), item, sep='\n')
                result = await session.execute(upsert_stmt)
                # print(result)
        # print(items)
        return json(items, default=str)


class MembershipFeeCategoryView(GenderView):
    DBObject: MembershipFeeCategory = MembershipFeeCategory

    async def get(self, request: Request, pk: str) -> HTTPResponse:
        """
        Gets membership fee category data based on provided id (pk).

        :param request: `Request` object
        :param pk: primary key of membership fee category table
        :return: JSON object with results
        """
        return await super().get(request, pk)

    async def patch(self, request: Request, pk: str) -> HTTPResponse:
        """
        Alter specific membership fee category entry in database.

        :param request: `Request` object
        :param pk: primary key of membership fee category table
        :return: JSON object with results
        """
        return await super().patch(request, pk)


class MembershipFeeCategoriesView(GendersView):
    DBObject: MembershipFeeCategory = MembershipFeeCategory

    async def get(self, request: Request) -> HTTPResponse:
        """
        Gets membership fee category collection from database.

        :param request: `Request` object
        :return: JSON object with results
        """
        return await super().get(request)

    async def post(self, request: Request) -> HTTPResponse:
        """
        Inserts the provided JSON payload to corresponding table.

        :param request: `Request` object
        :return: JSON with id and timestamp
        """
        return await super().post(request)


class AddressTypeView(GenderView):
    DBObject: AddressType = AddressType

    async def get(self, request: Request, pk: str) -> HTTPResponse:
        """
        Gets address type data based on provided id (pk).

        :param request: `Request` object
        :param pk: primary key of address type table
        :return: JSON object with results
        """
        return await super().get(request, pk)

    async def patch(self, request: Request, pk: str) -> HTTPResponse:
        """
        Alter specific address type entry in database.

        :param request: `Request` object
        :param pk: primary key of address type table
        :return: JSON object with results
        """
        return await super().patch(request, pk)


class AddressTypesView(GendersView):
    DBObject: AddressType = AddressType

    async def get(self, request: Request) -> HTTPResponse:
        """
        Gets address type collection from database.

        :param request: `Request` object
        :return: JSON object with results
        """
        return await super().get(request)

    async def post(self, request: Request) -> HTTPResponse:
        """
        Inserts the provided JSON payload to corresponding table.

        :param request: `Request` object
        :return: JSON with id and timestamp
        """
        return await super().post(request)


class PhoneTypeView(GenderView):
    DBObject: PhoneType = PhoneType

    async def get(self, request: Request, pk: str) -> HTTPResponse:
        """
        Gets phone type data based on provided id (pk).

        :param request: `Request` object
        :param pk: primary key of phone type table
        :return: JSON object with results
        """
        return await super().get(request, pk)

    async def patch(self, request: Request, pk: str) -> HTTPResponse:
        """
        Alter specific phone type entry in database.

        :param request: `Request` object
        :param pk: primary key of phone type table
        :return: JSON object with results
        """
        return await super().patch(request, pk)


class PhoneTypesView(GendersView):
    DBObject: PhoneType = PhoneType

    async def get(self, request: Request) -> HTTPResponse:
        """
        Gets phone type collection from database.

        :param request: `Request` object
        :return: JSON object with results
        """
        return await super().get(request)

    async def post(self, request: Request) -> HTTPResponse:
        """
        Inserts the provided JSON payload to corresponding table.

        :param request: `Request` object
        :return: JSON with id and timestamp
        """
        return await super().post(request)


class EmailTypeView(GenderView):
    DBObject: EmailType = EmailType

    async def get(self, request: Request, pk: str) -> HTTPResponse:
        """
        Gets email type data based on provided id (pk).

        :param request: `Request` object
        :param pk: primary key of email type table
        :return: JSON object with results
        """
        return await super().get(request, pk)

    async def patch(self, request: Request, pk: str) -> HTTPResponse:
        """
        Alter specific email type entry in database.

        :param request: `Request` object
        :param pk: primary key of email type table
        :return: JSON object with results
        """
        return await super().patch(request, pk)


class EmailTypesView(GendersView):
    DBObject: EmailType = EmailType

    async def get(self, request: Request) -> HTTPResponse:
        """
        Gets email type collection from database.

        :param request: `Request` object
        :return: JSON object with results
        """
        return await super().get(request)

    async def post(self, request: Request) -> HTTPResponse:
        """
        Inserts the provided JSON payload to corresponding table.

        :param request: `Request` object
        :return: JSON with id and timestamp
        """
        return await super().post(request)


bp_gender = Blueprint("genders", url_prefix="/genders/")
bp_gender.add_route(GenderView.as_view(), '/<pk:str>')
bp_gender.add_route(GendersView.as_view(), '/')

bp_membership_fee_category = Blueprint("membership_fee_categories", url_prefix="/membership-fee-categories/")
bp_membership_fee_category.add_route(MembershipFeeCategoryView.as_view(), "/<pk:str>")
bp_membership_fee_category.add_route(MembershipFeeCategoriesView.as_view(), "/")

bp_address_type = Blueprint("address_types", url_prefix="/address-types/")
bp_address_type.add_route(AddressTypeView.as_view(), "/<pk:str>")
bp_address_type.add_route(AddressTypesView.as_view(), "/")

bp_phone_type = Blueprint("phone_types", url_prefix="/phone-types/")
bp_phone_type.add_route(PhoneTypeView.as_view(), "/<pk:str>")
bp_phone_type.add_route(PhoneTypesView.as_view(), "/")

bp_email_type = Blueprint("email_types", url_prefix="/email-types/")
bp_email_type.add_route(EmailTypeView.as_view(), "/<pk:str>")
bp_email_type.add_route(EmailTypesView.as_view(), "/")
