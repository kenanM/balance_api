from sqlalchemy import (
    Column,
    Date,
    Float,
    Integer,
)


from balance.database import Base


class Balance(Base):
    __tablename__ = 'balance'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)

    def __init__(self, amount, date):
        self.amount = amount
        self.date = date
