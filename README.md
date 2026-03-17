---
title: Customer Support AI Agent
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.40.0"
python_version: "3.11"
app_file: app.py
pinned: false
---

# 🤖 Customer Support AI Agent

An intelligent customer support agent built with **LangGraph**, **RAG**, and **Web Search** that handles customer queries in Bengali, English, and Banglish — automatically routing to the most appropriate response source.

---

## 🎯 Project Overview

This project implements a **multi-node AI agent** that intelligently routes customer queries through three layers:

1. **RAG (Retrieval Augmented Generation)** — Searches company knowledge base first
2. **Web Search** — Falls back to internet search if knowledge base has no answer
3. **Human Escalation** — Escalates to human support team if no answer found anywhere

---

## 🏗️ Architecture

```
Customer Query (Bengali / English / Banglish)
        ↓
[Smart Router] ──── User-specific query? ──→ [Escalate 🔴]
        ↓
    [RAG Node] ──── Answer found? ──→ [Respond 🟢]
        ↓
[Web Search Node] ── Answer found? ──→ [Respond 🔵]
        ↓
  [Escalate Node 🔴]
        ↓
  [Logger Node] → conversations.json
        ↓
[Streamlit Dashboard]
```

---

## ✨ Features

- 🌐 **Multilingual Support** — Bengali, English, and Banglish queries handled automatically
- 🔍 **RAG Pipeline** — ChromaDB vector store with multilingual embeddings
- 🌍 **Web Search Fallback** — Tavily API for real-time internet search
- 🚨 **Smart Escalation** — Automatic ticket generation with unique Reference ID
- 📊 **Live Dashboard** — Real-time stats, resolution rate, and conversation logs
- 💬 **Language Detection** — Automatic response language matching customer's language
- 🧠 **Smart Router** — Detects user-specific queries and routes directly to escalation

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | LangGraph |
| LLM | Groq (Llama 3.1 8B) |
| Vector Store | ChromaDB |
| Embeddings | sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 |
| Web Search | Tavily API |
| UI | Streamlit |
| Language | Python 3.11 |

---

## 📁 Project Structure

```
customer-support-agent/
│
├── app.py                          # Streamlit UI & Dashboard
├── graph.py                        # LangGraph workflow & all nodes
├── requirements.txt
├── .env                            # API keys (not committed)
├── .gitignore
│
├── vectorstore/
│   ├── __init__.py
│   └── setup_chroma.py             # ChromaDB setup & update functions
│
├── nodes/
│   └── __init__.py
│
├── data/                           # Knowledge base files
│   ├── orders.txt                  # Order related Q&A
│   ├── shipping.txt                # Shipping & delivery info
│   ├── payment.txt                 # Payment methods & refunds
│   ├── returns.txt                 # Return & exchange policy
│   ├── products.txt                # Product info & warranty
│   ├── account.txt                 # Account management
│   ├── offers.txt                  # Discounts & promotions
│   ├── technical.txt               # Technical support
│   └── general.txt                 # General company info
│
└── logs/
    └── conversations.json          # Conversation history
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11
- Groq API Key — [Get free key](https://console.groq.com)
- Tavily API Key — [Get free key](https://tavily.com)

###1. Installation

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

**5. Run the app**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

> **Note:** First run will automatically set up the ChromaDB vector store from knowledge base files. This takes 2-3 minutes.

---

## 🧪 Example Queries

| Query | Language | Source |
|-------|----------|--------|
| "Return policy কি?" | Bengali | 🟢 Knowledge Base |
| "What payment methods do you accept?" | English | 🟢 Knowledge Base |
| "Shipping charge koto?" | Banglish | 🟢 Knowledge Base |
| "What is the current dollar to BDT rate?" | English | 🔵 Web Search |
| "bKash account kivabe khulbo?" | Banglish | 🔵 Web Search |
| "আমার অর্ডার কোথায়?" | Bengali | 🔴 Escalated |
| "My order #12345 is missing" | English | 🔴 Escalated |
| "amar refund aseni" | Banglish | 🔴 Escalated |

---

## 📊 Dashboard Features

- **Total Conversations** counter
- **Source breakdown** — RAG vs Web vs Escalated counts
- **Resolution Rate** progress bar
- **Recent Conversations** with expandable details
- **Clear Chat** and **Refresh** controls

---

## 🔧 Adding New Knowledge

To add new topics to the knowledge base:

**1. Create a new `.txt` file in `data/` folder** following this format:
```
## Topic Title

Detailed information about the topic.
Include multiple sentences for better context.

Keywords: keyword1, keyword2, বাংলা কীওয়ার্ড, banglish keyword

---
```

**2. Delete the existing vector store:**
```bash
rd /s /q chroma_db     # Windows
```

**3. Restart the app** — it will rebuild automatically.

---

## ⚙️ Configuration

Key settings in `graph.py`:

```python
# Number of documents to retrieve from knowledge base
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Number of web search results
results = tavily.search(query=state["query"], max_results=3)

# LLM model
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
```

---

## 🌐 Deployment

### Deploy on Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add secrets in Streamlit Cloud settings:
   ```
   GROQ_API_KEY = "your_key"
   TAVILY_API_KEY = "your_key"
   ```
5. Deploy!

---

## 📈 Performance

- **Knowledge Base queries:** ~1-2 seconds response time
- **Web Search queries:** ~2-4 seconds response time
- **Accuracy:** ~85-90% correct routing across all query types
- **Languages supported:** Bengali, English, Banglish

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Mahabub**
- Junior AI Engineer | LLM & Generative AI Enthusiast
- Built with LangGraph, RAG, and Streamlit

---

## 🙏 Acknowledgements

- [LangChain](https://langchain.com) — LLM framework
- [LangGraph](https://langchain-ai.github.io/langgraph) — Agent orchestration
- [Groq](https://groq.com) — Fast LLM inference
- [Tavily](https://tavily.com) — AI-powered web search
- [ChromaDB](https://chromadb.com) — Vector database
- [Streamlit](https://streamlit.io) — UI framework