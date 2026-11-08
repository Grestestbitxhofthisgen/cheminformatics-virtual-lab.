import streamlit as st

from ui import card, hero, section_title

hero("About", "Built with care.", "An independent, open-source cheminformatics toolkit for learning and quick exploration.", compact=True)

section_title("Under the hood")
c = st.columns(3)
for col, (icon, t, b) in zip(c, [
    ("⚛️", "RDKit", "Parsing, descriptors, fingerprints and 2D/3D structure generation."),
    ("📈", "Plotly", "Interactive, responsive charts for exploring compound sets."),
    ("🧊", "py3Dmol", "WebGL molecular visualisation embedded directly in the page."),
]):
    col.markdown(card(icon, t, b), unsafe_allow_html=True)

section_title("Notes")
st.markdown(
    """
- LogP uses the Crippen method; TPSA and other descriptors come from RDKit.
- Lipinski compliance is reported as *pass* when there is at most one violation.
- 3D coordinates are generated with ETKDG and optimised with MMFF — they are illustrative, not a docking-quality conformer search.
- Uploads are processed in memory and not stored.
"""
)
st.caption("For educational use only. Not intended for clinical or regulatory decisions.")
