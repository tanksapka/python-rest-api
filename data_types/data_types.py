import datetime
from typing import Optional, TypedDict


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


class PersonAddressDataType(TypedDict):
    id: str
    person_id: str
    address_type_id: str
    zip: str
    city: str
    address_1: str
    address_2: Optional[str]


class OrganizationAddressDataType(TypedDict):
    id: str
    organization_id: str
    address_type_id: str
    address_type_name: str
    zip: str
    city: str
    address_1: str
    address_2: Optional[str]


class PersonEmailDataType(TypedDict):
    id: str
    person_id: str
    email_type_id: str
    email: str
    messenger: str
    skype: str


class OrganizationEmailDataType(TypedDict):
    id: str
    organization_id: str
    email_type_id: str
    email_type_name: str
    email: str
    messenger: str
    skype: str


class PersonPhoneDataType(TypedDict):
    id: str
    person_id: str
    phone_type_id: str
    phone: str
    phone_extension: Optional[str]
    messenger: str
    skype: str
    viber: str
    whatsapp: str


class OrganizationPhoneDataType(TypedDict):
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


class PersonMembershipDataType(TypedDict):
    id: str
    person_id: str
    organization_id: str
    organization_name: str
    active_flag: str
    inactivity_status_id: Optional[int]
    event_date: datetime.date
    notes: Optional[str]


class OrganizationMembershipDataType(TypedDict):
    id: str
    person_id: str
    person_name: str
    organization_id: str
    active_flag: str
    inactivity_status_id: Optional[int]
    event_date: datetime.date
    notes: Optional[str]


class GenderTypeType(TypedDict):
    value: str
    label: str


class MembershipFeeCategoryType(TypedDict):
    value: str
    label: str


class AddressTypeType(TypedDict):
    value: str
    label: str


class EmailTypeType(TypedDict):
    value: str
    label: str


class PhoneTypeType(TypedDict):
    value: str
    label: str