
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models,schemas
from database import get_db
from dependencies import get_current_user


router = APIRouter(prefix="/categories",  tags=["Categories"])

# CREATE CATEGORY
@router.post("/", response_model=schemas.CategoryResponse,status_code=status.HTTP_201_CREATED)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    existing_category = db.query(models.Category).filter(
        models.Category.name == category.name
    ).first()

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    new_category = models.Category(name=category.name)

    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
    except:
        db.rollback()
        raise HTTPException(
        status_code=500,
        detail="Something went wrong while creating expense"
    )

    return new_category


# GET ALL CATEGORIES
@router.get("/", response_model=list[schemas.CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    return db.query(models.Category).all()


# GET SINGLE CATEGORY
@router.get("/{category_id}", response_model=schemas.CategoryResponse)
def get_single_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


# UPDATE CATEGORY
@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(
    category_id: int,
    updated_data: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    duplicate = db.query(models.Category).filter(
        models.Category.name == updated_data.name,
        models.Category.id != category_id
    ).first()
    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Category name already exists"
        )
    category.name = updated_data.name
    db.commit()
    db.refresh(category)
    return category


# DELETE CATEGORY
@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    existing_expenses = db.query(models.Expense).filter(
        models.Expense.category_id == category_id
    ).first()

    if existing_expenses:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category because expenses are associated with it"
        )

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}
