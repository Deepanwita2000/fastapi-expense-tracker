from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date
from typing import Optional

import models
from database import get_db
from dependencies import get_current_user

router = APIRouter(
    prefix="/reports",
    tags=["Expense Reports"]
)


@router.get("/summary")
def monthly_summary(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    result = db.query(
        func.count(models.Expense.id).label("total_expenses"),
        func.coalesce(func.sum(models.Expense.amount), 0).label("total_amount")
    ).filter(
        models.Expense.user_id == current_user.id,
        extract("year", models.Expense.expense_date) == year,
        extract("month", models.Expense.expense_date) == month
    ).first()

    return {
        "year": year,
        "month": month,
        "total_expenses": result.total_expenses,
        "total_amount": result.total_amount
    }



# 2. Category-wise report
@router.get("/category-wise")
def category_wise_report(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    results = db.query(
        models.Category.name.label("category"),
        func.count(models.Expense.id).label("total_expenses"),
        func.sum(models.Expense.amount).label("total_amount")
    ).join(
        models.Expense,
        models.Expense.category_id == models.Category.id
    ).filter(
        models.Expense.user_id == current_user.id,
        extract("year", models.Expense.expense_date) == year,
        extract("month", models.Expense.expense_date) == month
    ).group_by(
        models.Category.id,
        models.Category.name
    ).all()

    return {
        "year": year,
        "month": month,
        "categories": [
            {
                "category": row.category,
                "total_expenses": row.total_expenses,
                "total_amount": row.total_amount
            }
            for row in results
        ]
    }


# 3. Yearly report
@router.get("/yearly")
def yearly_report(
    year: int = Query(..., ge=2000, le=2100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    results = db.query(
        extract("month", models.Expense.expense_date).label("month"),
        func.count(models.Expense.id).label("total_expenses"),
        func.sum(models.Expense.amount).label("total_amount")
    ).filter(
        models.Expense.user_id == current_user.id,
        extract("year", models.Expense.expense_date) == year
    ).group_by(
        extract("month", models.Expense.expense_date)
    ).order_by(
        extract("month", models.Expense.expense_date)
    ).all()

    return {
        "year": year,
        "monthly_report": [
            {
                "month": int(row.month),
                "total_expenses": row.total_expenses,
                "total_amount": row.total_amount
            }
            for row in results
        ]
    }