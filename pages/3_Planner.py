import streamlit as st
from db import get_connection

st.title("📅 Next Day Planner")

conn = get_connection()

task = st.text_input("Task")
focus = st.selectbox("Focus", ["Screening", "Psychology", "GTO", "Interview"])

if st.button("Add Plan"):
    conn.execute("INSERT INTO schedule (task, focus) VALUES (?, ?)", (task, focus))
    conn.commit()
    st.success("Added")

rows = conn.execute("SELECT * FROM schedule").fetchall()

for r in rows:
    st.write(f"• {r[1]} ({r[2]})")