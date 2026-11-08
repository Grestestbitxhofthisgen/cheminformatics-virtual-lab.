import io

import pandas as pd
import plotly.express as px
import streamlit as st

from chem import FP_TYPES, MAX_ROWS, fingerprint_bits, guess_smiles_column, mol_svg, parse_smiles, similarity_table
from sample_data import SAMPLES
from ui import hero, section_title

hero("Similarity Search", "Find look-alikes.", "Rank a compound library against a query molecule using Tanimoto similarity.", compact=True)

c1, c2 = st.columns([1.4, 1], gap="large")
with c1:
    choice = st.selectbox("Query example", ["Custom"] + list(SAMPLES), index=1)
    query = st.text_input("Query SMILES", value=SAMPLES.get(choice, ""))
with c2:
    fp_type = st.selectbox("Fingerprint", FP_TYPES)
    radius, nbits = 2, 2048
    if fp_type.startswith("Morgan"):
        radius = st.slider("Morgan radius", 1, 4, 2)
    if not fp_type.startswith("MACCS"):
        nbits = st.select_slider("Bits", [512, 1024, 2048, 4096], value=2048)

source = st.segmented_control("Library", ["Built-in drugs", "Paste SMILES", "Upload CSV"], default="Built-in drugs") or "Built-in drugs"
names, smiles_list = [], []
if source == "Built-in drugs":
    names, smiles_list = list(SAMPLES), list(SAMPLES.values())
elif source == "Paste SMILES":
    txt = st.text_area("One per line — optionally `SMILES name`", height=150, placeholder="CCO ethanol\nc1ccccc1 benzene")
    for i, line in enumerate(l for l in txt.splitlines() if l.strip()):
        parts = line.split(None, 1)
        smiles_list.append(parts[0])
        names.append(parts[1] if len(parts) > 1 else f"mol_{i+1}")
else:
    up = st.file_uploader("CSV with a SMILES column", type=["csv"])
    if up:
        try:
            df_up = pd.read_csv(io.BytesIO(up.getvalue()), nrows=MAX_ROWS)
            col = guess_smiles_column(df_up)
            if col is None:
                st.error("No column containing 'smiles' in its name was found.")
            else:
                name_col = next((c for c in df_up.columns if str(c).lower() in ("name", "id", "compound")), None)
                smiles_list = df_up[col].astype(str).tolist()
                names = df_up[name_col].astype(str).tolist() if name_col else [f"mol_{i+1}" for i in range(len(df_up))]
        except Exception as e:
            st.error(f"Could not read the file: {e}")

if not query.strip():
    st.info("Enter a query SMILES to start.")
    st.stop()
if parse_smiles(query) is None:
    st.error("The query SMILES is invalid.")
    st.stop()
if not smiles_list:
    st.info("Provide a library to search.")
    st.stop()

with st.spinner("Computing fingerprints…"):
    res = similarity_table(query.strip(), tuple(names), tuple(smiles_list), fp_type, radius, nbits)
if res.empty:
    st.error("None of the library SMILES could be parsed.")
    st.stop()
skipped = len(smiles_list) - len(res)
if skipped:
    st.warning(f"{skipped} invalid SMILES were skipped.")

top_n = st.slider("Show top N", 3, min(30, len(res)), min(10, len(res))) if len(res) > 3 else len(res)
top = res.head(top_n)

section_title("Results")
fig = px.bar(top.iloc[::-1], x="Tanimoto", y="Name", orientation="h", color="Tanimoto",
             color_continuous_scale=["#D2D2D7", "#0071E3"], range_x=[0, 1])
fig.update_layout(height=max(300, 34 * top_n), margin=dict(l=0, r=0, t=10, b=0), coloraxis_showscale=False,
                  plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif"))
st.plotly_chart(fig, width="stretch")

st.dataframe(top, width="stretch", hide_index=True)
st.download_button("Download full ranking (CSV)", res.to_csv(index=False), file_name="similarity.csv", mime="text/csv")

section_title("Closest structures")
cols = st.columns(3)
for i, row in top.head(6).iterrows():
    with cols[i % 3]:
        st.markdown(f'<div class="panel">{mol_svg(row["SMILES"], 260, 200)}<b>{row["Name"]}</b><br>'
                    f'<span style="color:#6E6E73">Tanimoto {row["Tanimoto"]:.2f}</span></div>', unsafe_allow_html=True)
        st.write("")

with st.expander("Fingerprint bits of the query"):
    bits = fingerprint_bits(query.strip(), fp_type, radius, nbits)
    st.write(f"{len(bits)} bits set")
    st.code(", ".join(map(str, bits)) or "—")
