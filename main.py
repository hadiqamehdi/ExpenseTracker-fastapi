from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
from fastapi.responses import FileResponse
import os


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JSON_FILE = "C:/Users/hadiqa.mehdi/Desktop/expense-tracker/expense.json"

class Expense(BaseModel):
    title: str
    amount: float
    category: str
    date: str

# ✅ define file functions first
def read_file() -> List[dict]:
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, 'r') as f:
        return json.load(f)

def write_file(expenses: List[dict]):
    with open(JSON_FILE, 'w') as f:
        json.dump(expenses, f, indent=4)

# ✅ endpoints after
@app.get("/expenses")
def get_expenses():
    return read_file()

@app.post("/add-expense")
def add_expense(expense: Expense):
    expense_file = read_file()
    expense_file.append(expense.dict())
    write_file(expense_file)
    return {"message": "expense added successfully"}

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))
