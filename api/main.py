from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from decoder.decoder import decode
from pydantic import BaseModel

app = FastAPI()

origins = ["http://localhost:5173", "https://dna-decoding-full-stack-hq6wda947-kangaroo0726s-projects.vercel.app", "https://dna-decoding-full-stack.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DecodeRequest(BaseModel):
    strand: str
    strand_type: str
    five_to_three: bool

@app.post("/decode")
def decode_dna(request: DecodeRequest):
    try:
        converted, proteins = decode(request.strand, request.strand_type, request.five_to_three)
        return {"converted": converted, "proteins": proteins}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
