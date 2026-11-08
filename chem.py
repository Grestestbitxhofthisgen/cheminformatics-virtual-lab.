"""Cheminformatics helpers (RDKit). Heavy functions are cached with st.cache_data."""
from __future__ import annotations

import io
from typing import Optional

import numpy as np
import pandas as pd
import streamlit as st
from rdkit import Chem, DataStructs, RDLogger
from rdkit.Chem import AllChem, Crippen, Descriptors, Lipinski, MACCSkeys, QED, rdMolDescriptors
from rdkit.Chem import rdFingerprintGenerator as rfg
from rdkit.Chem.Draw import rdMolDraw2D

RDLogger.DisableLog("rdApp.*")

MAX_ROWS = 5000
FP_TYPES = ["Morgan (ECFP-like)", "RDKit topological", "Atom pair", "MACCS keys"]


def parse_smiles(smiles: str) -> Optional[Chem.Mol]:
    smiles = (smiles or "").strip()
    if not smiles:
        return None
    return Chem.MolFromSmiles(smiles)


@st.cache_data(show_spinner=False)
def mol_svg(smiles: str, width: int = 420, height: int = 320) -> Optional[str]:
    mol = parse_smiles(smiles)
    if mol is None:
        return None
    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    drawer.drawOptions().clearBackground = False
    rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol)
    drawer.FinishDrawing()
    return drawer.GetDrawingText()


def _props(mol: Chem.Mol) -> dict:
    mw = Descriptors.MolWt(mol)
    logp = Crippen.MolLogP(mol)
    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)
    violations = int(mw > 500) + int(logp > 5) + int(hbd > 5) + int(hba > 10)
    return {
        "Formula": rdMolDescriptors.CalcMolFormula(mol),
        "MW": round(mw, 2),
        "LogP": round(logp, 2),
        "TPSA": round(rdMolDescriptors.CalcTPSA(mol), 2),
        "HBD": hbd,
        "HBA": hba,
        "RotBonds": rdMolDescriptors.CalcNumRotatableBonds(mol),
        "Rings": rdMolDescriptors.CalcNumRings(mol),
        "HeavyAtoms": mol.GetNumHeavyAtoms(),
        "QED": round(QED.qed(mol), 3),
        "Lipinski violations": violations,
        "Lipinski pass": violations <= 1,
    }


@st.cache_data(show_spinner=False)
def compute_properties(smiles: str) -> Optional[dict]:
    mol = parse_smiles(smiles)
    return None if mol is None else _props(mol)


@st.cache_data(show_spinner=False)
def molblock_3d(smiles: str, optimize: bool = True) -> Optional[str]:
    mol = parse_smiles(smiles)
    if mol is None:
        return None
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    if AllChem.EmbedMolecule(mol, params) != 0:
        return None
    if optimize:
        try:
            AllChem.MMFFOptimizeMolecule(mol, maxIters=500)
        except Exception:
            pass
    return Chem.MolToMolBlock(mol)


def make_fp(mol: Chem.Mol, fp_type: str, radius: int = 2, nbits: int = 2048):
    if fp_type.startswith("Morgan"):
        return rfg.GetMorganGenerator(radius=radius, fpSize=nbits).GetFingerprint(mol)
    if fp_type.startswith("RDKit"):
        return rfg.GetRDKitFPGenerator(fpSize=nbits).GetFingerprint(mol)
    if fp_type.startswith("Atom"):
        return rfg.GetAtomPairGenerator(fpSize=nbits).GetFingerprint(mol)
    return MACCSkeys.GenMACCSKeys(mol)


@st.cache_data(show_spinner=False)
def fingerprint_bits(smiles: str, fp_type: str, radius: int, nbits: int) -> Optional[list]:
    mol = parse_smiles(smiles)
    return None if mol is None else list(make_fp(mol, fp_type, radius, nbits).GetOnBits())


@st.cache_data(show_spinner=False)
def similarity_table(query: str, names: tuple, smiles: tuple, fp_type: str, radius: int, nbits: int) -> pd.DataFrame:
    qmol = parse_smiles(query)
    if qmol is None:
        return pd.DataFrame()
    qfp = make_fp(qmol, fp_type, radius, nbits)
    rows, fps = [], []
    for n, s in zip(names, smiles):
        m = parse_smiles(s)
        if m is None:
            continue
        rows.append((n, s))
        fps.append(make_fp(m, fp_type, radius, nbits))
    if not fps:
        return pd.DataFrame()
    sims = DataStructs.BulkTanimotoSimilarity(qfp, fps)
    df = pd.DataFrame(rows, columns=["Name", "SMILES"])
    df["Tanimoto"] = np.round(sims, 4)
    return df.sort_values("Tanimoto", ascending=False).reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_table(data: bytes, filename: str) -> pd.DataFrame:
    """Read a CSV/TSV or SDF upload into a DataFrame (raises ValueError on bad input)."""
    name = filename.lower()
    if name.endswith(".sdf"):
        supplier = Chem.ForwardSDMolSupplier(io.BytesIO(data))
        rows = []
        for i, mol in enumerate(supplier):
            if mol is None:
                continue
            row = {"Name": mol.GetProp("_Name") if mol.HasProp("_Name") and mol.GetProp("_Name") else f"mol_{i+1}",
                   "SMILES": Chem.MolToSmiles(mol)}
            row.update({k: v for k, v in mol.GetPropsAsDict().items() if k not in row})
            rows.append(row)
            if len(rows) >= MAX_ROWS:
                break
        if not rows:
            raise ValueError("No valid molecules found in the SDF file.")
        return pd.DataFrame(rows)
    if name.endswith((".csv", ".tsv", ".txt")):
        sep = "\t" if name.endswith(".tsv") else None
        df = pd.read_csv(io.BytesIO(data), sep=sep, engine="python", nrows=MAX_ROWS)
        if df.empty:
            raise ValueError("The file is empty.")
        return df
    raise ValueError("Unsupported file type. Please upload a .csv, .tsv or .sdf file.")


def guess_smiles_column(df: pd.DataFrame) -> Optional[str]:
    for c in df.columns:
        if "smiles" in str(c).lower():
            return c
    return None


@st.cache_data(show_spinner=False)
def enrich(df: pd.DataFrame, smiles_col: str) -> tuple[pd.DataFrame, int]:
    """Append computed properties; returns (valid-rows dataframe, number of invalid rows)."""
    out, bad = [], 0
    for _, r in df.iterrows():
        p = compute_properties(str(r[smiles_col]))
        if p is None:
            bad += 1
            continue
        out.append({**r.to_dict(), **p})
    return pd.DataFrame(out), bad
