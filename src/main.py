import string
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from eval import generate

all_characters = string.printable
n_characters = len(all_characters)

device = "cuda:0" if torch.cuda.is_available else "cpu"

app = FastAPI()


class Content(BaseModel):
    content: str
    length: int

@app.get("/")
async def index():
    return {"message": "hi, go to /docs"}
    
@app.post("/kashbot")
async def kashbot(content: Content):
    return generate(content.dict()["content"], content.dict()["length"])