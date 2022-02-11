from sqlalchemy.orm import Session
from sqlalchemy import func, or_, exc
from fastapi.encoders import jsonable_encoder
from . import model, schema

# -- Customer --#

def get_customers(db: Session):
    return db.query(model.Customer).all()

def get_customer(db: Session, customer_id: int):
    return db.query(model.Customer).filter(
        model.Customer.customer_id == customer_id
    ).all()

def create_customer(db: Session, customer: schema.CustomerInput):   
    db_item = model.Customer(firstname=customer.firstname, 
                                       lastname=customer.lastname, 
                                       date_of_birth=customer.date_of_birth, 
                                       level_id=customer.level_id,
                                       signup_date=customer.signup_date
                                       )
    # we can also populate the model using a shortcut:  
    # db_item = model.Customer(**customer.dict())                                        
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
 
def update_customer(db: Session, customer: schema.Customer): 
    existing_customer = db.query(model.Customer).filter(model.Customer.customer_id == customer.customer_id).first()
    if existing_customer:
        db.query(model.Customer).filter(model.Customer.customer_id == existing_customer.customer_id).update(customer.dict())
        db.commit()
        return existing_customer
    else:
        return 404

def delete_customer(db: Session, customer_id: int): 
    existing_customer = db.query(model.Customer).filter(model.Customer.customer_id == customer_id).first()
    if existing_customer:
        db.query(model.Customer).filter(model.Customer.customer_id == customer_id).delete()
        db.commit()
        return existing_customer
    else:
        return 404

# -- LoyaltyLevel --#

def get_loyalty_levels(db: Session):
    return db.query(model.LoyaltyLevel).all()

def get_loyalty_level(db: Session, level_id: int):
    return db.query(model.LoyaltyLevel).filter(
        model.LoyaltyLevel.level_id == level_id
    ).all()

def get_loyalty_level_count(db: Session, level_id: int):
    return db.query(model.LoyaltyLevel).filter(
        model.LoyaltyLevel.level_id == level_id
    ).count()

def create_loyalty_level(db: Session, loyalty_level: schema.LoyaltyLevel):   
    db_item = model.LoyaltyLevel(**loyalty_level.dict())                                  
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_loyalty_level(db: Session, loyalty_level: schema.LoyaltyLevel): 
    existing_loyalty_level = db.query(model.LoyaltyLevel).filter(model.LoyaltyLevel.level_id == loyalty_level.level_id).first()
    if existing_loyalty_level:
        db.query(model.LoyaltyLevel).filter(model.LoyaltyLevel.level_id == existing_loyalty_level.level_id).update(loyalty_level.dict())
        db.commit()
        return existing_loyalty_level
    else:
        return 404

def delete_loyalty_level(db: Session, level_id: int): 
    existing_loyalty_level = db.query(model.LoyaltyLevel).filter(model.LoyaltyLevel.level_id == level_id).first()
    if existing_loyalty_level:
        db.query(model.LoyaltyLevel).filter(model.LoyaltyLevel.level_id == level_id).delete()
        db.commit()
        return existing_loyalty_level
    else:
        return 404

# -- Purchase --#

def get_purchases(db: Session):
    return db.query(model.Purchase).all()

def get_purchase(db: Session, purchase_id: int):
    return db.query(model.Purchase).filter(
        model.Purchase.purchase_id == purchase_id
    ).all()

def get_purchase_based_on_customer_id(db: Session, customer_id: int):
    return db.query(model.Purchase).filter(
        model.Purchase.customer_id == customer_id
    ).all()

def create_purchase(db: Session, purchase: schema.PurchaseInput):
    db_item = model.Purchase(**purchase.dict())    
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except exc.IntegrityError:
        db.rollback()
        return 404

def update_purchase(db: Session, purchase: schema.Purchase): 
    existing_purchase = db.query(model.Purchase).filter(model.Purchase.customer_id == purchase.customer_id, model.Purchase.purchase_id == purchase.purchase_id).first()
    if existing_purchase:
        db.query(model.Purchase).filter(model.Purchase.purchase_id == existing_purchase.purchase_id).update(purchase.dict())
        db.commit()
        return existing_purchase
    else:
        return 404

def delete_purchase(db: Session, purchase_id: int): 
    existing_purchase = db.query(model.Purchase).filter(model.Purchase.purchase_id == purchase_id).first()
    if existing_purchase:
        db.query(model.Purchase).filter(model.Purchase.purchase_id == existing_purchase.purchase_id).delete()
        db.commit()
        return existing_purchase
    else:
        return 404

  