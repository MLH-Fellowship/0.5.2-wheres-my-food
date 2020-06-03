import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "cool 😎"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
