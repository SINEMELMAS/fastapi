from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Calculator! Use endpoints /add, /subtract, /multiply, /divide."}

@app.get("/add")
def add(a: float, b: float):
    result = a + b
    return {"operation": "addition", "a": a, "b": b, "result": result}

@app.get("/subtract")
def subtract(a: float, b: float):
    result = a - b
    return {"operation": "subtraction", "a": a, "b": b, "result": result}

@app.get("/multiply")
def multiply(a: float, b: float):
    result = a * b
    return {"operation": "multiplication", "a": a, "b": b, "result": result}

@app.get("/divide")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
    result = a / b
    return {"operation": "division", "a": a, "b": b, "result": result}
