import streamlit as st
from utils import load_json, save_json
import dashboard

# Ensure set_page_config is the first thing called
st.set_page_config(page_title="Homework", page_icon="📓")

st.write("# Manage Homework")

col1, col2 = st.columns([1, 2])

# Column 1: Add new homework
with col1:
    st.write("## Add New Homework")
    dashboard.add_manual_homework()

# Column 2: Display all Homework
with col2:
    st.write("## All Homework")
    dashboard.display_homework()
