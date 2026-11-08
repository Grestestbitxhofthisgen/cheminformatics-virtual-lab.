import streamlit as st

from ui import card, hero, section_title

hero(
    "Cheminformatics Virtual Lab",
    "Explore molecules.<br>Beautifully simple.",
    "Visualise structures, calculate drug-likeness, search by similarity and explore compound datasets — all in your browser.",
)

_, mid, _ = st.columns([1, 1.2, 1])
with mid:
    st.page_link("pages/1_Molecule_Viewer.py", label="Get started  →", icon="🔬")

section_title("Everything you need")
tools = [
    ("🔬", "Molecule Viewer", "Paste a SMILES string and see crisp 2D depictions or an interactive 3D model.", "pages/1_Molecule_Viewer.py"),
    ("⚗️", "Property Calculator", "Molecular weight, LogP, TPSA, H-bond donors and acceptors with a Lipinski rule-of-five check.", "pages/2_Property_Calculator.py"),
    ("🧬", "Similarity Search", "Rank a compound library against your query using Tanimoto similarity and several fingerprints.", "pages/3_Similarity_Search.py"),
    ("📊", "Dataset Explorer", "Upload CSV or SDF files, filter by properties and explore interactive Plotly charts.", "pages/4_Dataset_Explorer.py"),
]
cols = st.columns(2)
for i, (icon, title, body, target) in enumerate(tools):
    with cols[i % 2]:
        st.markdown(card(icon, title, body), unsafe_allow_html=True)
        st.page_link(target, label=f"Open {title}")
        st.write("")
