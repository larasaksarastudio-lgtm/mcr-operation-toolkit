import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="MCR Dashboard - Unit Rental", page_icon="🚜", layout="wide")

st.title("🚜 Monitoring Control Room (MCR) - Unit Rental Dashboard")
st.markdown("Dashboard sederhana untuk memantau status aktivitas unit rental berdasarkan database lokal `mcr_data.db`.")

# Function to load data
@st.cache_data
def load_data():
    conn = sqlite3.connect("mcr_data.db")
    df = pd.read_sql_query("SELECT * FROM unit_rental", conn)
    conn.close()
    return df

df_units = load_data()

# Metric: Total Unit
total_units = len(df_units)
st.metric(label="Total Unit Rental", value=total_units)

st.markdown("---")

# Layout columns for charts and stats
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Distribusi Status Aktivitas Unit")
    status_counts = df_units["status_aktivitas"].value_counts().reset_index()
    status_counts.columns = ["Status", "Jumlah"]

    # Display Bar Chart using streamlit native bar_chart
    st.bar_chart(status_counts.set_index("Status"))

with col2:
    st.subheader("📋 Ringkasan Status")
    st.dataframe(status_counts, use_container_width=True)

st.markdown("---")

# Raw Data Table
st.subheader("📂 Raw Data: Tabel Unit Rental")
st.dataframe(df_units, use_container_width=True)
