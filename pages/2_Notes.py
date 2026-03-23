import streamlit as st
from db import get_connection
from datetime import datetime

st.title("📝 Daily Notes")

conn = get_connection()

date = st.date_input("Date", datetime.today())
note = st.text_area("Write your reflection")

if st.button("Save"):
    conn.execute("INSERT INTO notes (date, content) VALUES (?, ?)", (date, note))
    conn.commit()
    st.success("Saved")

# SHOW
rows = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()

for r in rows:
    st.write(f"**{r[1]}** - {r[2]}")