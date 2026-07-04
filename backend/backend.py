from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],# for development
    allow_methods=["*"],
    allow_headers=["*"],
)


class RequestModel (BaseModel):
    query: str
@app.post("/generate")
def generate_response (req: RequestModel):
    result = f"{req.query}"
    return {"result":result}