# AI PDF Chatbot

An intelligent chatbot that allows users to upload PDF documents and ask questions in natural language. Instead of relying solely on a language model's knowledge, the chatbot retrieves the most relevant information directly from the uploaded document before generating a response, resulting in accurate, context-aware answers with minimal hallucinations.

---

## 🚀 Features

- 📄 Upload and process multiple PDF documents
- 💬 Natural language question answering
- 🧠 Retrieval-Augmented Generation (RAG)
- ✂️ Semantic text chunking
- 🔍 Hybrid search for improved retrieval
- 🗄️ Vector database powered by Qdrant
- 🤖 Context-aware responses using Google Gemini
- 📚 Multi-document retrieval
- 💡 Source citations for every response
- 📝 Conversation history
- ⚡ Real-time streaming responses
- 🌐 FastAPI backend with a responsive web interface

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Backend | FastAPI |
| Language Model | Google Gemini |
| Vector Database | Qdrant |
| PDF Processing | PyPDF |
| Language | Python |
| Embeddings | Google Embedding Models |
| Frontend | HTML, CSS, JavaScript |

---

## 📂 Project Structure

```text
AI-PDF-Chatbot/
│
├── main.py
├── templates/
├── static/
├── uploads/
├── .env
├── .env.example
├── requirements.txt
├── README.md
└── ...
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Aayan165/AI-PDF-Chatbot.git
cd AI-PDF-Chatbot
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

Or simply duplicate the file and rename it to `.env`.

Then update the values:

```env
GEMINI_API_KEY="your_gemini_api_key"

QDRANT_URL="your_qdrant_url"
QDRANT_API_KEY="your_qdrant_api_key"
```

### 5. Run the application

```bash
uvicorn main:app --reload
```

Open your browser and visit:

```
http://127.0.0.1:8000
```

---

## 🧠 How It Works

1. Upload a PDF document.
2. The application extracts text from the PDF.
3. The text is divided into semantic chunks with overlap.
4. Each chunk is converted into vector embeddings.
5. Embeddings are stored in Qdrant.
6. When a user asks a question:
   - The query is embedded.
   - The most relevant chunks are retrieved using hybrid search.
   - Retrieved context is passed to Google Gemini.
   - Gemini generates an accurate, context-aware answer.

---

## 🎯 Future Improvements

- OCR support for scanned PDFs
- Support for additional document formats (DOCX, PPTX, TXT)
- User authentication and personalized workspaces
- Chat with an entire document library
- Advanced metadata filtering
- Document summarization
- Export chat history (PDF/Markdown)
- Docker containerization
- Cloud deployment (AWS/Azure/GCP)
- Role-based access control for teams
- Citation highlighting within the PDF viewer

---

## 📚 Learning Outcomes

This project helped me gain practical experience with:

- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Google Gemini API
- Vector Databases
- Embeddings
- Hybrid Search
- FastAPI
- Prompt Engineering
- AI Application Development

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome! Feel free to fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.
