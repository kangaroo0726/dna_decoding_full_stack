from fastapi import FastAPI, HTTPException
from decoder.decoder import decode
from pydantic import BaseModel

app = FastAPI()

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
