import streamlit as st
import pandas as pd
from db import get_connection

st.title("📊 Performance Analytics")

conn = get_connection()

df = pd.read_sql("SELECT * FROM tasks", conn)

if df.empty:
    st.warning("No data yet")
    st.stop()

# ---------- SCORE ----------
df["final"] = (
    df["self_score"] +
    df["mentor_score"] +
    df["olq_score"]
) / 3

# ---------- METRICS ----------
st.metric("🔥 Avg Score", round(df["final"].mean(), 2))
st.metric("✅ Completion Rate", f"{(df['completed'].mean()*100):.1f}%")

# ---------- CHARTS ----------
st.subheader("📈 Score Trend")
st.line_chart(df["final"])

st.subheader("📊 Focus Distribution")
st.bar_chart(df["focus"].value_counts())