from typing import Optional
from sqllite import sqllite_db
from fastapi import FastAPI
import uvicorn
from databases import Database

database = Database("sqlite+aiosqlite:///metroscubicos.sqlite")


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def database_connetc():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    query = f"SELECT * FROM ESTATE LIMIT {item_id}"
    results = await database.fetch_all(query=query)
    return results

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0", debug=True)
