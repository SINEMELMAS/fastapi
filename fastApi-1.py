from fastapi import FastAPI

app = FastAPI()
# The "name" parameter is passed as a query parameter
@app.get("/")
async def read(name: str):
   return {"message": f"Hello, {name}!"}
