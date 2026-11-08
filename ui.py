"""Shared Apple-style UI helpers: CSS, hero, cards, footer."""
import streamlit as st

FOOTER_TEXT = "Created by Allen V Abraham | RA2611026050103 | Section: AIML B"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root{
  --bg:#FBFBFD; --surface:#FFFFFF; --text:#1D1D1F; --text2:#6E6E73;
  --accent:#0071E3; --accent-hover:#0077ED; --border:#D2D2D7; --soft:#F5F5F7;
  --radius:18px;
}
html, body, [class*="css"], .stApp, button, input, textarea, select{
  font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text","Inter","Helvetica Neue",Arial,sans-serif !important;
  -webkit-font-smoothing:antialiased;
}
.stApp{background:var(--bg); color:var(--text);}
section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"]{display:none !important;}

/* sticky translucent top nav */
header[data-testid="stHeader"]{
  background:rgba(251,251,253,.72) !important;
  backdrop-filter:saturate(180%) blur(20px);
  -webkit-backdrop-filter:saturate(180%) blur(20px);
  border-bottom:1px solid rgba(210,210,215,.6);
}
header[data-testid="stHeader"] a, header[data-testid="stHeader"] button{
  border-radius:980px !important; transition:all .2s ease; color:var(--text) !important;
}
header[data-testid="stHeader"] a:hover{background:var(--soft) !important;}

.block-container{max-width:1080px; padding-top:3.5rem; padding-bottom:2rem;}
#MainMenu, footer{visibility:hidden;}

/* hero */
.hero{text-align:center; padding:4.5rem 1rem 3rem;}
.hero.compact{padding:2rem 1rem 1.5rem; text-align:left;}
.eyebrow{color:var(--accent); font-weight:600; font-size:1.05rem; letter-spacing:.01em; margin-bottom:.4rem;}
.hero h1{font-size:clamp(2.4rem,6vw,4.4rem); font-weight:800; letter-spacing:-.035em; line-height:1.05; margin:0 0 1rem; color:var(--text);}
.hero.compact h1{font-size:clamp(2rem,4vw,2.8rem);}
.hero p{font-size:clamp(1.05rem,2vw,1.4rem); color:var(--text2); font-weight:400; max-width:720px; margin:0 auto; line-height:1.45;}
.hero.compact p{margin:0;}

/* cards */
.card{background:var(--surface); border:1px solid rgba(210,210,215,.55); border-radius:var(--radius);
  padding:1.6rem 1.5rem; box-shadow:0 2px 12px rgba(0,0,0,.04); transition:transform .25s ease, box-shadow .25s ease; height:100%;}
.card:hover{transform:translateY(-4px); box-shadow:0 12px 32px rgba(0,0,0,.09);}
.card .icon{font-size:2rem; margin-bottom:.6rem;}
.card h3{font-size:1.25rem; font-weight:700; margin:0 0 .4rem; letter-spacing:-.01em;}
.card p{color:var(--text2); font-size:.97rem; line-height:1.5; margin:0;}

/* buttons: pill */
.stButton>button, .stDownloadButton>button, [data-testid="stPageLink"] a{
  border-radius:980px !important; padding:.5rem 1.4rem !important; font-weight:500 !important;
  border:1px solid var(--border) !important; background:var(--surface) !important; color:var(--text) !important;
  transition:all .2s ease !important;}
.stButton>button:hover, .stDownloadButton>button:hover, [data-testid="stPageLink"] a:hover{
  border-color:var(--accent) !important; color:var(--accent) !important;}
.stButton>button[kind="primary"]{background:var(--accent) !important; color:#fff !important; border-color:var(--accent) !important;}
.stButton>button[kind="primary"]:hover{background:var(--accent-hover) !important; color:#fff !important;}

/* inputs */
.stTextInput input, .stTextArea textarea, .stNumberInput input, div[data-baseweb="select"]>div{
  border-radius:12px !important; border:1px solid var(--border) !important; background:var(--surface) !important;}
.stTextInput input:focus, .stTextArea textarea:focus{border-color:var(--accent) !important; box-shadow:0 0 0 4px rgba(0,113,227,.15) !important;}
[data-testid="stFileUploader"] section{border-radius:var(--radius) !important; border:1.5px dashed var(--border) !important; background:var(--surface) !important;}

/* metrics & dataframes */
[data-testid="stMetric"]{background:var(--surface); border:1px solid rgba(210,210,215,.55); border-radius:16px; padding:1rem 1.2rem; box-shadow:0 2px 10px rgba(0,0,0,.03);}
[data-testid="stMetricLabel"]{color:var(--text2);}
[data-testid="stDataFrame"]{border-radius:14px; overflow:hidden; border:1px solid rgba(210,210,215,.55);}
[data-testid="stExpander"]{border-radius:14px; border:1px solid rgba(210,210,215,.55); background:var(--surface);}

/* panels & chips */
.panel{background:var(--surface); border:1px solid rgba(210,210,215,.55); border-radius:var(--radius); padding:1rem; box-shadow:0 2px 12px rgba(0,0,0,.04); text-align:center;}
.chip{display:inline-block; padding:.25rem .8rem; border-radius:980px; font-size:.85rem; font-weight:600; margin:.15rem .25rem .15rem 0;}
.chip.ok{background:#E8F7ED; color:#1B7F3B;} .chip.bad{background:#FDECEC; color:#C62828;}
.section-title{font-size:1.6rem; font-weight:700; letter-spacing:-.02em; margin:2.2rem 0 1rem;}

/* footer */
.app-footer{margin-top:4rem; padding:1.4rem 0 1rem; border-top:1px solid var(--border); text-align:center; color:var(--text2); font-size:.78rem; letter-spacing:.01em;}

@media (max-width:640px){ .hero{padding:2.5rem .5rem 1.5rem;} .block-container{padding-left:1rem; padding-right:1rem;} }
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def hero(eyebrow: str, title: str, subtitle: str, compact: bool = False) -> None:
    cls = "hero compact" if compact else "hero"
    st.markdown(
        f'<div class="{cls}"><div class="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def card(icon: str, title: str, body: str) -> str:
    return f'<div class="card"><div class="icon">{icon}</div><h3>{title}</h3><p>{body}</p></div>'


def section_title(text: str) -> None:
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def chip(text: str, ok: bool) -> str:
    return f'<span class="chip {"ok" if ok else "bad"}">{text}</span>'


def footer() -> None:
    st.markdown(f'<div class="app-footer">{FOOTER_TEXT}</div>', unsafe_allow_html=True)
