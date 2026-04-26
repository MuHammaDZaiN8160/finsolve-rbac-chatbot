import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(
    page_title="FinSolve AI Assistant",
    page_icon="💼",
    layout="wide"
)

# Custom styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .role-badge {
        background-color: #1f77b4;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">💼 FinSolve Internal AI Assistant</p>', unsafe_allow_html=True)

# Sidebar login
with st.sidebar:
    st.header("🔐 Login")
    
    if "token" not in st.session_state:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            if username and password:
                try:
                    res = requests.post(
                        f"{API}/auth/login",
                        json={"username": username, "password": password}
                    )
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state["token"] = data["token"]
                        st.session_state["role"] = data["role"]
                        st.session_state["username"] = data["username"]
                        st.session_state["messages"] = []
                        st.success(f"Welcome, {data['username']}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                except Exception as e:
                    st.error(f"Cannot connect to server: {e}")
            else:
                st.warning("Please enter username and password")
    else:
        st.success(f"✅ Logged in")
        st.info(f"**User:** {st.session_state['username']}")
        st.info(f"**Role:** {st.session_state['role'].upper()}")
        
        st.markdown("---")
        st.markdown("**Test Accounts:**")
        st.code("""
tony.sharma    → c_level
alice.finance  → finance
bob.hr         → hr
carol.mkt      → marketing
dave.eng       → engineering
emp.general    → employee

Password: pass123
        """)
        
        if st.button("Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# Main chat area
if "token" not in st.session_state:
    st.info("👈 Please login from the sidebar to start chatting.")
    
    st.markdown("### 👥 Available Roles")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**💰 Finance**\nFinancial reports, expenses")
        st.markdown("**📣 Marketing**\nCampaigns, sales metrics")
    with col2:
        st.markdown("**👥 HR**\nEmployee data, payroll")
        st.markdown("**⚙️ Engineering**\nTech docs, guidelines")
    with col3:
        st.markdown("**👑 C-Level**\nFull access to all data")
        st.markdown("**🙋 Employee**\nGeneral info, policies")
else:
    # Initialize messages
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    # Display chat history
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("sources"):
                with st.expander("📄 Source Documents"):
                    for s in msg["sources"]:
                        st.write(f"• {s}")
    
    # Chat input
    if query := st.chat_input("Ask anything based on your role..."):
        # Show user message
        st.session_state["messages"].append({
            "role": "user",
            "content": query
        })
        with st.chat_message("user"):
            st.write(query)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    res = requests.post(
                        f"{API}/chat",
                        json={
                            "query": query,
                            "token": st.session_state["token"]
                        }
                    )
                    if res.status_code == 200:
                        data = res.json()
                        st.write(data["answer"])
                        if data["sources"]:
                            with st.expander("📄 Source Documents"):
                                for s in data["sources"]:
                                    st.write(f"• {s}")
                        st.session_state["messages"].append({
                            "role": "assistant",
                            "content": data["answer"],
                            "sources": data["sources"]
                        })
                    elif res.status_code == 401:
                        st.error("Session expired. Please login again.")
                        st.session_state.clear()
                    else:
                        st.error("Something went wrong. Please try again.")
                except Exception as e:
                    st.error(f"Cannot connect to server: {e}")