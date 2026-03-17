import streamlit as st

st.set_page_config(
    page_title="AI Customer Support Agent",
    page_icon="🤖",
    layout="wide"
)

import json, os
os.makedirs("logs", exist_ok=True)

from vectorstore.setup_chroma import setup_vectorstore
if not os.path.exists("./chroma_db"):
    with st.spinner("🔧 Knowledge Base setup হচ্ছে... একটু অপেক্ষা করুন।"):
        setup_vectorstore()

from graph import agent, AgentState

st.markdown("""
<style>
    .user-bubble {
        background: #0084ff;
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 2px auto;
        max-width: 75%;
        width: fit-content;
        margin-left: auto;
        font-size: 15px;
        line-height: 1.5;
    }
    .bot-bubble {
        background: #f1f1f1;
        color: #1a1a1a;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px auto 2px 0;
        max-width: 75%;
        width: fit-content;
        font-size: 15px;
        line-height: 1.5;
    }
    .source-label {
        font-size: 11px;
        color: #888;
        margin-bottom: 12px;
        margin-left: 4px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

SOURCE_BADGES = {
    "rag":       "🟢 Knowledge Base",
    "web":       "🔵 Web Search",
    "escalated": "🔴 Escalated to Human"
}

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_input" not in st.session_state:
    st.session_state.pending_input = ""

chat_col, dashboard_col = st.columns([2, 1])

with chat_col:
    st.markdown("## 🤖 Customer Support AI Agent")
    st.caption("বাংলা • English • Banglish — সব ভাষায় সাহায্য করি")
    st.divider()

    if not st.session_state.messages:
        st.markdown(
            '<div class="bot-bubble">👋 আসসালামু আলাইকুম! বাংলা, English, বা Banglish — যেকোনো ভাষায় প্রশ্ন করুন।</div>',
            unsafe_allow_html=True
        )
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="user-bubble">👤 {msg["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                answer = msg["content"].replace("\n", "<br>")
                st.markdown(
                    f'<div class="bot-bubble">🤖 {answer}</div>',
                    unsafe_allow_html=True
                )
                badge = SOURCE_BADGES.get(msg.get("source", ""), "")
                st.markdown(
                    f'<div class="source-label">📌 {badge}</div>',
                    unsafe_allow_html=True
                )

    st.divider()

    st.markdown("**💡 Quick Examples:**")
    ex1, ex2, ex3, ex4 = st.columns(4)
    with ex1:
        if st.button("📦 Return policy"):
            st.session_state.pending_input = "Return policy কি?"
    with ex2:
        if st.button("🚚 Shipping charge"):
            st.session_state.pending_input = "Shipping charge koto?"
    with ex3:
        if st.button("💳 bKash payment"):
            st.session_state.pending_input = "bKash diye kivabe pay korbo?"
    with ex4:
        if st.button("❓ My order"):
            st.session_state.pending_input = "আমার order #12345 কোথায়?"

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            label="message",
            label_visibility="collapsed",
            value=st.session_state.pending_input,
            placeholder="আপনার প্রশ্ন লিখুন... (বাংলা / English / Banglish)"
        )
        send_btn = st.form_submit_button("Send 📤", use_container_width=True)

    if st.session_state.pending_input:
        st.session_state.pending_input = ""

    if send_btn and user_input.strip():
        st.session_state.messages.append({
            "role": "user",
            "content": user_input.strip()
        })

        with st.spinner("🤔 উত্তর খুঁজছি..."):
            state: AgentState = {
                "query": user_input.strip(),
                "original_query": user_input.strip(),
                "rag_answer": "",
                "web_answer": "",
                "final_answer": "",
                "source": "",
                "conversation_log": []
            }
            result = agent.invoke(state)

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["final_answer"],
            "source": result["source"]
        })

        st.rerun()

with dashboard_col:
    st.markdown("## 📊 Dashboard")
    st.divider()

    try:
        with open("logs/conversations.json", encoding="utf-8") as f:
            logs = json.load(f)
    except Exception:
        logs = []

    total = len(logs)
    rag_c = sum(1 for l in logs if l["source"] == "rag")
    web_c = sum(1 for l in logs if l["source"] == "web")
    esc_c = sum(1 for l in logs if l["source"] == "escalated")

    st.metric("💬 Total Conversations", total)

    c1, c2, c3 = st.columns(3)
    c1.metric("🟢 RAG", rag_c)
    c2.metric("🔵 Web", web_c)
    c3.metric("🔴 Escalated", esc_c)

    if total > 0:
        rate = round(((rag_c + web_c) / total) * 100)
        st.progress(rate / 100)
        st.caption(f"✅ Resolution Rate: {rate}%")

    st.divider()

    st.markdown("**🕐 Recent Conversations**")
    if not logs:
        st.info("এখনো কোনো conversation নেই।")
    else:
        for log in reversed(logs[-5:]):
            icon = {"rag": "🟢", "web": "🔵", "escalated": "🔴"}.get(log["source"], "⚪")
            short_q = log["query"][:35] + "..." if len(log["query"]) > 35 else log["query"]
            with st.expander(f"{icon} {short_q}"):
                st.caption(f"🕐 {log['timestamp'][:19]}")
                st.caption(f"📌 Source: {log['source']}")
                st.write(log["answer"][:200] + "..." if len(log["answer"]) > 200 else log["answer"])

    st.divider()

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()