from fastapi import FastAPI
from decoder.decoder import decode
from pydantic import BaseModel

app = FastAPI()

class DecodeRequest(BaseModel):
    strand: str
    strand_type: str
    five_to_three: bool

@app.post("/decode")
def decode_dna(request: DecodeRequest):
    converted, proteins = decode(request.strand, request.strand_type, request.five_to_three)
    return {"converted": converted, "proteins": proteins}
