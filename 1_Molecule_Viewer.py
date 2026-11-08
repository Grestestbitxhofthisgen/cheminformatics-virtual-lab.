import streamlit as st
import streamlit.components.v1 as components
import py3Dmol

from chem import compute_properties, mol_svg, molblock_3d, parse_smiles
from sample_data import SAMPLES
from ui import hero

hero("Molecule Viewer", "See any molecule.", "Enter a SMILES string to render its 2D structure or an interactive 3D model.", compact=True)

left, right = st.columns([1, 1.25], gap="large")

with left:
    choice = st.selectbox("Start from an example", ["Custom"] + list(SAMPLES))
    smiles = st.text_input("SMILES", value=SAMPLES.get(choice, ""), placeholder="e.g. CC(=O)Oc1ccccc1C(=O)O")
    mode = st.segmented_control("View", ["2D", "3D"], default="2D") or "2D"
    style = "Ball & stick"
    if mode == "3D":
        style = st.selectbox("3D style", ["Ball & stick", "Stick", "Sphere", "Line"])

mol = parse_smiles(smiles)

with right:
    if not smiles.strip():
        st.info("Enter a SMILES string to begin.")
    elif mol is None:
        st.error("That doesn't look like a valid SMILES string. Check brackets, ring numbers and atom symbols.")
    elif mode == "2D":
        svg = mol_svg(smiles.strip())
        st.markdown(f'<div class="panel">{svg}</div>', unsafe_allow_html=True)
        st.download_button("Download SVG", svg, file_name="molecule.svg", mime="image/svg+xml")
    else:
        with st.spinner("Generating 3D conformer…"):
            block = molblock_3d(smiles.strip())
        if block is None:
            st.error("Could not generate a 3D conformer for this molecule.")
        else:
            styles = {
                "Ball & stick": {"stick": {"radius": 0.15}, "sphere": {"scale": 0.28}},
                "Stick": {"stick": {}},
                "Sphere": {"sphere": {}},
                "Line": {"line": {}},
            }
            view = py3Dmol.view(width=640, height=440)
            view.addModel(block, "mol")
            view.setStyle(styles[style])
            view.setBackgroundColor("white")
            view.zoomTo()
            components.html(view._make_html(), height=460, scrolling=False)
            st.download_button("Download MOL file", block, file_name="molecule.mol", mime="chemical/x-mdl-molfile")

if mol is not None:
    p = compute_properties(smiles.strip())
    st.write("")
    c = st.columns(4)
    c[0].metric("Formula", p["Formula"])
    c[1].metric("Mol. weight", f'{p["MW"]}')
    c[2].metric("LogP", f'{p["LogP"]}')
    c[3].metric("Heavy atoms", p["HeavyAtoms"])
