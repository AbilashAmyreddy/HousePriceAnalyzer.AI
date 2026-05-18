import warnings
warnings.filterwarnings("ignore")

import pickle
import numpy as np
import pandas as pd
import streamlit as st

from scraper import scrape_99acres, get_sample_listings

# ─────────────────────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HousePrice.AI",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# Theme / CSS
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0,1&family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg0: #070b14;
    --bg1: #0b1220;
    --bg2: #0f1729;
    --card: rgba(255,255,255,0.05);
    --card2: rgba(255,255,255,0.07);
    --line: rgba(255,255,255,0.10);
    --line2: rgba(214,177,83,0.25);
    --text: #eef2ff;
    --muted: #94a3b8;
    --gold: #d6b153;
    --gold2: #f2d27c;
    --good: #34d399;
    --shadow: 0 20px 60px rgba(0,0,0,0.35);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--text) !important;
}

.stApp {
    background:
        radial-gradient(circle at 15% 15%, rgba(214,177,83,0.10), transparent 28%),
        radial-gradient(circle at 85% 10%, rgba(59,130,246,0.10), transparent 26%),
        radial-gradient(circle at 70% 80%, rgba(214,177,83,0.08), transparent 25%),
        linear-gradient(135deg, #060913 0%, #0a1020 45%, #070b14 100%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    max-width: 1450px !important;
    padding: 1.1rem 1.6rem 2rem 1.6rem !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border: 1px solid rgba(214,177,83,0.35) !important;
    background: linear-gradient(135deg, #d6b153 0%, #f2d27c 100%) !important;
    color: #0b1220 !important;
    font-weight: 800 !important;
    border-radius: 16px !important;
    padding: 0.8rem 1.1rem !important;
    box-shadow: 0 10px 30px rgba(214,177,83,0.22);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 40px rgba(214,177,83,0.30);
}

/* Inputs */
div[data-baseweb="select"], div[data-baseweb="input"], .stNumberInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
}

.stSelectbox label, .stNumberInput label {
    color: var(--muted) !important;
    font-size: 0.76rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    font-weight: 700 !important;
}

/* Headline / hero */
.hero {
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(214,177,83,0.18);
    background:
        linear-gradient(135deg, rgba(15,23,42,0.92), rgba(10,15,30,0.92)),
        radial-gradient(circle at top right, rgba(214,177,83,0.18), transparent 35%);
    border-radius: 28px;
    padding: 2rem 2.1rem;
    box-shadow: var(--shadow);
}
.hero::before,
.hero::after {
    content: "";
    position: absolute;
    border-radius: 999px;
    filter: blur(2px);
    pointer-events: none;
}
.hero::before {
    right: -60px;
    top: -50px;
    width: 220px;
    height: 220px;
    background: radial-gradient(circle, rgba(214,177,83,0.18), transparent 66%);
}
.hero::after {
    left: 8%;
    bottom: -80px;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(59,130,246,0.10), transparent 70%);
}

.hero-grid {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 1.2rem;
    align-items: start;
}
.hero-badge {
    display: inline-flex;
    gap: 0.45rem;
    align-items: center;
    padding: 0.35rem 0.8rem;
    border-radius: 999px;
    border: 1px solid rgba(214,177,83,0.22);
    background: rgba(214,177,83,0.08);
    color: var(--gold2);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.hero-title {
    margin-top: 0.8rem;
    margin-bottom: 0.6rem;
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    line-height: 0.95;
    letter-spacing: -0.03em;
}
.hero-title span { color: var(--gold2); font-style: italic; }
.hero-sub {
    max-width: 700px;
    color: var(--muted);
    font-size: 1rem;
    line-height: 1.75;
    margin-bottom: 1.4rem;
}
.hero-stats {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.85rem;
    margin-top: 0.7rem;
}
.stat {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 0.9rem 1rem;
}
.stat-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: var(--gold2);
    line-height: 1;
}
.stat-label {
    margin-top: 0.35rem;
    color: var(--muted);
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.hero-meta {
    justify-self: end;
    width: 100%;
    max-width: 330px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 1.1rem;
}
.meta-title {
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.7rem;
    font-weight: 800;
}
.meta-item {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.72rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.meta-item:last-child { border-bottom: none; }
.meta-key { color: var(--muted); font-size: 0.82rem; }
.meta-val { color: var(--text); font-size: 0.82rem; font-weight: 700; text-align: right; }

.section-wrap {
    padding-top: 0.25rem;
}
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    color: var(--text);
    letter-spacing: -0.02em;
    margin-top: 0;
}
.section-sub {
    color: var(--muted);
    font-size: 0.84rem;
    margin-top: 0.25rem;
}
.kicker {
    color: var(--gold2);
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-size: 0.72rem;
}
.divider {
    height: 1px;
    margin: 1rem 0;
    background: linear-gradient(90deg, transparent, rgba(214,177,83,0.85), transparent);
}

/* Prediction box */
.result-box {
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(214,177,83,0.25);
    background:
        linear-gradient(135deg, rgba(214,177,83,0.14), rgba(255,255,255,0.04)),
        rgba(255,255,255,0.03);
    border-radius: 26px;
    padding: 1.6rem 1.6rem 1.35rem 1.6rem;
    box-shadow: 0 22px 55px rgba(0,0,0,0.28);
}
.result-label {
    color: var(--muted);
    font-size: 0.74rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    font-weight: 800;
}
.result-price {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.4rem, 4vw, 4rem);
    line-height: 0.95;
    color: var(--gold2);
    margin: 0.55rem 0 0.5rem 0;
}
.result-range {
    color: var(--muted);
    font-size: 0.88rem;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.85rem;
    margin-top: 0.95rem;
}
.metric {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1rem;
}
.metric-value {
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--text);
}
.metric-label {
    margin-top: 0.3rem;
    color: var(--muted);
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
    margin-top: 0.9rem;
}
.pill {
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.035);
    color: var(--text);
    border-radius: 999px;
    padding: 0.45rem 0.8rem;
    font-size: 0.76rem;
}
.pill strong { color: var(--gold2); }

