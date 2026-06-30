from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams, PointStruct
from dotenv import load_dotenv
import os
import uuid
from embeddings import get_embedding

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "pdf_chunks"

def create_collection():
    collections = client.get_collections()

    existing = [
        c.name
        for c in collections.collections
    ]

    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=3072,
                distance=Distance.COSINE
            )
        )
        print("Collection created")
    else:
        print("Collection already exists")


def store_chunks(chunks, filename, page_number):
    points = []

    for chunk in chunks:
        embedding = get_embedding(chunk)
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "document": filename,
                    "page": page_number
                }
            )
        )
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    print(
        f"{len(chunks)} chunks stored from "
        f"{filename} page {page_number}"
    )

def search_chunks(question, limit=8):
    question_embedding = get_embedding(question)
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding,
        limit=limit
    )

    return results.points

def get_documents():
    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True
    )
    documents = set()

    for point in points:
        documents.add(point.payload["document"])

    return sorted(list(documents))

def keyword_search(question):
    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True
    )

    keywords = question.lower().split()
    matches = []
    for point in points:
        text = point.payload["text"].lower()
        score = 0
        for word in keywords:
            if word in text:
                score += 1
        if score > 0:
            matches.append((score, point))
    
    matches.sort(key=lambda x: x[0], reverse=True)

    return [
        point for score, point in matches[:5]
    ]

def hybrid_search(question):
    semantic_results = search_chunks(question, limit=5)
    keyword_results = keyword_search(question)

    combined = []
    seen = set()

    for point in semantic_results + keyword_results:
        if point.id not in seen:
            combined.append(point)
            seen.add(point.id)

    return combined[:8]