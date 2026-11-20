from fastapi import FastAPI
# from database import engine, Base
# import models

from routers import auth_routes , expense_routes , category_routes, report_routes

app = FastAPI(title="Expense Tracker API")

# Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(expense_routes.router)
app.include_router(category_routes.router)
app.include_router(report_routes.router)


@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}