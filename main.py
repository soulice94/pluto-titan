from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import strategies.strategy_1 as strategy1
import strategies.strategy_2 as strategy2
import aiofiles
import uuid
from pydantic import BaseModel
from typing import Annotated, List
from classifier import SimpleMerchantClassifier


class ExecuteStrategyRequest(BaseModel):
    file_uuid: str
    strategy: str


app = FastAPI()

# CORS settings
# modify the IP addresses as needed
# the pluto app will be accessed from these origins
# I ran this project in local development
origins = [
    "http://localhost:8081",
    "http://192.168.68.*:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the PDF Transaction Extractor API"}


@app.post("/file/upload/")
async def upload_file(file: Annotated[UploadFile, File()]):
    file_content = await file.read()
    file_uuid = uuid.uuid4()
    # saving the file inside the temp_pdfs folder
    print(f"Saving file with UUID: {file_uuid}")
    async with aiofiles.open(f"temp_pdfs/{str(file_uuid)}.pdf", "wb") as f:
        await f.write(file_content)
    # Here you would typically save the file or process it
    print(f"Received file: {file.filename} with UUID: {file_uuid}")
    return {"file_name": file.filename, "file_uuid": str(file_uuid)}


@app.post("/file/filter/")
async def execute_strategy(request: ExecuteStrategyRequest):
    file_uuid, strategy = request.file_uuid, request.strategy
    result = ""
    if strategy == "1":
        result = await strategy1.run(file_uuid)
    elif strategy == "2":
        result = await strategy2.run(file_uuid)
    else:
        return {"error": "Invalid strategy selected. Please choose '1' or '2'."}

    return {"result": result}


class MerchantClassificationRequest(BaseModel):
    merchants: List[str]
    similarity_threshold: float = 0.7


@app.post("/merchants/classify-simple/")
async def classify_merchants_simple(request: MerchantClassificationRequest):
    """Group similar merchants using fuzzy matching"""
    # Initialize simple classifier
    simple_classifier = SimpleMerchantClassifier()
    try:
        groups = simple_classifier.group_merchants(
            request.merchants,
            int(request.similarity_threshold * 100),  # Convert to percentage
        )

        return {
            "groups": groups,
            "total_groups": len(groups),
            "total_merchants": len(request.merchants),
        }
    except Exception as e:
        return {"error": f"Classification failed: {str(e)}"}
