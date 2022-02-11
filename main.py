import os, secrets, requests, json
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Response, status, Path
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_503_SERVICE_UNAVAILABLE

from sqlalchemy.orm import Session 
from sqlalchemy import MetaData, inspect
from sqlalchemy.sql import func

from app import model, schema, crud
from app.database import SessionLocal, engine

from dotenv import load_dotenv, find_dotenv

app = FastAPI()

#security = HTTPBasic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def start(
        db:   Session = Depends(get_db)
    ):
    print("Starting up...")
    inspector = inspect(engine)
    # check if we created the tables in the database already. If not, create and populate them
    if not inspector.has_table('customer'):
        print("Creating the tables in the database")
        model.LoyaltyLevel.metadata.create_all(engine)
        model.Customer.metadata.create_all(engine)
        model.Purchase.metadata.create_all(engine)

        #populate the tables with test data
        print("Populating the tables in the database")
        session = Session(engine)
        loyalty_level_instance_1 = model.LoyaltyLevel(level_id="pl", description='Platinum', discount=25)
        loyalty_level_instance_2 = model.LoyaltyLevel(level_id="gl", description='Gold', discount=15)
        session.add_all([loyalty_level_instance_1, loyalty_level_instance_2])
        
        customer_instance = model.Customer(firstname='John', lastname='Doe', date_of_birth=func.now(), level_id=loyalty_level_instance_1.level_id,  signup_date=func.now())
        purchase_instance = model.Purchase(customer = customer_instance, purchase_name="something")
        session.add_all([purchase_instance])
        session.commit()
    else:   
        print("Found the database tables")

@app.on_event("shutdown")
async def shutdown(db:   Session = Depends(get_db)):
        print("Shutting down...")
        print("Dropping tables")
        model.LoyaltyLevel.metadata.drop_all(engine)
        model.Customer.metadata.drop_all(engine)
        model.Purchase.metadata.drop_all(engine)
        print("Tables dropped")
       
    
# # authentication piece (we don't use it in this example)
# def is_authenticated(credentials: HTTPBasicCredentials = Depends(security)):
#     correct_username = secrets.compare_digest(credentials.username, "someusername")
#     correct_password = secrets.compare_digest(credentials.password, "somepassword")
#     if not (correct_username and correct_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect login credentials",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return True


@app.get("/")
def read_root():
    return {"Hello": "World"}

# -- Customer --#

@app.get(
    "/customers",
    tags=["Customers"],
    response_model=List[schema.Customer],
    response_model_exclude={"date_of_birth"}, # in case we need to exclude a field from response
    # response_model_exclude_none=True  # usefull if response json is too big and we want to hide nulls to make it smaller
    summary="Gets all customers",
    response_description="A list containing all the customers"
)
def get_customers(
        db:   Session = Depends(get_db)
        #,auth: bool    = Depends(is_authenticated)
    ):
    return crud.get_customers(db)

@app.get(
    "/customer/{customer_id}",
    tags=["Customers"], # a way to group api calls in the docs page
    response_model=List[schema.Customer],
    summary="Gets a single customer based on customer_id",
    response_description="A single customer based on the provided ID",
    responses={404: {"model": None, "description": "Customer ID not found"}}
)
def get_customer(customer_id: int = Path(
                                        ...,
                                        title="Customer ID",
                                        description="Customer unique indetifier",
                                        gt=0
                                        ),
                db:   Session = Depends(get_db)
                #,auth: bool    = Depends(is_authenticated)
                ):
    """
    Multiline comment
    """
    result = crud.get_customer(db, customer_id)

    if not result:
        return Response(
            'Customer not found',
            media_type="text/plain",
            status_code=HTTP_404_NOT_FOUND
        )

    return result

@app.post("/customer/", 
        tags=["Customers"], # a way to group api calls in the docs page
        response_model=schema.CustomerInput, 
        summary="Create a customer",
        response_description="Newly created customer",
        status_code = status.HTTP_201_CREATED
        )
def create_customer(customer: schema.CustomerInput,
                    db:   Session = Depends(get_db), 
                    #,auth: bool    = Depends(is_authenticated)
                    ):
    if not crud.get_loyalty_level_count(db, customer.level_id) > 0:
        raise HTTPException(status_code=404, detail=str(customer.level_id) + " is not a valid loyalty level id.")
    
    result = crud.create_customer(db, customer)
    return result

@app.put("/customer/", 
        tags=["Customers"],
        response_model=schema.Customer, 
        summary="Update a single customer",
        response_description="Updated the customer",
        status_code = status.HTTP_200_OK
        )
