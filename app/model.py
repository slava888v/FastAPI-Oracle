from numbers import Number
from sqlalchemy import Sequence, Boolean, Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from .database import Base, engine

class LoyaltyLevel(Base):
    __tablename__ = "loyalty_level"
    #__table_args__ = {'schema': 'db_schema_name'}
    
    level_id            = Column(String(length=2), primary_key=True)
    description         = Column(String(length=100))
    discount            = Column(Integer)           
    customer            = relationship("Customer", back_populates="loyalty_level")
    
# one to many relationship
class Purchase(Base):
    __tablename__ = "purchase"
#     __table_args__ = {'schema': 'db_schema_name'}
    
    purchase_id         = Column(Integer, Sequence('purchase_id_seq'), primary_key=True)
    customer_id         = Column(Integer, ForeignKey('customer.customer_id', ondelete="CASCADE"), nullable=False)
    purchase_name       = Column(String(length=100))
    purchase_date       = Column(Date) 
    # many-to-one
    customer            = relationship("Customer", back_populates="purchase")

class Customer(Base):
    __tablename__ = "customer"
#     __table_args__ = {'schema': 'db_schema_name'}

    customer_id     = Column(Integer, Sequence('customer_id_seq'), primary_key=True)
    firstname       = Column(String(length=100))
    lastname        = Column(String(length=100))
    date_of_birth   = Column(Date) 
    level_id        = Column(String(length=2), ForeignKey('loyalty_level.level_id'))
    signup_date     = Column(Date) 
    #one-to-one
    loyalty_level   = relationship("LoyaltyLevel", back_populates="customer", uselist=False)
    #one-to-many    
    purchase        = relationship("Purchase", back_populates="customer", cascade="all, delete", passive_deletes=True,)    

