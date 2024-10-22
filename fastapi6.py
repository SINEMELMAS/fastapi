from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


# Define a Pydantic model for the BMI output
class BMIOutput(BaseModel):
    bmi: float
    message: str


# Simple route to say Hi!
@app.get("/")
def Hi():
    return {"message": "HI!"}


# BMI calculation function
@app.get("/Function1", response_model=BMIOutput)
def Function1(weight: float = Query(..., description="Weight in kilograms"),
              height: float = Query(..., description="Height in meters")):
    # Calculate BMI
    bmi = weight / (height ** 2)

    # Generate a message based on the BMI value
    if bmi < 18.5:
        message = "You are underweight."
    elif 18.5 <= bmi < 24.9:
        message = "You have a normal weight."
    elif 25 <= bmi < 29.9:
        message = "You are overweight."
    else:
        message = "You are obese."

    # Return the result as a BMIOutput model
    return BMIOutput(bmi=bmi, message=message)
