from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
)

Base = declarative_base()


class Limits(Base):
    __tablename__ = 'limits'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    max_transfer = Column(Integer, nullable=False)


class TransactionHistory(Base):
    __tablename__ = 'transfer_history'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    country = Column(String, nullable=False)
