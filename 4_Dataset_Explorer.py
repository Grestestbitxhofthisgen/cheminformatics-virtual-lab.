import pandas as pd
import plotly.express as px
import streamlit as st

from chem import MAX_ROWS, enrich, guess_smiles_column, load_table
from sample_data import SAMPLES
from ui import hero, section_title

hero("Dataset Explorer", "Understand your data.", "Upload a CSV or SDF, compute properties and filter and plot interactively.", compact=True)

src = st.segmented_control("Data source", ["Sample set", "Upload file"], default="Sample set") or "Sample set"
raw = None
if src == "Sample set":
    raw = pd.DataFrame({"Name": list(SAMPLES), "SMILES": list(SAMPLES.values())})
else:
    up = st.file_uploader("CSV, TSV or SDF (max 50 MB, first 5,000 rows used)", type=["csv", "tsv", "sdf"])
    if up is None:
        st.info("Upload a file to begin, or switch to the sample set.")
        st.stop()
    try:
        with st.spinner("Reading file…"):
            raw = load_table(up.getvalue(), up.name)
    except Exception as e:
        st.error(f"Could not read the file: {e}")
        st.stop()

guess = guess_smiles_column(raw)
cols = list(raw.columns)
smiles_col = st.selectbox("SMILES column", cols, index=cols.index(guess) if guess in cols else 0)

with st.spinner("Computing properties…"):
    df, bad = enrich(raw.head(MAX_ROWS), smiles_col)
if df.empty:
    st.error("No valid molecules found. Pick a different SMILES column.")
    st.stop()
if bad:
    st.warning(f"{bad} rows with invalid SMILES were skipped.")

section_title("Filters")
f1, f2, f3 = st.columns(3)
mw_lo, mw_hi = float(df["MW"].min()), float(df["MW"].max())
lp_lo, lp_hi = float(df["LogP"].min()), float(df["LogP"].max())
mw = f1.slider("Molecular weight", mw_lo, mw_hi, (mw_lo, mw_hi)) if mw_lo < mw_hi else (mw_lo, mw_hi)
lp = f2.slider("LogP", lp_lo, lp_hi, (lp_lo, lp_hi)) if lp_lo < lp_hi else (lp_lo, lp_hi)
only_lip = f3.toggle("Lipinski-compliant only")

mask = df["MW"].between(*mw) & df["LogP"].between(*lp)
if only_lip:
    mask &= df["Lipinski pass"]
view = df[mask]

m = st.columns(3)
m[0].metric("Molecules shown", f"{len(view):,}", f"of {len(df):,}", delta_color="off")
m[1].metric("Mean MW", f'{view["MW"].mean():.1f}' if len(view) else "—")
m[2].metric("Lipinski pass", f'{view["Lipinski pass"].mean()*100:.0f}%' if len(view) else "—")

if view.empty:
    st.warning("No molecules match the current filters.")
    st.stop()

section_title("Charts")
layout = dict(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif"),
              margin=dict(l=0, r=0, t=40, b=0))
hover = [c for c in view.columns if c not in ("Lipinski pass",)][:1]
t1, t2, t3 = st.tabs(["MW vs LogP", "Distribution", "Compare"])
with t1:
    fig = px.scatter(view, x="MW", y="LogP", color=view["Lipinski pass"].map({True: "Pass", False: "Fail"}),
                     hover_name=hover[0], size="TPSA", size_max=18,
                     color_discrete_map={"Pass": "#0071E3", "Fail": "#FF3B30"}, title="Chemical space")
    fig.update_layout(**layout, legend_title_text="Lipinski")
    st.plotly_chart(fig, width="stretch")
with t2:
    prop = st.selectbox("Property", ["MW", "LogP", "TPSA", "HBD", "HBA", "RotBonds", "QED"])
    fig = px.histogram(view, x=prop, nbins=25, color_discrete_sequence=["#0071E3"], title=f"{prop} distribution")
    fig.update_layout(**layout, bargap=0.06)
    st.plotly_chart(fig, width="stretch")
with t3:
    a, b = st.columns(2)
    xa = a.selectbox("X axis", ["MW", "LogP", "TPSA", "HBD", "HBA", "RotBonds", "QED"], index=2)
    yb = b.selectbox("Y axis", ["MW", "LogP", "TPSA", "HBD", "HBA", "RotBonds", "QED"], index=6)
    fig = px.density_heatmap(view, x=xa, y=yb, nbinsx=15, nbinsy=15, color_continuous_scale=["#F5F5F7", "#0071E3"])
    fig.update_layout(**layout)
    st.plotly_chart(fig, width="stretch")

section_title("Data")
st.dataframe(view, width="stretch", hide_index=True)
st.download_button("Download filtered data (CSV)", view.to_csv(index=False), file_name="filtered_molecules.csv", mime="text/csv")
