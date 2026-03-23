import streamlit as st
import pandas as pd
from db import get_connection
from datetime import datetime

st.title("📊 Daily Tracker")

conn = get_connection()

# ---------- ADD TASK ----------
with st.sidebar:
    st.header("Add Task")

    date = st.date_input("Date", datetime.today())
    task = st.text_input("Task")
    focus = st.selectbox("Focus", ["Screening", "Psychology", "GTO", "Interview"])

    if st.button("Add"):
        conn.execute("""
        INSERT INTO tasks (date, task, focus, completed, self_score, mentor_score, olq_score, notes, improvement)
        VALUES (?, ?, ?, 0, 0, 0, 0, '', '')
        """, (date, task, focus))
        conn.commit()
        st.success("Task Added")

# ---------- LOAD ----------
df = pd.read_sql("SELECT * FROM tasks", conn)

if not df.empty:
    edited = st.data_editor(df, use_container_width=True)

    # SAVE BACK
    for _, row in edited.iterrows():
        conn.execute("""
        UPDATE tasks SET
            date=?, task=?, focus=?, completed=?,
            self_score=?, mentor_score=?, olq_score=?,
            notes=?, improvement=?
        WHERE id=?
        """, (
            row["date"], row["task"], row["focus"], row["completed"],
            row["self_score"], row["mentor_score"], row["olq_score"],
            row["notes"], row["improvement"], row["id"]
        ))

    conn.commit()

    # SCORE
    edited["final"] = (
        edited["self_score"] +
        edited["mentor_score"] +
        edited["olq_score"]
    ) / 3

    st.metric("📊 Avg Score", round(edited["final"].mean(), 2))