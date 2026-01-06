<div align=center>

# 🔍 Semantic Search Engine

![Python](https://img.shields.io/badge/Python-3.13+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F61?style=for-the-badge)

*A powerful RAG (Retrieval-Augmented Generation) application that enables intelligent Q&A over your PDF documents using vector embeddings and large language models.*


</div>

## Features

- **PDF Document Processing** — Upload and parse PDF documents with automatic text extraction
- **Semantic Understanding** — Leverages embedding models to understand context, not just keywords
- **Conversational Q&A** — Ask natural language questions about your documents
- **Real-time Streaming** — Get LLM responses streamed in real-time for better UX
- **Flexible Model Support** — Switch between local (Ollama) or cloud (OpenAI) models
- **Persistent Vector Store** — ChromaDB storage for efficient similarity search

---

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   PDF File   │────▶│  Text Split  │────▶│  Embeddings  │
└──────────────┘     └──────────────┘     └──────────────┘
                                                 │
                                                 ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Response   │◀────│     LLM      │◀────│   ChromaDB   │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- [Ollama](https://ollama.ai/) installed locally (for local models)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/FamilOrujov/Semantic-Search-Engine.git
   cd Semantic-Search-Engine
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Pull required Ollama models**
   ```bash
   ollama pull mxbai-embed-large
   ollama pull gemma3:1b
   ```

4. **Run the application**
   ```bash
   uv run streamlit run app.py
   ```

5. **Open your browser** at `http://localhost:8501`

---

## Configuration

### Using Local Models (Default)

The application uses Ollama by default with:
- **Embedding Model**: `mxbai-embed-large`
- **LLM**: `gemma3:1b`

### Using OpenAI Models

To switch to OpenAI, edit `app.py`:

```python
# Embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

# LLM Model
llm = ChatOpenAI(model="gpt-4.1-nano")
```

Set your API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key"
```

---

## 📁 Project Structure

```
semantic-search-engine/
├── app.py              # Main Streamlit application
├── chroma/             # Vector database storage
│   └── db/             # Persistent embeddings
├── pyproject.toml      # Project dependencies
├── uv.lock             # Locked dependencies
└── README.md
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit |
| **Framework** | LangChain |
| **Vector Store** | ChromaDB |
| **Embeddings** | Ollama / OpenAI |
| **LLM** | Gemma 3 / GPT-4.1 |
| **PDF Parsing** | PyPDF |

---

## 📝 How It Works

1. **Document Upload** — User uploads a PDF document through the Streamlit interface
2. **Text Splitting** — Document is chunked into manageable pieces (1000 chars with 200 overlap)
3. **Embedding Generation** — Each chunk is converted to a vector embedding
4. **Vector Storage** — Embeddings are stored in ChromaDB for efficient retrieval
5. **Query Processing** — User questions are embedded and matched against stored vectors
6. **Response Generation** — Retrieved context is passed to the LLM for answer synthesis

