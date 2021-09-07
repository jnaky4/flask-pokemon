from Tables import metadata
from sqlalchemy import Column, Integer, String, Float, Table, Sequence


UserTable = Table(
    'Users', metadata,
    Column('id', Integer, Sequence('seq_reg_id_70', increment=1, start=1), primary_key=True),
    Column('name', String(25), nullable=False),
    Column('email', String(25), nullable=False),
    Column('password', String(25), nullable=False),
    Column('telephone', Integer, nullable=False),
    Column('address', String(125), nullable=False),
    Column('city', String(25), nullable=False),
    Column('state', String(2), nullable=False),
    Column('zipcode', Integer, nullable=False)
                )
