import datetime
from typing import Optional, List, TypedDict


class Person(TypedDict):
    person_id: str
    registration_number: int
    membership_id: str
    person_name: str
    birthdate: Optional[datetime.date]
    mother_name: Optional[str]
    gender_id: Optional[str]
    gender_name: Optional[str]
    identity_card_number: Optional[str]
    membership_fee_category_id: str
    membership_fee_category_name: str
    notes: Optional[str]


class Organization(TypedDict):
    organization_id: str
    organization_name: str
    parent_organization_id: str
    parent_organization_name: str
    description: str
    accepts_members_flag: str
    establishment_date: str
    termination_date: datetime.date
    notes: str


class OrganizationJS(TypedDict):
    """
    Incoming data type from frontend.
    """
    organization_name: str
    parent_organization_id: str
    parent_organization_name: str
    description: Optional[str]
    accepts_members_flag: str
    establishment_date: str
    termination_date: Optional[str]
    notes: Optional[str]


class PersonAddress(TypedDict):
    id: str
    person_id: str
    address_type_id: str
    zip: str
    city: str
    address_1: str
    address_2: Optional[str]


class OrganizationAddress(TypedDict):
    id: str
    organization_id: str
    address_type_id: str
    zip: str
    city: str
    address_1: str
    address_2: Optional[str]


class OrganizationAddressJS(TypedDict):
    """
    Incoming data type from frontend.
    """
    address_type_id: str
    address_type_name: str
    zip: str
    city: str
    address_1: str
    address_2: Optional[str]


class PersonEmail(TypedDict):
    id: str
    person_id: str
    email_type_id: str
    email: str
    messenger: str
    skype: str


class OrganizationEmail(TypedDict):
    id: str
    organization_id: str
    email_type_id: str
    email: str
    messenger: str
    skype: str


class OrganizationEmailJS(TypedDict):
    """
    Incoming data type from frontend.
    """
    email_type_id: str
    email_type_name: str
    email: str
    messenger: str
    skype: str


class PersonPhone(TypedDict):
    id: str
    person_id: str
    phone_type_id: str
    phone: str
    phone_extension: Optional[str]
    messenger: str
    skype: str
    viber: str
    whatsapp: str


class OrganizationPhone(TypedDict):
    id: str
    organization_id: str
    phone_type_id: str
    phone: str
    phone_extension: Optional[str]
    messenger: str
    skype: str
    viber: str
    whatsapp: str


class OrganizationPhoneJS(TypedDict):
    """
    Incoming data type from frontend.
    """
    phone_type_id: str
    phone_type_name: str
    phone: str
    phone_extension: Optional[str]
    messenger: str
    skype: str
    viber: str
    whatsapp: str


class PersonMembership(TypedDict):
    id: str
    person_id: str
    organization_id: str
    organization_name: str
    active_flag: str
    inactivity_status_id: Optional[int]
    event_date: datetime.date
    notes: Optional[str]


class OrganizationMembership(TypedDict):
    id: str
    person_id: str
    person_name: str
    organization_id: str
    active_flag: str
    inactivity_status_id: Optional[int]
    event_date: datetime.date
    notes: Optional[str]


class GenderType(TypedDict):
    value: str
    label: str


class MembershipFeeCategory(TypedDict):
    value: str
    label: str


class AddressType(TypedDict):
    value: str
    label: str


class EmailType(TypedDict):
    value: str
    label: str


class PhoneType(TypedDict):
    value: str
    label: str


class MapJS(TypedDict):
    """
    Incoming data type from frontend.
    """
    id: Optional[str]
    created_on: str
    created_by: str
    name: str
    description: Optional[str]
    valid_flag: str


class MapPython(TypedDict):
    """
    Native data to be sent to frontend.
    """
    id: str
    created_on: datetime.datetime
    created_by: str
    name: str
    description: str
    valid_flag: str


class ParentOrganization(TypedDict):
    organization_id: str
    organization_name: str


class PersonMapping(TypedDict):
    """
    Person related mapping types. Primary usage for new Person addition.
    """
    gender_type: List[GenderType]
    membership_fee_type: List[MembershipFeeCategory]
    address_type: List[AddressType]
    email_type: List[EmailType]
    phone_type: List[PhoneType]


class OrganizationMapping(TypedDict):
    """
    Organization related mapping types. Primary usage for new Organization addition.
    """
    parent_organizations: List[ParentOrganization]
    address_type: List[AddressType]
    email_type: List[EmailType]
    phone_type: List[PhoneType]


class Mapping(TypedDict):
    """
    Mapping types available for the whole app.
    """
    gender_type: List[MapPython]
    membership_fee_type: List[MapPython]
    address_type: List[MapPython]
    email_type: List[MapPython]
    phone_type: List[MapPython]


class PersonResult(TypedDict):
    person: Person
    address: List[PersonAddress]
    email: List[PersonEmail]
    phone: List[PersonPhone]
    membership: List[PersonMembership]
    gender_type: List[GenderType]
    membership_fee_type: List[MembershipFeeCategory]
    address_type: List[AddressType]
    email_type: List[EmailType]
    phone_type: List[PhoneType]


class OrganizationResult(TypedDict):
    organization: Organization
    address: List[OrganizationAddress]
    email: List[OrganizationEmail]
    phone: List[OrganizationPhone]
    membership: List[OrganizationMembership]
    parent_organizations: List[ParentOrganization]
    address_type: List[AddressType]
    email_type: List[EmailType]
    phone_type: List[PhoneType]
