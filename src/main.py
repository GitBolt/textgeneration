import string
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from core.evaluate import generate
from core.model import RNN

all_characters = string.printable
n_characters = len(all_characters)
device = "cuda:0" if torch.cuda.is_available() else "cpu"

model = RNN(
    n_characters,
    256,
    2,
    n_characters
).to(device)
model.load_state_dict(torch.load(
    "data/data.pt",
    map_location=torch.device(device))
)
model.eval()

app = FastAPI()

class Content(BaseModel):
    content: str
    length: int


@app.get("/")
async def index():
    return {"message": "hi, go to /docs"}


@app.post("/kashbot")
async def kashbot(content: Content):
    return generate(
        model,
        content.dict()["content"],
        content.dict()["length"]
    )
