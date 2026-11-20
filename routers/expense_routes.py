
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas

from database import get_db
from dependencies import get_current_user


router = APIRouter(prefix="/expenses", tags=["Expenses"])


# CREATE EXPENSE
@router.post("/", response_model=schemas.ExpenseResponse,
             status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    print("current_user: ",current_user)

    category = db.query(models.Category).filter(
        models.Category.id == expense.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    new_expense = models.Expense(
        title=expense.title,
        amount=expense.amount,
        description=expense.description,
        expense_date=expense.expense_date,
        category_id=expense.category_id,
        user_id=current_user.id
    )
    try:

        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)
    except:
        db.rollback
        raise HTTPException(
        status_code=500,
        detail="Something went wrong while creating expense"
    )

    return new_expense


# # GET ALL EXPENSES
# @router.get("/", response_model=list[schemas.ExpenseResponse])
# def get_expenses(
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)
# ):

#     expenses = db.query(models.Expense).filter(
#         models.Expense.user_id == current_user.id
#     ).all()

#     return expenses

from typing import Optional
from datetime import date
from fastapi import Query
import math


@router.get("/", response_model=schemas.ExpenseListResponse)
def get_expenses(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100),

    category_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,

    min_amount: Optional[float] = Query(None, ge=0),
    max_amount: Optional[float] = Query(None, ge=0),

    search: Optional[str] = None,

    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    query = db.query(models.Expense).filter(
        models.Expense.user_id == current_user.id
    )

    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be greater than end date"
        )

    if min_amount is not None and max_amount is not None:
        if min_amount > max_amount:
            raise HTTPException(
                status_code=400,
                detail="Minimum amount cannot be greater than maximum amount"
            )

    # CATEGORY FILTER
    if category_id is not None:
        query = query.filter(models.Expense.category_id == category_id )

    # DATE FILTER
    if start_date is not None:
        query = query.filter(models.Expense.expense_date >= start_date)

    if end_date is not None:
        query = query.filter(models.Expense.expense_date <= end_date )

    # AMOUNT FILTER
    if min_amount is not None:
        query = query.filter(models.Expense.amount >= min_amount )

    if max_amount is not None:
        query = query.filter(models.Expense.amount <= max_amount )

    # SEARCH BY TITLE
    if search:
        query = query.filter(models.Expense.title.ilike(f"%{search}%"))

    # TOTAL RECORDS
    total = query.count()

    # PAGINATION
    offset = (page - 1) * limit

    expenses = query.order_by(
        models.Expense.expense_date.desc(),
        models.Expense.id.desc()
    ).offset(offset).limit(limit).all()

    total_pages = math.ceil(total / limit)

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "expenses": expenses
    }



# GET SINGLE EXPENSE
@router.get("/{expense_id}", response_model=schemas.ExpenseResponse)
def get_single_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense


# UPDATE EXPENSE
@router.put("/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(
    expense_id: int,
    updated_data: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    category = db.query(models.Category).filter(
        models.Category.id == updated_data.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    expense.title = updated_data.title
    expense.amount = updated_data.amount
    expense.description = updated_data.description
    expense.expense_date = updated_data.expense_date
    expense.category_id = updated_data.category_id

    try:
        db.commit()
        db.refresh(expense)
    except:
        db.rollback()
        raise HTTPException(
        status_code=500,
        detail="Something went wrong while creating expense"
    )

    return expense


# DELETE EXPENSE
@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
    
    try:
        db.delete(expense)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(
        status_code=500,
        detail="Something went wrong while creating expense"
    )

    return {"message": "Expense deleted successfully"}
