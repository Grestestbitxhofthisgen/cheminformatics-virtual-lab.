import pandas as pd
import streamlit as st

from chem import compute_properties, parse_smiles
from sample_data import SAMPLES
from ui import chip, hero, section_title

hero("Property Calculator", "Know your molecule.", "Physicochemical descriptors and a Lipinski rule-of-five drug-likeness check.", compact=True)

choice = st.selectbox("Start from an example", ["Custom"] + list(SAMPLES))
smiles = st.text_input("SMILES", value=SAMPLES.get(choice, ""), placeholder="Paste a SMILES string")

if not smiles.strip():
    st.info("Enter a SMILES string to calculate properties.")
    st.stop()
if parse_smiles(smiles) is None:
    st.error("Invalid SMILES. Please check the string and try again.")
    st.stop()

with st.spinner("Calculating…"):
    p = compute_properties(smiles.strip())

section_title("Descriptors")
r1 = st.columns(4)
r1[0].metric("Molecular weight", p["MW"], help="g/mol")
r1[1].metric("LogP (Crippen)", p["LogP"])
r1[2].metric("TPSA", p["TPSA"], help="Å²")
r1[3].metric("QED", p["QED"], help="Quantitative estimate of drug-likeness (0–1)")
r2 = st.columns(4)
r2[0].metric("H-bond donors", p["HBD"])
r2[1].metric("H-bond acceptors", p["HBA"])
r2[2].metric("Rotatable bonds", p["RotBonds"])
r2[3].metric("Rings", p["Rings"])

section_title("Lipinski rule of five")
rules = [
    ("MW ≤ 500", p["MW"] <= 500, p["MW"]),
    ("LogP ≤ 5", p["LogP"] <= 5, p["LogP"]),
    ("HBD ≤ 5", p["HBD"] <= 5, p["HBD"]),
    ("HBA ≤ 10", p["HBA"] <= 10, p["HBA"]),
]
st.markdown("".join(chip(f'{"✓" if ok else "✗"} {name}', ok) for name, ok, _ in rules), unsafe_allow_html=True)
if p["Lipinski violations"] == 0:
    st.success("No violations — the molecule satisfies Lipinski's rule of five.")
elif p["Lipinski pass"]:
    st.success("One violation — still generally considered drug-like (≤ 1 violation).")
else:
    st.warning(f'{p["Lipinski violations"]} violations — likely poor oral bioavailability.')

df = pd.DataFrame([{"SMILES": smiles.strip(), **p}])
st.download_button("Download results (CSV)", df.to_csv(index=False), file_name="properties.csv", mime="text/csv")
