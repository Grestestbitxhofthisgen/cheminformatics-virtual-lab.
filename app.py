"""Entry point: global config, Apple-style theme, top navigation and footer."""
import streamlit as st

from ui import footer, inject_css

st.set_page_config(
    page_title="Cheminformatics Virtual Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_css()

pages = [
    st.Page("pages/home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/1_Molecule_Viewer.py", title="Molecule Viewer", icon="🔬"),
    st.Page("pages/2_Property_Calculator.py", title="Properties", icon="⚗️"),
    st.Page("pages/3_Similarity_Search.py", title="Similarity", icon="🧬"),
    st.Page("pages/4_Dataset_Explorer.py", title="Datasets", icon="📊"),
    st.Page("pages/5_About.py", title="About", icon="ℹ️"),
]
nav = st.navigation(pages, position="top")
nav.run()
footer()
