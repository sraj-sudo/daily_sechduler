import streamlit as st
from db import init_db, get_connection
from utils import send_daily_update, send_telegram, get_daily_status

# ---------- CONFIG ----------
st.set_page_config(
    page_title="SSB Mission Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- INIT ----------
init_db()

# ---------- UI ----------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #e6edf3;
}
.block-container {
    padding: 1rem;
}
.stButton>button {
    background-color: #1f6feb;
    color: white;
    border-radius: 10px;
    width: 100%;
}
h1, h2, h3 {
    color: #58a6ff;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN ----------
def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.title("🔐 SSB Dashboard Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            st.session_state.authenticated = True
            st.session_state.user = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

    return False


if not login():
    st.stop()

user = st.session_state.user

# ---------- SIDEBAR ----------
st.sidebar.title("🪖 SSB Control Panel")
st.sidebar.success(f"👤 {user}")

st.sidebar.markdown("### 📡 Telegram Controls")

if st.sidebar.button("📤 Send Daily Status"):
    send_daily_update(user)
    st.sidebar.success("Sent to Telegram!")

if st.sidebar.button("📊 Get Status Preview"):
    msg = get_daily_status(user)
    st.sidebar.text(msg)

if st.sidebar.button("🚀 Send Motivation"):
    send_telegram("🔥 Stay consistent. SSB is a process. Keep pushing!")
    st.sidebar.success("Motivation sent!")

# ---------- MAIN ----------
st.title("✈️ SSB Mission Dashboard")

conn = get_connection()
cursor = conn.cursor()

# ---------- METRICS ----------
cursor.execute("SELECT COUNT(*) FROM tasks WHERE user=?", (user,))
total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed=1 AND user=?", (user,))
completed = cursor.fetchone()[0]

progress = (completed / total * 100) if total > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("📋 Total Tasks", total)
col2.metric("✅ Completed", completed)
col3.metric("📈 Progress", f"{progress:.1f}%")

# ---------- NEXT DAY PLAN ----------
st.subheader("📅 Tomorrow's Plan")

cursor.execute("SELECT task, focus FROM schedule WHERE user=?", (user,))
plans = cursor.fetchall()

if plans:
    for p in plans:
        st.write(f"• {p[0]} ({p[1]})")
else:
    st.info("No plan set yet")

# ---------- QUICK SEND ----------
st.subheader("⚡ Quick Telegram Update")

if st.button("Send Tomorrow Plan 🔔"):
    if plans:
        msg = "📅 Tomorrow's Plan:\n\n"
        for p in plans:
            msg += f"• {p[0]} ({p[1]})\n"
    else:
        msg = "⚠️ No tasks planned for tomorrow"

    send_telegram(msg)
    st.success("Plan sent to Telegram!")

conn.close()

# ---------- FOOTER ----------
st.markdown("---")
st.caption("🚀 Discipline = Selection")