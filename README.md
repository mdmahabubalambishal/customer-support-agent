---
title: Customer Support AI Agent
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: false
license: mit
---

<div align="center">

# 🤖 Customer Support AI Agent

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&pause=1000&color=3498DB&center=true&vCenter=true&width=600&lines=Intelligent+Customer+Support+Agent;LangGraph+%7C+RAG+%7C+Web+Search;Bengali+%7C+English+%7C+Banglish;Deployed+on+Hugging+Face+Spaces" alt="Typing SVG" />

<br>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-FF6B6B?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F54E42?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6B35?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![HuggingFace](https://img.shields.io/badge/🤗_Hugging_Face-Deployed-FFD21E?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-2ecc71?style=for-the-badge)

<br>

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Open_App-FF4B4B?style=for-the-badge)](https://huggingface.co/spaces/mahabub-unlocked/customer-support-agent)
[![GitHub](https://img.shields.io/badge/💻_Source_Code-GitHub-black?style=for-the-badge&logo=github)](https://github.com/mdmahabubalambishal/customer-support-agent)
[![LinkedIn](https://img.shields.io/badge/👤_Connect-LinkedIn-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/md-mahabub-alam-bishal/)

<br>/

> **একটা intelligent AI agent যা Bengali, English, এবং Banglish এ customer queries handle করে — RAG, Web Search, এবং Smart Escalation দিয়ে automatically সঠিক response source এ route করে।**

</div>

---

## 🎯 Project Overview

This project implements a multi-node AI agent that intelligently routes customer queries through three layers:

**RAG Layer** — Searches company knowledge base first  
**Web Search Layer** — Falls back to internet search if knowledge base has no answer  
**Escalation Layer** — Escalates to human support team if no answer found anywhere  

---

## 🚀 Live Demo

**👉 [App Open করো](https://huggingface.co/spaces/mahabub-unlocked/customer-support-agent)**

| Feature | Description |
|---------|-------------|
| 🌐 Multilingual | Bengali, English, Banglish সব handle করে |
| 🔍 RAG Pipeline | Company knowledge base থেকে answer খোঁজে |
| 🌍 Web Search | Real-time internet search fallback |
| 🚨 Smart Escalation | Human support এ automatic ticket generate |
| 📊 Live Dashboard | Real-time stats ও conversation logs |

---

## 🏗️ Architecture
```
Customer Query (Bengali / English / Banglish)
        │
        ▼
┌───────────────────┐
│   Smart Router    │ ── User-specific query? ──→ [Escalate 🔴]
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│    RAG Node       │ ── Answer found? ──→ [Respond 🟢]
│  (ChromaDB)       │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Web Search Node  │ ── Answer found? ──→ [Respond 🔵]
│  (Tavily API)     │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Escalate Node 🔴 │ ── Unique Reference ID generate
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   Logger Node     │ ── conversations.json save
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│Streamlit Dashboard│ ── Live stats + conversation logs
└───────────────────┘
```

---

## ✨ Features

🌐 **Multilingual Support** — Bengali, English, Banglish queries automatically handled  
🔍 **RAG Pipeline** — ChromaDB vector store with multilingual embeddings  
🌍 **Web Search Fallback** — Tavily API for real-time internet search  
🚨 **Smart Escalation** — Automatic ticket generation with unique Reference ID  
📊 **Live Dashboard** — Real-time stats, resolution rate, conversation logs  
💬 **Language Detection** — Response language matches customer's language automatically  
🧠 **Smart Router** — Detects user-specific queries, routes directly to escalation  
📝 **Conversation Logger** — All conversations saved to JSON with timestamps  

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | LangGraph |
| LLM | Groq (LLaMA 3.1 8B Instant) |
| Vector Store | ChromaDB |
| Embeddings | paraphrase-multilingual-MiniLM-L12-v2 |
| Web Search | Tavily API |
| UI | Streamlit |
| Language | Python 3.11 |
| Deployment | Hugging Face Spaces |

---

## 📁 Project Structure
```
customer-support-agent/
│
├── 📄 app.py                       # Streamlit UI & Dashboard
├── 📄 graph.py                     # LangGraph workflow & all nodes
├── 📄 requirements.txt
├── 📄 .env                         # API keys (not committed)
├── 📄 .gitignore
│
├── 📁 vectorstore/
│   ├── __init__.py
│   └── setup_chroma.py             # ChromaDB setup & update functions
│
├── 📁 nodes/
│   └── __init__.py
│
├── 📁 data/                        # Knowledge base files
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
└── 📁 logs/
    └── conversations.json          # Conversation history
```

---

## 🚀 Getting Started

### Prerequisites
```
Python 3.11+
Groq API Key   → groq.com (Free)
Tavily API Key → tavily.com (Free)
```

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/mdmahabubalambishal/customer-support-agent.git
cd customer-support-agent
```

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

`.env` file বানাও project root এ —
```env
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
```
┌─────────────────────────────────────────────────┐
│  🤖 Customer Support AI Agent — Dashboard       │
│                                                 │
│  💬 Total    │ 🟢 Resolved  │ 🔴 Escalated     │
│     47       │     38       │      9            │
│                                                 │
│  Resolution Rate ████████████████░░░░  81%      │
│                                                 │
│  Source Breakdown:                              │
│  🟢 Knowledge Base  ███████████████  32 (68%)   │
│  🔵 Web Search      ████████         9  (19%)   │
│  🔴 Escalated       ████             6  (13%)   │
│                                                 │
│  📝 Recent Conversations (expandable)           │
└─────────────────────────────────────────────────┘
```

- **Total Conversations** counter
- **Source Breakdown** — RAG vs Web vs Escalated
- **Resolution Rate** progress bar
- **Recent Conversations** with expandable details
- **Clear Chat** and **Refresh** controls

---

## 🔍 How Routing Works
```
Step 1 → Smart Router
         User-specific query detect করে
         (order ID, account, refund mention)
         → Yes: Escalate immediately 🔴

Step 2 → RAG Node
         ChromaDB knowledge base search করে
         Similarity threshold check
         → Answer found: Respond 🟢

Step 3 → Web Search Node
         Tavily API দিয়ে internet search
         Real-time data fetch
         → Answer found: Respond 🔵

Step 4 → Escalation Node
         Unique Reference ID generate করে
         Human support team notify করে 🔴

Step 5 → Logger Node
         conversations.json এ save করে
         Dashboard update হয়
```

---

## 🔧 Adding New Knowledge

নতুন topic knowledge base এ যোগ করতে —

**1. `data/` folder এ নতুন `.txt` file বানাও:**
```
## Topic Title

Detailed information about the topic.
Include multiple sentences for better context.

Keywords: keyword1, keyword2, বাংলা কীওয়ার্ড, banglish keyword

---
```

**2. Existing vector store delete করো:**
```bash
rd /s /q chroma_db     # Windows
rm -rf chroma_db       # Mac/Linux
```

**3. App restart করো** — automatically rebuild হবে।

---

## ⚙️ Configuration

Key settings in `graph.py` —
```python
# Knowledge base থেকে কতটা document retrieve করবে
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Web search results কতটা নেবে
results = tavily.search(query=state["query"], max_results=3)

# LLM model selection
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
```

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Knowledge Base response time | ~1-2 seconds |
| Web Search response time | ~2-4 seconds |
| Routing accuracy | ~85-90% |
| Languages supported | Bengali, English, Banglish |
| Knowledge base topics | 9 categories |

---

## 💡 What I Learned
```
✅ LangGraph Agent Architecture
   Multi-node graph design
   Conditional edge routing
   State management across nodes

✅ RAG Pipeline
   ChromaDB vector store setup
   Multilingual embeddings
   Similarity search tuning

✅ Multilingual LLM
   Language detection
   Response language matching
   Bengali/Banglish handling

✅ Tool Integration
   Tavily web search API
   Groq LLM inference
   ChromaDB retrieval

✅ Production Agent
   Smart escalation logic
   Conversation logging
   Real-time dashboard
```

---

## 🗺️ Roadmap
```
✅ Phase 1 — Core Agent (DONE)
   LangGraph + RAG + Web Search + Escalation

✅ Phase 2 — Multilingual Support (DONE)
   Bengali + English + Banglish

✅ Phase 3 — Dashboard (DONE)
   Real-time stats + conversation logs

⏳ Phase 4 — Advanced Features
   □ Voice input support
   □ Email notification on escalation
   □ Admin panel for knowledge base management
   □ Analytics export (PDF/Excel)

⏳ Phase 5 — MLOps
   □ Response quality monitoring
   □ Automated knowledge base updates
   □ A/B testing different LLMs
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

<div align="center">

**Md Mahabub Alam Bishal**
*AI/ML Engineer | LLM & Generative AI Enthusiast*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/md-mahabub-alam-bishal/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github)](https://github.com/mdmahabubalambishal)
[![HuggingFace](https://img.shields.io/badge/🤗_HuggingFace-Follow-FFD21E?style=for-the-badge)](https://huggingface.co/mahabub-unlocked)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=for-the-badge&logo=gmail)](mailto:mdmahabubalambishal@gmail.com)

</div>

## 🙏 Acknowledgements

- [LangChain](https://langchain.com/) — LLM framework
- [LangGraph](https://langchain-ai.github.io/langgraph/) — Agent orchestration
- [Groq](https://groq.com/) — Fast LLM inference
- [Tavily](https://tavily.com/) — AI-powered web search
- [ChromaDB](https://www.trychroma.com/) — Vector database
- [Streamlit](https://streamlit.io/) — UI framework
- [Hugging Face](https://huggingface.co/) — Embeddings & deployment

---

<div align="center">

⭐ **এই project টা useful লাগলে GitHub এ Star দাও!**

*Made with ❤️ by Mahabub*

**Live Demo:** [huggingface.co/spaces/mahabub-unlocked/customer-support-agent](https://huggingface.co/spaces/mahabub-unlocked/customer-support-agent)  
**GitHub:** [github.com/mdmahabubalambishal/customer-support-agent](https://github.com/mdmahabubalambishal/customer-support-agent)

</div>