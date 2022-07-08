from models.models import (
    Address, AddressType, Email, EmailType, Gender, Membership, MembershipFeeCategory, Organization, Person, Phone,
    PhoneType
)
from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.sql import and_
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.selectable import Select


query_person: Select = select(
    Person.id.label('person_id'),
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

query_people_count: count = count(Person.id)

parent_organization: AliasedClass = aliased(Organization, name='parent_org')
query_organization: Select = select(
    Organization.id.label('organization_id'),
    Organization.name.label('organization_name'),
    parent_organization.id.label('parent_organization_id'),
    parent_organization.name.label('parent_organization_name'),
    Organization.description,
    Organization.accepts_members_flag,
    Organization.establishment_date,
    Organization.termination_date,
    Organization.notes,
).join(parent_organization, isouter=True, onclause=Organization.organization_parent_id == parent_organization.id)

query_organization_count: count = count(Organization.id)

query_parent_organizations: Select = select(
    Organization.id.label('organization_id'),
    Organization.name.label('organization_name'),
).where(and_(Organization.organization_parent_id.is_(None), Organization.termination_date.is_(None)))

query_person_address: Select = select(
    Address.id,
    Address.person_id,
    Address.address_type_id,
    Address.zip,
    Address.city,
    Address.address_1,
    Address.address_2,
)

query_organization_address: Select = select(
    Address.id,
    Address.organization_id,
    Address.address_type_id,
    Address.zip,
    Address.city,
    Address.address_1,
    Address.address_2,
)

query_person_email: Select = select(
    Email.id,
    Email.person_id,
    Email.email_type_id,
    Email.email,
    Email.messenger,
    Email.skype,
)

query_organization_email: Select = select(
    Email.id,
    Email.organization_id,
    Email.email_type_id,
    Email.email,
    Email.messenger,
    Email.skype,
)

query_person_phone: Select = select(
    Phone.id,
    Phone.person_id,
    Phone.phone_type_id,
    Phone.phone_number,
    Phone.phone_extension,
    Phone.messenger,
    Phone.skype,
    Phone.viber,
    Phone.whatsapp,
)

query_organization_phone: Select = select(
    Phone.id,
    Phone.organization_id,
    Phone.phone_type_id,
    Phone.phone_number,
    Phone.phone_extension,
    Phone.messenger,
    Phone.skype,
    Phone.viber,
    Phone.whatsapp,
)

query_person_membership: Select = select(
    Membership.id,
    Membership.person_id,
    Membership.organization_id,
    Organization.name.label('organization_name'),
    Membership.active_flag,
    Membership.inactivity_status_id,
    Membership.event_date,
    Membership.notes,
).join(Organization)

query_organization_membership: Select = select(
    Membership.id,
    Membership.person_id,
    Person.name.label('person_name'),
    Membership.organization_id,
    Membership.active_flag,
    Membership.inactivity_status_id,
    Membership.event_date,
    Membership.notes,
).join(Person)

query_gender: Select = select(
    Gender.id.label('value'),
    Gender.name.label('label'),
).where(Gender.valid_flag == 'Y')

query_gender_map: Select = select(
    Gender.id,
    Gender.name,
    Gender.description,
    Gender.valid_flag,
    Gender.created_on,
    Gender.created_by,
)

query_membership_fee_category: Select = select(
    MembershipFeeCategory.id.label('value'),
    MembershipFeeCategory.name.label('label'),
).where(MembershipFeeCategory.valid_flag == 'Y')

query_membership_fee_category_map: Select = select(
    MembershipFeeCategory.id,
    MembershipFeeCategory.name,
    MembershipFeeCategory.description,
    MembershipFeeCategory.valid_flag,
    MembershipFeeCategory.created_on,
    MembershipFeeCategory.created_by,
)

query_address_type: Select = select(
    AddressType.id.label('value'),
    AddressType.name.label('label'),
).where(AddressType.valid_flag == 'Y')

query_address_type_map: Select = select(
    AddressType.id,
    AddressType.name,
    AddressType.description,
    AddressType.valid_flag,
    AddressType.created_on,
    AddressType.created_by,
)

query_email_type: Select = select(
    EmailType.id.label('value'),
    EmailType.name.label('label'),
).where(EmailType.valid_flag == 'Y')

query_email_type_map: Select = select(
    EmailType.id,
    EmailType.name,
    EmailType.description,
    EmailType.valid_flag,
    EmailType.created_on,
    EmailType.created_by,
)

query_phone_type: Select = select(
    PhoneType.id.label('value'),
    PhoneType.name.label('label'),
).where(PhoneType.valid_flag == 'Y')

query_phone_type_map: Select = select(
    PhoneType.id,
    PhoneType.name,
    PhoneType.description,
    PhoneType.valid_flag,
    PhoneType.created_on,
    PhoneType.created_by,
)
