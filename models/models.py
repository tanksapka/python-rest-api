import datetime
from sqlalchemy import INTEGER, NCHAR, NVARCHAR, DATE, DATETIME, TEXT, Column, CheckConstraint, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import create_engine
from typing import Any, Dict
from uuid import uuid4

Base = declarative_base()
sql_url = "sqlite:///:memory:"
db_engine = create_engine(sql_url, echo=True)


class BaseModel(Base):
    __abstract__ = True
    id = Column(NCHAR(36), primary_key=True, default=str(uuid4()))
    created_on = Column(DATETIME(), nullable=False, default=datetime.datetime.now())
    created_by = Column(NVARCHAR(50), nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class BaseMapModel(BaseModel):
    __abstract__ = True
    name = Column(NVARCHAR(255), unique=True, nullable=False)
    description = Column(NVARCHAR(255), nullable=True)
    valid_flag = Column(NCHAR(1), CheckConstraint("valid_flag in ('Y', 'N')", name='chk_valid_flag'), nullable=False)


class Gender(BaseMapModel):
    __tablename__ = "gender"


class MembershipFeeCategory(BaseMapModel):
    __tablename__ = "membership_fee_category"


class AddressType(BaseMapModel):
    __tablename__ = "address_type"


class PhoneType(BaseMapModel):
    __tablename__ = "phone_type"


class EmailType(BaseMapModel):
    __tablename__ = "email_type"


class Person(BaseModel):
    __tablename__ = 'person'
    registration_number = Column(INTEGER(), nullable=False)
    membership_id = Column(NVARCHAR(30), nullable=False)
    name = Column(NVARCHAR(255), nullable=False)
    birthdate = Column(DATE(), nullable=True)
    mother_name = Column(NVARCHAR(255), nullable=True)
    gender_id = Column(NCHAR(36), ForeignKey('gender.id', name='fk_person_gender_id'), nullable=True)
    identity_card_number = Column(NVARCHAR(50), nullable=True)
    membership_fee_category_id = Column(
        NCHAR(36), ForeignKey('membership_fee_category.id', name='fk_person_membership_fee_category_id'), nullable=False
    )
    notes = Column(TEXT(), nullable=True)


class Organization(BaseModel):
    __tablename__ = 'organization'
    organization_parent_id = Column(
        NCHAR(36), ForeignKey('organization.id', name='fk_organization_organization_id'), nullable=True
    )
    name = Column(NVARCHAR(255), nullable=False)
    description = Column(NVARCHAR(255), unique=True, nullable=True)
    accepts_members_flag = Column(
        NCHAR(1), CheckConstraint("accepts_members_flag in ('Y', 'N')", name='chk_accepts_members_flag'),
        nullable=False
    )
    establishment_date = Column(DATE(), nullable=False)
    termination_date = Column(DATE(), nullable=True)
    notes = Column(TEXT(), nullable=True)


class Address(BaseModel):
    __tablename__ = 'address'
    person_id = Column(NCHAR(36), ForeignKey('person.id', name='fk_address_person_id'), nullable=True)
    organization_id = Column(
        NCHAR(36), ForeignKey('organization.id', name='fk_address_organization_id'), nullable=True
    )
    address_type_id = Column(
        NCHAR(36), ForeignKey('address_type.id', name='fk_address_address_type_id'), nullable=False
    )
    zip = Column(NVARCHAR(255), nullable=False)
    city = Column(NVARCHAR(255), nullable=False)
    address_1 = Column(NVARCHAR(255), nullable=False)
    address_2 = Column(NVARCHAR(255), nullable=True)


class Phone(BaseModel):
    __tablename__ = "phone"
    person_id = Column(NCHAR(36), ForeignKey('person.id', name='fk_phone_person_id'), nullable=True)
    organization_id = Column(NCHAR(36), ForeignKey('organization.id', name='fk_phone_organization_id'), nullable=True)
    phone_type_id = Column(NCHAR(36), ForeignKey('phone_type.id', name='fk_phone_phone_type_id'), nullable=False)
    phone_number = Column(NVARCHAR(255), nullable=False)
    phone_extension = Column(NVARCHAR(255), nullable=True)
    messenger = Column(NCHAR(1), CheckConstraint("messenger in ('Y', 'N')", name='chk_messenger'), nullable=False)
    skype = Column(NCHAR(1), CheckConstraint("skype in ('Y', 'N')", name='chk_skype'), nullable=False)
    viber = Column(NCHAR(1), CheckConstraint("viber in ('Y', 'N')", name='chk_viber'), nullable=False)
    whatsapp = Column(NCHAR(1), CheckConstraint("whatsapp in ('Y', 'N')", name='chk_whatsapp'), nullable=False)


class Email(BaseModel):
    __tablename__ = "email"
    person_id = Column(NCHAR(36), ForeignKey('person.id', name='fk_email_person_id'), nullable=True)
    organization_id = Column(NCHAR(36), ForeignKey('organization.id', name='fk_email_organization_id'), nullable=True)
    email_type_id = Column(NCHAR(36), ForeignKey('email_type.id', name='fk_email_email_type_id'), nullable=False)
    email = Column(NVARCHAR(255), nullable=False)
    messenger = Column(NCHAR(1), CheckConstraint("messenger in ('Y', 'N')", name='chk_messenger'), nullable=False)
    skype = Column(NCHAR(1), CheckConstraint("skype in ('Y', 'N')", name='chk_skype'), nullable=False)


class Membership(BaseModel):
    __tablename__ = "membership"
    person_id = Column(NCHAR(36), ForeignKey('person.id', name='fk_email_person_id'), nullable=False)
    organization_id = Column(NCHAR(36), ForeignKey('organization.id', name='fk_email_organization_id'), nullable=False)
    active_flag = Column(NCHAR(1), CheckConstraint("active_flag in ('Y', 'N')", name='chk_active_flag'), nullable=False)
    inactivity_status_id = Column(NCHAR(36), nullable=True)
    event_date = Column(DATE(), nullable=False)
    notes = Column(TEXT(), nullable=True)


if __name__ == '__main__':
    print(Base.metadata.create_all(bind=db_engine))
