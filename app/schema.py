from ast import LtE, Num
from typing import List, Optional
from unicodedata import numeric
from fastapi import Query
from pydantic import BaseModel
from datetime import date

class LoyaltyLevel(BaseModel):

    level_id: str = Query(
        ...,
        title="Loyalty level ID",
        description="Loyalty level ID",
        max_length=2,
    )
    description: Optional[str] = Query(
        None,
        title="Loyalty level description",
        description="The description of the Loyalty level",
        max_length=100,
    )
    discount: Optional[int] = Query(
        0,
        title="Loyalty discount percentage",
        description="Loyalty discount percentage",
        lte=100
    )

    class Config:
        orm_mode = True

class Customer(BaseModel):
    customer_id: int = Query(                                         
        ...,                                                                    
        title="Customer ID",                                                    
        description="The ID of the customer",                                 
        gt=0,

    )
    firstname: Optional[str] = Query(
        None,
        title="Customer's first name",
        description="The first name of the customer",
        max_length=100,
    )
    lastname: Optional[str] = Query(
        None,
        title="Customer's last name",
        description="The last name of the customer",
        max_length=100,
    )
    date_of_birth: Optional[date] = Query(
        None,
        title="Date of birth",
        description="Customer's date of birth",
    )
    level_id: str = Query(
        ...,
        title="Loyalty level ID",
        description="Loyalty level ID",
        max_length=2,
    )
    signup_date: Optional[date] = Query(
        None,
        title="Sign up date",
        description="Customer's sign up date",
    )
        
    class Config:
        orm_mode = True
    
# a copy of the Customer model but without the customer_id. We create this for POST requests validation
# this is done since we don't need to specify a the key (customer_id) whern creating a customer (since it's a sequence)
class CustomerInput(BaseModel):
    firstname: Optional[str] = Query(
        None,
        title="Customer's first name",
        description="The first name of the customer",
        max_length=100,
    )
    lastname: Optional[str] = Query(
        None,
        title="Customer's last name",
        description="The last name of the customer",
        max_length=100,
    )
    date_of_birth: Optional[date] = Query(
        None,
        title="Date of birth",
        description="Customer's date of birth",
    )
    level_id: str = Query(
        ...,
        title="Loyalty level ID",
        description="Loyalty level ID",
        max_length=2,
    )
    signup_date: Optional[date] = Query(
        None,
        title="Sign up date",
        description="Customer's sign up date",
    )

    class Config:
        orm_mode = True

class Purchase(BaseModel):
    purchase_id: int = Query(                                         
        ...,                                                                    
        title="Purchase ID",                                                    
        description="The ID of the purchase",                                 
        gt=0,
    )
    customer_id: int = Query(
        ...,
        title="Customer ID FK",
        description="Customer ID FK",
        gt=0,
    )
    purchase_name: Optional[str] = Query(
        None,
        title="Purchase name",
        description="The name of the purchase",
        max_length=100,
    )
    purchase_date: Optional[date] = Query(
        None,
        title="Purchase date",
        description="The date of the purchase",
    )
    
    class Config:
        orm_mode = True

class PurchaseInput(BaseModel):
    customer_id: int = Query(
        ...,
        title="Customer ID FK",
        description="Customer ID FK",
        gt=0,
    )
    purchase_name: Optional[str] = Query(
        None,
        title="Purchase name",
        description="The name of the purchase",
        max_length=100,
    )
    purchase_date: Optional[date] = Query(
        None,
        title="Purchase date",
        description="The date of the purchase",
    )
    
    class Config:
        orm_mode = True
        
