from rag import chunk_text
from qdrant_manager import (
    create_collection,
    store_chunks,
    search_chunks,
    get_documents,
    hybrid_search
)
from chatbot import generate_answer

from pydantic import BaseModel

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pypdf import PdfReader
import os

app = FastAPI()

chat_history = []

templates = Jinja2Templates(directory="templates")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(data: QuestionRequest):
    results = hybrid_search(data.question)
    context = "\n\n".join(
        point.payload["text"]
        for point in results
    )

    chat_history.append({
        "role": "user",
        "content": data.question
    })

    answer = generate_answer(context, data.question, chat_history[-6:])

    chat_history.append({
        "role": "assistant",
        "content": answer
    })

    sources =  []

    for point in results:
        source = {
            "document": point.payload["document"],
            "page": point.payload["page"]
        }
        if source not in sources:
            sources.append(source)

    return {
        "answer": answer,
        "sources": sources
    }

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/documents")
async def documents():
    return {
        "documents": get_documents()
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(file_path)
    total_text = ""
    total_chunks = 0

    for page_num, page in enumerate(reader.pages, start=1):
        extracted = page.extract_text()
        if not extracted:
            continue

        total_text += extracted
        chunks = chunk_text(extracted)

        store_chunks(chunks, file.filename, page_num)

        total_chunks += len(chunks)
    
    return {
        "filename": file.filename,
        "characters": len(total_text),
        "chunks_created": total_chunks
    }

@app.on_event("startup")
async def startup_event():
    create_collection()