def update_customer(customer: schema.Customer,
                    db:   Session = Depends(get_db),
                    #,auth: bool    = Depends(is_authenticated)
                    ):
    if not crud.get_loyalty_level_count(db, customer.level_id) > 0:
        raise HTTPException(status_code=404, detail=str(customer.level_id) + " is not a valid loyalty level.")

    result = crud.update_customer(db, customer)    
    if isinstance(result, model.Customer):
        return result
    else:
        if result == 404:
            raise HTTPException(
                status_code=404,
                detail="Could not find a customer with key (customer_id=" + str(customer.customer_id) + ")",
                headers={"X-Error": "Some error goes here"},
            )

@app.delete("/customer/{customer_id}", 
        tags=["Customers"],
        response_model=schema.Customer, 
        summary="Delete a single customer based customer_id - cascading (all associated records will be deleted)",
        response_description="Deleted the customer and all the associated records",
        status_code = status.HTTP_200_OK
        )
def delete_customer(customer_id: int = Path(
                                        ...,
                                        title="Customer ID",
                                        description="Customer unique indetifier",
                                        gt=0
                                        ),
                db:   Session = Depends(get_db)
                #,auth: bool    = Depends(is_authenticated)
                ):
    result = crud.delete_customer(db, customer_id)
    
    if isinstance(result, model.Customer):
        return result
    else:
        if result == 404:
            raise HTTPException(
                status_code=404,
                detail="Could not find a customer with key (customer_id=" + str(customer_id) + ")",
                headers={"X-Error": "Some error goes here"},
            )

# -- Purchase --#

@app.get(
    "/purchases",
    tags=["Purchases"],
    response_model=List[schema.Purchase],
    summary="Gets all purchases",
    response_description="A list containing all the purchases"
)
def get_purchases(
        db:   Session = Depends(get_db)
        #,auth: bool    = Depends(is_authenticated)
    ):
    return crud.get_purchases(db)


@app.get(
    "/purchase/{purchase_id}",
    tags=["Purchases"],
    response_model=List[schema.Purchase],
    summary="Gets a single purchase based on purchase_id",
    response_description="A single purchase based on the provided ID",
    responses={404: {"model": None, "description": "Purchase ID not found"}}
)
def get_purchase(purchase_id: int = Path(
                                        ...,
                                        title="Purchase ID",
                                        description="Purchase unique indetifier",
                                        gt=0
                                        ),
                db:   Session = Depends(get_db)
                #,auth: bool    = Depends(is_authenticated)
                ):
    """
    Multiline comment
    """
    result = crud.get_purchase(db, purchase_id)

    if not result:
        return Response(
            'No purchases found',
            media_type="text/plain",
            status_code=HTTP_404_NOT_FOUND
        )
    return result

@app.get(
    "/purchases/{customer_id}",
    tags=["Purchases"],
    response_model=List[schema.Purchase],
    summary="Gets a list of purchases based on customer_id",
    response_description="A list of purchases based on the provided ID",
    responses={404: {"model": None, "description": "Customer ID not found"}}
)
def get_purchase(customer_id: int = Path(
                                        ...,
                                        title="Purchase ID",
                                        description="Purchase unique indetifier",
                                        gt=0
                                        ),
                db:   Session = Depends(get_db)
                #,auth: bool    = Depends(is_authenticated)
                ):
    """
    Multiline comment
    """
    result = crud.get_purchase_based_on_customer_id(db, customer_id)

    if not result:
        return Response(
            'No purchases found',
            media_type="text/plain",
            status_code=HTTP_404_NOT_FOUND
        )
    return result

@app.post("/purchases/", 
        tags=["Purchases"], # a way to group api calls in the docs page
        response_model=schema.Purchase, 
        summary="Create a purchase",
        response_description="Newly created purchase",
        status_code = status.HTTP_201_CREATED
        )
def create_purchase(purchase: schema.PurchaseInput,
                    db:   Session = Depends(get_db), 
                    #,auth: bool    = Depends(is_authenticated),
                    ):
    result = crud.create_purchase(db, purchase)
    
    if isinstance(result, model.Purchase):
        return result
    else:
        if result == 404:
            raise HTTPException(
                status_code=404,
                detail="Integrity constrain violated. Parent key (customer_id=" + str(purchase.customer_id) + ") not found",
                headers={"X-Error": "Some error goes here"},
            ) 

@app.put("/purchase/", 
        tags=["Purchases"],
        response_model=schema.Purchase, 
        summary="Update a single purchase",
        response_description="Updated the purchase",
        status_code = status.HTTP_200_OK
        )
def update_purchase(purchase: schema.Purchase,
                    db:   Session = Depends(get_db),
                    #,auth: bool    = Depends(is_authenticated)
                    ):
    result = crud.update_purchase(db, purchase)
    
    if isinstance(result, model.Purchase):
        return result
    else:
        if result == 404:
            raise HTTPException(
                status_code=404,
                detail="Could not find a purchase card with purchase_id=" + str(purchase.purchase_id) + " and " + "customer_id=" + str(purchase.customer_id) + ")",
                headers={"X-Error": "Some error goes here"},
            )

@app.delete("/purchase/{purchase_id}", 
        tags=["Purchases"],
        response_model=schema.Purchase, 
        summary="Delete a single purchase based on card_id",
        response_description="Deleted a single purchase based on card_id",
        status_code = status.HTTP_200_OK
        )
def delete_purchase(purchase_id: int = Path(
                                        ...,
                                        title="Purchase ID",
                                        description="Purchase unique indetifier",
                                        gt=0
                                        ),
                db:   Session = Depends(get_db)
                #,auth: bool    = Depends(is_authenticated)
                ):
    result = crud.delete_purchase(db, purchase_id)
    
    if isinstance(result, model.Purchase):
        return result
    else:
        if result == 404:
            raise HTTPException(
                status_code=404,
                detail="Could not find a purchase with key (card_id=" + str(purchase_id) + ")",
                headers={"X-Error": "Some error goes here"},
            )

# -- LoyaltyLevel --#

@app.get(
    "/loyalty_levels",
    tags=["LoyaltyLevels"],
    response_model=List[schema.LoyaltyLevel],
    summary="Gets all loyalty levels",
    response_description="A list containing all the loyalty levels"
)
def get_loyalty_levels(
        db:   Session = Depends(get_db)
        #,auth: bool    = Depends(is_authenticated)
    ):
    return crud.get_loyalty_levels(db)

@app.get(
    "/loyalty_level/{level_id}",
    tags=["LoyaltyLevels"], 
    response_model=List[schema.LoyaltyLevel],
    summary="Gets a single loyalty level based on level_id",
    response_description="A single loyalty level based on the provided ID",
    responses={404: {"model": None, "description": "Level ID not found"}}
)
def get_loyalty_level(level_id: str = Path(
                                        ...,
                                        title="Loyalty level ID",
                                        description="Unique loyalty level indetifier",
                                        max_length=2
                                        ),
                db:   Session = Depends(get_db)
                #,auth: bool    = Depends(is_authenticated)
                ):

    result = crud.get_loyalty_level(db, level_id)

    if not result:
        return Response(
            'Loyalty level not found',
            media_type="text/plain",
            status_code=HTTP_404_NOT_FOUND
        )

    return result

@app.post("/loyalty_level/", 
        tags=["LoyaltyLevels"], 
        response_model=schema.LoyaltyLevel, 
        summary="Create a loyalty level",
        response_description="Newly created loyalty level",
        status_code = status.HTTP_201_CREATED
        )
def create_loyalty_level(loyalty_level: schema.LoyaltyLevel,
                    db:   Session = Depends(get_db), 
                    #,auth: bool    = Depends(is_authenticated)
                    ):
        
    result = crud.create_loyalty_level(db, loyalty_level)
    return result

@app.put("/loyalty_level/", 
        tags=["LoyaltyLevels"],
        response_model=schema.LoyaltyLevel, 
        summary="Update a single loyalty level",
        response_description="Updated the loyalty level",
        status_code = status.HTTP_200_OK
        )
def update_loyalty_level(loyalty_level: schema.LoyaltyLevel,
                    db:   Session = Depends(get_db),
                    #,auth: bool    = Depends(is_authenticated)
                    ):
    # if not crud.get_loyalty_level_count(db, loyalty_level.level_id) > 0:
    #     raise HTTPException(status_code=404, detail=str(loyalty_level.level_id) + " is not a valid loyalty level.")

    result = crud.update_loyalty_level(db, loyalty_level)    
    if isinstance(result, model.LoyaltyLevel):
        return result
    else:
        if result == 404:
            raise HTTPException(
                status_code=404,
                detail="Could not find a loyalty level with key (level_id=" + str(loyalty_level.level_id) + ")",
                headers={"X-Error": "Some error goes here"},
            )

@app.delete("/loyalty_level/{level_id}", 
        tags=["LoyaltyLevels"],
        response_model=schema.LoyaltyLevel, 
        summary="Delete a single loyalty level based level_id",
        response_description="Deleted the loyalty level",
        status_code = status.HTTP_200_OK
        )
def delete_loyalty_level(level_id: str = Path(
                                        ...,
                                        title="Loyalty level ID",
                                        description="Unique loyalty level indetifier",
                                        max_length=2
                                        ),
                db:   Session = Depends(get_db)
                #,auth: bool    = Depends(is_authenticated)
                ):
    result = crud.delete_loyalty_level(db, level_id)
    
    if isinstance(result, model.LoyaltyLevel):
        return result
    else:
        if result == 404:
            raise HTTPException(
                status_code=404,
                detail="Could not find a loyalty level with key (level_id=" + str(level_id) + ")",
                headers={"X-Error": "Some error goes here"},
            )