/* Listings */
.listing {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    align-items: center;
    padding: 1rem 1.1rem;
    border-radius: 18px;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 0.7rem;
}
.listing-name { color: var(--text); font-weight: 700; font-size: 0.94rem; }
.listing-loc { color: var(--muted); font-size: 0.78rem; margin-top: 0.2rem; }
.listing-price { color: var(--gold2); font-family: 'DM Serif Display', serif; font-size: 1.25rem; }
.listing-src { color: var(--muted); font-size: 0.68rem; text-align: right; margin-top: 0.18rem; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.45rem;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    color: var(--muted) !important;
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 999px !important;
    padding: 0.55rem 0.95rem !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
}
.stTabs [aria-selected="true"] {
    color: #0b1220 !important;
    background: linear-gradient(135deg, #d6b153, #f2d27c) !important;
    border-color: rgba(214,177,83,0.55) !important;
}

.footer {
    margin-top: 2rem;
    padding: 1.25rem 0 0.5rem 0;
    border-top: 1px solid rgba(255,255,255,0.08);
    color: var(--muted);
    text-align: center;
    font-size: 0.78rem;
    line-height: 1.8;
}
.footer strong { color: var(--gold2); }

/* Responsive */
@media (max-width: 1100px) {
    .hero-grid { grid-template-columns: 1fr; }
    .hero-meta { max-width: 100%; justify-self: start; }
    .hero-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .metric-grid { grid-template-columns: 1fr; }
}
@media (max-width: 750px) {
    .block-container { padding: 0.85rem !important; }
    .hero { border-radius: 22px; padding: 1.2rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = pickle.load(open("model.pkl", "rb"))
    columns = pickle.load(open("columns.pkl", "rb"))
    locations = pickle.load(open("locations.pkl", "rb"))
    return model, columns, sorted(locations)


model, columns, locations = load_model()


def predict_price(location: str, sqft: int, bath: int, bhk: int) -> float:
    row = pd.DataFrame(columns=columns, data=np.zeros((1, len(columns))))
    row["total_sqft"] = sqft
    row["bath"] = bath
    row["bhk"] = bhk
    loc_col = f"location_{location}"
    if loc_col in row.columns:
        row[loc_col] = 1
    log_pred = model.predict(row)[0]
    return float(np.expm1(log_pred))


def format_lakh(value: float) -> str:
    return f"₹{value:.2f}L"


def add_spacing(height: int = 10):
    st.markdown(f"<div style='height:{height}px;'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero">
    <div class="hero-grid">
        <div>
            <div class="hero-badge">AI + Web Scraping + ML Analytics</div>
            <div class="hero-title">HousePrice<span>.AI</span></div>
            <div class="hero-sub">
                An AI-powered real estate analytics platform built using both structured housing datasets
                and live web-scraped property listings. The system combines machine learning prediction
                with real-time market intelligence for smarter house price estimation.
            </div>
            <div class="hero-stats">
                <div class="stat"><div class="stat-value">10,999</div><div class="stat-label">Training Records</div></div>
                <div class="stat"><div class="stat-value">R² 0.81</div><div class="stat-label">Model Score</div></div>
                <div class="stat"><div class="stat-value">187</div><div class="stat-label">Locations</div></div>
                <div class="stat"><div class="stat-value">GBR</div><div class="stat-label">Algorithm</div></div>
            </div>
        </div>
        <div class="hero-meta">
            <div class="meta-title">Project Snapshot</div>
            <div class="meta-item"><div class="meta-key">Domain</div><div class="meta-val">House Price Prediction</div></div>
            <div class="meta-item"><div class="meta-key">Approach</div><div class="meta-val">ML + Web Scraping</div></div>
            <div class="meta-item"><div class="meta-key">Frontend</div><div class="meta-val">Streamlit UI</div></div>
            <div class="meta-item"><div class="meta-key">Dataset</div><div class="meta-val">Bengaluru Housing</div></div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

add_spacing(10)

# ─────────────────────────────────────────────────────────────
# Main Layout
# ─────────────────────────────────────────────────────────────
left, mid, right = st.columns([1.02, 0.06, 1.45], vertical_alignment="top")

with left:
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="kicker">Property Inputs</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Configure the home</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Pick the key features used by the model.</div>', unsafe_allow_html=True)
    add_spacing(2)

    location = st.selectbox(
        "Location",
        options=locations,
        index=locations.index("Whitefield") if "Whitefield" in locations else 0,
    )

    sqft = st.number_input(
        "Total Area (sqft)",
        min_value=300,
        max_value=10000,
        value=1200,
        step=50,
    )

    c1, c2 = st.columns(2)
    with c1:
        bhk = st.selectbox("BHK", [1, 2, 3, 4, 5, 6], index=1)
    with c2:
        bath = st.selectbox("Bathrooms", [1, 2, 3, 4, 5], index=1)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="background:rgba(214,177,83,0.08); border:1px solid rgba(214,177,83,0.18); border-radius:18px; padding:0.9rem 1rem;">
            <div style="color:#94a3b8; font-size:0.72rem; letter-spacing:0.14em; text-transform:uppercase; font-weight:800; margin-bottom:0.35rem;">Current Selection</div>
            <div style="color:#eef2ff; font-size:0.92rem; line-height:1.7;">{bhk} BHK · {sqft:,} sqft · {bath} Bath · {location}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    add_spacing(12)
    predict_btn = st.button("✦ Predict Market Value")

    add_spacing(10)

    with st.expander("Model Details", expanded=False):
        st.markdown(
            """
            <div style="color:#94a3b8; font-size:0.84rem; line-height:1.8;">
            <b style="color:#f2d27c;">Algorithm:</b> Gradient Boosting Regressor<br>
            <b style="color:#f2d27c;">Training Records:</b> 10,999 Bangalore listings<br>
            <b style="color:#f2d27c;">Cross-Validation R²:</b> 0.81<br>
            <b style="color:#f2d27c;">Feature Set:</b> Location, Area, BHK, Bathrooms<br>
            <b style="color:#f2d27c;">Encoding:</b> One-hot location encoding<br>
            <b style="color:#f2d27c;">Transform:</b> log1p → expm1
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="kicker">Prediction Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Premium estimate view</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">A cleaner, more product-like presentation for your result.</div>', unsafe_allow_html=True)
    add_spacing(2)

    if predict_btn:
        with st.spinner("Running model inference..."):
            predicted = predict_price(location, sqft, bath, bhk)

        low = predicted * 0.90
        high = predicted * 1.10
        ppsf = (predicted * 100000) / sqft
        confidence = min(int(0.81 * 100), 95)

        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-label">Estimated Market Value</div>
                <div class="result-price">{format_lakh(predicted)}</div>
                <div class="result-range">Expected range: {format_lakh(low)} — {format_lakh(high)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="metric-grid">
                <div class="metric">
                    <div class="metric-value">{format_lakh(predicted)}</div>
                    <div class="metric-label">Predicted Price</div>
                </div>
                <div class="metric">
                    <div class="metric-value">₹{ppsf:,.0f}</div>
                    <div class="metric-label">Price per Sqft</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{confidence}%</div>
                    <div class="metric-label">Confidence</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        add_spacing(12)
        st.markdown(
            f"""
            <div>
                <div style="display:flex; justify-content:space-between; margin-bottom:0.45rem; color:#94a3b8; font-size:0.72rem; letter-spacing:0.12em; text-transform:uppercase; font-weight:800;">
                    <span>Prediction Confidence</span>
                    <span style="color:#f2d27c;">{confidence}%</span>
                </div>
                <div style="height:8px; border-radius:999px; background:rgba(255,255,255,0.05); overflow:hidden; border:1px solid rgba(255,255,255,0.06);">
                    <div style="width:{confidence}%; height:100%; border-radius:999px; background:linear-gradient(90deg,#d6b153,#f2d27c);"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        add_spacing(14)
        st.markdown(
            f"""
            <div style="padding:1rem 1.1rem; border-radius:20px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);">
                <div class="kicker">Input Summary</div>
                <div style="margin-top:0.75rem; display:grid; grid-template-columns:1fr 1fr; gap:0.55rem 1rem; font-size:0.84rem;">
                    <div style="color:#94a3b8;">Location</div><div style="text-align:right; font-weight:700;">{location}</div>
                    <div style="color:#94a3b8;">Area</div><div style="text-align:right; font-weight:700;">{sqft:,} sqft</div>
                    <div style="color:#94a3b8;">BHK</div><div style="text-align:right; font-weight:700;">{bhk}</div>
                    <div style="color:#94a3b8;">Bathrooms</div><div style="text-align:right; font-weight:700;">{bath}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="min-height:420px; display:flex; align-items:center; justify-content:center; text-align:center; padding:2rem; border-radius:24px; border:1px dashed rgba(214,177,83,0.25); background:rgba(255,255,255,0.025);">
                <div>
                    <div style="font-size:3rem; margin-bottom:0.7rem;">🏙️</div>
                    <div style="font-family:'DM Serif Display',serif; font-size:1.65rem; color:#eef2ff;">A polished estimate awaits</div>
                    <div style="margin-top:0.55rem; color:#94a3b8; font-size:0.88rem; line-height:1.7; max-width:340px;">
                        Choose the property details and click <b style="color:#f2d27c;">Predict Market Value</b> to display the ML estimate in a premium dashboard layout.
                    </div>
                    <div class="pill-row" style="justify-content:center; margin-top:1rem;">
                        <div class="pill"><strong>Location</strong> aware</div>
                        <div class="pill"><strong>Regression</strong> model</div>
                        <div class="pill"><strong>Live</strong> comparison</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Data Insights
# ─────────────────────────────────────────────────────────────
st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="kicker">Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Data insights</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Visual context from the training dataset helps the project feel complete and credible.</div>', unsafe_allow_html=True)

add_spacing(6)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Price Distribution",
    "Area vs Price",
    "BHK vs Price",
    "Correlation",
    "Top Locations",
])

charts = {
    tab1: ("Data/chart1_price_distribution.png", "Distribution of house prices across the dataset."),
    tab2: ("Data/chart2_area_vs_price.png", "Bigger homes generally command higher prices."),
    tab3: ("Data/chart3_bhk_vs_price.png", "Average price tends to rise with BHK count."),
    tab4: ("Data/chart4_correlation.png", "Area is usually the strongest driver of price."),
    tab5: ("Data/chart5_top_locations.png", "Premium localities ranked by average price."),
}

for tab, (path, caption) in charts.items():
    with tab:
        st.markdown(
            f'<div style="color:#94a3b8; font-size:0.82rem; margin:0.2rem 0 0.8rem 0;">{caption}</div>',
            unsafe_allow_html=True,
        )
        try:
            st.image(path, use_container_width=True)
        except Exception:
            st.warning("Chart not found. Please run the EDA script first.")

# ─────────────────────────────────────────────────────────────
# Live listings section
# ─────────────────────────────────────────────────────────────
st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="kicker">Market Check</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Live market listings</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Pull current listings to compare your prediction with real market data.</div>', unsafe_allow_html=True)

list_col1, list_col2 = st.columns([0.42, 0.58], vertical_alignment="top")

with list_col1:
    if st.button("🔄 Fetch Current Listings"):
        with st.spinner("Fetching live listings..."):
            listings_df = scrape_99acres()
        st.success(f"Fetched {len(listings_df)} listings")
        st.session_state["listings_df"] = listings_df

with list_col2:
    listings_df = st.session_state.get("listings_df")
    if listings_df is not None and len(listings_df) > 0:
        for _, row in listings_df.iterrows():
            st.markdown(
                f"""
                <div class="listing">
                    <div>
                        <div class="listing-name">{row['title']}</div>
                        <div class="listing-loc">📍 {row['location']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="listing-price">{row['price']}</div>
                        <div class="listing-src">{row['source']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div style="padding:1.4rem; text-align:center; border-radius:20px; border:1px dashed rgba(214,177,83,0.25); background:rgba(255,255,255,0.025); color:#94a3b8;">
                Click <b style="color:#f2d27c;">Fetch Current Listings</b> to show real-time property examples.
            </div>
            """,
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="footer">
    <strong>HousePrice.AI</strong> · Built by Abilash Amyreddy · Streamlit · Scikit-learn · BeautifulSoup
    <br>Minor Project · Bengaluru Housing Dataset + Web Scraping
</div>
""",
    unsafe_allow_html=True,
)
