import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from backend.rag import ask_question, load_user_pdf
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # 1. Check if file is PDF
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )
        
        # 2. Create temp folder
        os.makedirs("temp", exist_ok=True)
        
        # 3. Read and save file
        contents = await file.read()
        file_path = f"temp/{file.filename}"
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # 4. Process PDF
        load_user_pdf(file_path)
        
        return {
            "message": "PDF uploaded successfully",
            "filename": file.filename,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading PDF: {str(e)}"
        )

@app.post("/ask")
def ask(data: Question):
    try:
        result = ask_question(data.question)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )