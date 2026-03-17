from typing import TypedDict, Literal
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from tavily import TavilyClient
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import json, os
from datetime import datetime

load_dotenv()

class AgentState(TypedDict):
    query: str
    original_query: str
    rag_answer: str
    web_answer: str
    final_answer: str
    source: str
    conversation_log: list

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
tavily = TavilyClient()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})


def detect_language(text: str):
    bengali_chars = sum(1 for c in text if '\u0980' <= c <= '\u09FF')
    banglish_words = [
        "ki", "koto", "ache", "chai", "hobe", "korte", "jabe",
        "dao", "nao", "bol", "amar", "apnar", "ami", "apni",
        "ta", "te", "ke", "theke", "korbo", "debo", "nibo"
    ]
    text_lower = text.lower()
    is_bengali = bengali_chars > 2
    is_banglish = (not is_bengali) and any(
        w in text_lower.split() for w in banglish_words
    )
    if is_bengali:
        return "bengali"
    elif is_banglish:
        return "banglish"
    else:
        return "english"


def smart_router_node(state: AgentState) -> AgentState:
    return {**state, "original_query": state["query"]}

def smart_router(state: AgentState) -> Literal["rag", "escalate"]:
    query_lower = state["query"].lower()
    original = state["query"]
    
    # English / Banglish specific keywords
    english_keywords = [
    "my order is", "my order was", "my order has",
    "my order number", "my refund", "my account",
    "my delivery", "my payment",
    "order id", "order #", "payment status"
]
    
    # Banglish specific keywords
    banglish_keywords = [
        "amar order", "amar refund", "amar account",
        "amar delivery", "amar payment"
    ]
    
    # Bengali Unicode check — "আমার" = \u0986\u09ae\u09be\u09b0
    bengali_keywords = [
    "আমার অর্ডার", "আমার রিফান্ড", "আমার একাউন্ট",
    "আমার ডেলিভারি", "আমার পেমেন্ট",
    "আমার অর্ডার cancel", "আমার delivery",
    "দুইবার কাটা", "block হয়েছে"
]
    
    if any(kw in query_lower for kw in english_keywords):
        return "escalate"
    if any(kw in query_lower for kw in banglish_keywords):
        return "escalate"
    if any(kw in original for kw in bengali_keywords):
        return "escalate"
    
    return "rag"


def rag_node(state: AgentState) -> AgentState:
    print("RAG Node: Knowledge base searching...")
    # Third-party / device questions সরাসরি web search এ পাঠাও
    query_lower = state["query"].lower()
    external_keywords = [
    "android", "iphone", "ios", "browser", "chrome", "firefox",
    "cache clear", "clear cache", "clear browser", "google", "samsung",
    "windows", "nagad", "bkash", "rocket", "pathao", "sundarban",
    "redx", "whatsapp", "facebook", "instagram", "youtube",
    "visa card kivabe", "visa card pabo", "mastercard kivabe",
    "google pay", "apple pay"
]
    if any(kw in query_lower for kw in external_keywords):
        print("RAG: External question, going to web search...")
        return {**state, "rag_answer": ""}
    docs = retriever.invoke(state["query"])

    if not docs:
        return {**state, "rag_answer": ""}

    context = "\n".join([d.page_content for d in docs])
    lang = detect_language(state["query"])

    if lang == "bengali":
        lang_instruction = "RESPOND IN BENGALI ONLY."
    elif lang == "banglish":
        lang_instruction = "RESPOND IN BANGLISH ONLY (English letters, Bengali meaning)."
    else:
        lang_instruction = "RESPOND IN ENGLISH ONLY."

    prompt = (
    "You are a customer support agent for a Bangladeshi e-commerce company.\n\n"
    "LANGUAGE: " + lang_instruction + "\n\n"
    "Knowledge base context:\n"
    + context + "\n\n"
    "Customer Question: " + state["query"] + "\n\n"
    "STRICT RULES:\n"
    "1. Read the context carefully.\n"
    "2. If the context contains a DIRECT answer to the question, answer clearly.\n"
    "3. If the context does NOT contain relevant information, respond with exactly: NOT_FOUND\n"
    "4. Do NOT make up answers. Do NOT use general knowledge. ONLY use the context above.\n"
    "5. If the question asks HOW TO DO something on a phone, browser, computer, or any device or third-party app (like Nagad, bKash, Android, iPhone, browser, Google, Samsung, WhatsApp) — respond with exactly: NOT_FOUND\n"
    "6. ONLY answer questions that are DIRECTLY about our company's products, policies, orders, shipping, payment, or account.\n"
    "Answer:"
)

    response = llm.invoke(prompt).content.strip()

    if "NOT_FOUND" in response.upper() or len(response) < 10:
        print("RAG: Not found, going to web search...")
        return {**state, "rag_answer": ""}

    return {**state, "rag_answer": response}


def web_search_node(state: AgentState) -> AgentState:
    print("Web Search Node: Searching internet...")
    try:
        results = tavily.search(query=state["query"], max_results=3)
        context = "\n".join([
            r["content"] for r in results.get("results", [])
        ])

        if not context:
            return {**state, "web_answer": ""}

        lang = detect_language(state["query"])

        if lang == "bengali":
            lang_instruction = "RESPOND IN BENGALI ONLY."
        elif lang == "banglish":
            lang_instruction = "RESPOND IN BANGLISH ONLY (English letters, Bengali meaning)."
        else:
            lang_instruction = "RESPOND IN ENGLISH ONLY."

        prompt = (
            "You are a customer support agent for a Bangladeshi e-commerce company.\n\n"
            "LANGUAGE: " + lang_instruction + "\n\n"
            "Web search results:\n"
            + context + "\n\n"
            "Customer Question: " + state["query"] + "\n\n"
            "STRICT RULES:\n"
            "1. Give a concise helpful answer based on search results.\n"
            "2. If results are completely irrelevant, respond with exactly: NOT_FOUND\n"
            "3. " + lang_instruction + "\n\n"
            "Answer:"
        )

        response = llm.invoke(prompt).content.strip()

        if "NOT_FOUND" in response.upper():
            return {**state, "web_answer": ""}

        return {**state, "web_answer": response}

    except Exception as e:
        print("Search error: " + str(e))
        return {**state, "web_answer": ""}


def escalation_node(state: AgentState) -> AgentState:
    print("Escalation Node: Sending to human agent...")
    ticket_id = "TICKET-" + datetime.now().strftime("%Y%m%d%H%M%S")
    lang = detect_language(state["query"])

    if lang == "bengali":
        msg = (
            "আমি দুঃখিত, আপনার প্রশ্নের সঠিক উত্তর দিতে পারছি না।\n\n"
            "আপনার সমস্যাটি আমাদের human support team এ পাঠানো হয়েছে।\n\n"
            "Response time: 2-4 ghontar modhye\n"
            "Reference ID: " + ticket_id + "\n\n"
            "যোগাযোগ: 16XXX\n"
            "Email: support@company.com"
        )
    elif lang == "banglish":
        msg = (
            "Sorry, apnar question er proper answer dite parchi na.\n\n"
            "Apnar problem amader human support team e pathano hoyeche.\n\n"
            "Response time: 2-4 ghontar modhye\n"
            "Reference ID: " + ticket_id + "\n\n"
            "Contact: 16XXX\n"
            "Email: support@company.com"
        )
    else:
        msg = (
            "I apologize, I could not find a satisfactory answer to your question.\n\n"
            "Your query has been escalated to our human support team.\n\n"
            "Expected response time: 2-4 hours\n"
            "Reference ID: " + ticket_id + "\n\n"
            "Contact: 16XXX\n"
            "Email: support@company.com"
        )

    return {**state, "final_answer": msg, "source": "escalated"}


def set_rag_response(state: AgentState) -> AgentState:
    return {**state, "final_answer": state["rag_answer"], "source": "rag"}

def set_web_response(state: AgentState) -> AgentState:
    return {**state, "final_answer": state["web_answer"], "source": "web"}


def logger_node(state: AgentState) -> AgentState:
    os.makedirs("logs", exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": state["original_query"],
        "answer": state["final_answer"],
        "source": state["source"]
    }
    try:
        with open("logs/conversations.json", "r", encoding="utf-8") as f:
            logs = json.load(f)
    except Exception:
        logs = []

    logs.append(log_entry)

    with open("logs/conversations.json", "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

    print("Logged | Source: " + state["source"])
    return state


def route_after_rag(state: AgentState) -> Literal["respond", "web_search"]:
    return "respond" if state["rag_answer"] else "web_search"

def route_after_web(state: AgentState) -> Literal["respond", "escalate"]:
    return "respond" if state["web_answer"] else "escalate"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("smart_router", smart_router_node)
    graph.add_node("rag", rag_node)
    graph.add_node("web_search", web_search_node)
    graph.add_node("escalate", escalation_node)
    graph.add_node("set_rag_response", set_rag_response)
    graph.add_node("set_web_response", set_web_response)
    graph.add_node("logger", logger_node)

    graph.set_entry_point("smart_router")

    graph.add_conditional_edges(
        "smart_router", smart_router,
        {"rag": "rag", "escalate": "escalate"}
    )
    graph.add_conditional_edges(
        "rag", route_after_rag,
        {"respond": "set_rag_response", "web_search": "web_search"}
    )
    graph.add_conditional_edges(
        "web_search", route_after_web,
        {"respond": "set_web_response", "escalate": "escalate"}
    )

    graph.add_edge("set_rag_response", "logger")
    graph.add_edge("set_web_response", "logger")
    graph.add_edge("escalate", "logger")
    graph.add_edge("logger", END)

    return graph.compile()


agent = build_graph()