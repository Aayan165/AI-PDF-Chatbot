import utils.session
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

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException

from pypdf import PdfReader
import os

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"message": "Rate limit exceeded. Please try again later."},
    )

chat_history = []

templates = Jinja2Templates(directory="templates")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class QuestionRequest(BaseModel):
    question: str

@limiter.limit("20/minute")
@app.post("/ask")
async def ask_question(request: Request, data: QuestionRequest):
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

@limiter.limit("5/minute")
@app.post("/upload")
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    content = await file.read()

    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File size must be less than 10 MB."
        )

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