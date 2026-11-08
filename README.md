# 🧪 Cheminformatics Virtual Lab

An Apple-style, multipage Streamlit app for exploring molecules: structure viewing (2D/3D), property calculation with Lipinski checks, Tanimoto similarity search and an interactive dataset explorer.

**Live app:** _add your Streamlit URL here_

## Screenshots
| Home | Molecule Viewer |
|---|---|
| ![Home](docs/screenshots/home.png) | ![Viewer](docs/screenshots/viewer.png) |
| **Properties** | **Dataset Explorer** |
| ![Props](docs/screenshots/properties.png) | ![Datasets](docs/screenshots/datasets.png) |

_(Take screenshots of the running app and save them in `docs/screenshots/` with the names above.)_

## Features
- **Molecule Viewer** – SMILES → 2D SVG (RDKit) or interactive 3D (py3Dmol); SVG / MOL download
- **Property Calculator** – MW, LogP, TPSA, HBD/HBA, rotatable bonds, QED, Lipinski rule of five; CSV download
- **Similarity Search** – Morgan, RDKit, atom-pair and MACCS fingerprints; Tanimoto ranking; Plotly chart; CSV download
- **Dataset Explorer** – CSV/TSV/SDF upload, property filters, Plotly charts, filtered CSV download
- Input validation with friendly errors, `st.cache_data` caching, spinners

## Project structure
```
app.py                  # entry point: config, theme CSS, top navigation, footer
ui.py                   # Apple-style CSS + hero/card/footer helpers
chem.py                 # RDKit logic (cached)
sample_data.py          # built-in demo molecules
pages/                  # home + 4 tools + about
.streamlit/config.toml  # theme
requirements.txt, packages.txt
```

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate   # Python 3.11
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
1. Push this repo to GitHub (public).
2. Go to <https://share.streamlit.io> → **Create app** → **Deploy a public app from GitHub**.
3. Repo: `cheminformatics-virtual-lab`, branch `main`, main file `app.py`.
4. Under **Advanced settings** choose **Python 3.11**, then Deploy.

---
Created by Allen V Abraham | RA2611026050103 | Section: AIML B
