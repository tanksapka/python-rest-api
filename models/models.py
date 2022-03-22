from sqlalchemy import INTEGER, NCHAR, NVARCHAR, DATE, DATETIME, TEXT, Column, CheckConstraint, UniqueConstraint,\
    PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import create_engine

Base = declarative_base()
sql_url = "sqlite:///:memory:"
db_engine = create_engine(sql_url, echo=True)


class BaseModel(Base):
    __abstract__ = True
    __tablename__ = 'base'
    id = Column(NCHAR(36), primary_key=True)
    created_on = Column(DATETIME(), nullable=False)
    created_by = Column(NVARCHAR(50), nullable=False)
    PrimaryKeyConstraint(id, name=f'pk_{__tablename__}')


class Gender(BaseModel):
    __tablename__ = "gender"
    name = Column(NVARCHAR(255), nullable=False)
    description = Column(NVARCHAR(255), nullable=True)
    valid_flag = Column(NCHAR(1), nullable=False)
    UniqueConstraint('description', name=f'uq_{__tablename__}')
    CheckConstraint("valid_flag in ('Y', 'N')", name=f'chk_{valid_flag.name}')


class Person(BaseModel):
    __tablename__ = 'person'
    registration_number = Column(INTEGER(), nullable=False)
    membership_id = Column(NVARCHAR(30), nullable=False)
    name = Column(NVARCHAR(255), nullable=False)
    birthdate = Column(DATE(), nullable=True)
    mother_name = Column(NVARCHAR(255), nullable=True)
    gender_id = Column(NCHAR(36), nullable=True)
    identity_card_number = Column(NVARCHAR(50), nullable=True)
    membership_fee_category_id = Column(NCHAR(36), nullable=False)
    notes = Column(TEXT(), nullable=True)


if __name__ == '__main__':
    print(Base.metadata.create_all(bind=db_engine))
