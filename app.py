import io
import requests
import pandas as pd
import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Manila Salary Dashboard", layout="centered")
st.title("🇵🇭 Manila Salary Benchmark")
st.markdown("Weighted salary estimation (**80% Government + 20% Market Data**)")

DBM_OFFICIAL_URL = "https://www.dbm.gov.ph/wp-content/uploads/Issuances/2025/National-Budget-Circular/NBC-No.-597.pdf"
NWPC_OFFICIAL_URL = "https://nwpc.dole.gov.ph/summary-of-current-regional-daily-minimum-wage-rates-non-agriculture-agriculture-and-other-wage-categories/"
PSA_OWS_URL = "https://psada.psa.gov.ph/catalog/237/data-dictionary?vcode=0SaY"

# -----------------------------
# Helpers
# -----------------------------
@st.cache_data
def load_csv_from_url(url: str) -> pd.DataFrame:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))

def load_csv(uploaded_file, url_text):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    if url_text.strip():
        return load_csv_from_url(url_text.strip())
    return None

def normalize_columns(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df

def lookup_salary(schedule_df, sg, step):
    row = schedule_df.loc[schedule_df["SalaryGrade"] == int(sg)]
    if row.empty:
        raise ValueError(f"SalaryGrade {sg} not found in DBM schedule.")
    col = f"Step{int(step)}"
    if col not in schedule_df.columns:
        raise ValueError(f"{col} column not found in DBM schedule.")
    return float(row.iloc[0][col])

# -----------------------------
# Sidebar - Adjustment
# -----------------------------
st.sidebar.header("⚙️ Adjustment")
multiplier = st.sidebar.slider("Salary Multiplier", 0.3, 1.5, 1.0, 0.01)
use_median = st.sidebar.checkbox("Use All Jobs Median")

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Data Input")

dbm_upload = st.sidebar.file_uploader("DBM Salary Schedule CSV", type=["csv"], key="dbm")
dbm_url = st.sidebar.text_input("DBM Salary Schedule CSV URL", value="")

map_upload = st.sidebar.file_uploader("Job ↔ Salary Grade Mapping CSV", type=["csv"], key="map")
map_url = st.sidebar.text_input("Job Mapping CSV URL", value="")

market_upload = st.sidebar.file_uploader("Market Salary CSV", type=["csv"], key="market")
market_url = st.sidebar.text_input("Market Salary CSV URL", value="")

st.sidebar.markdown("---")
st.sidebar.subheader("🏙 NCR / Manila Adjustment")
apply_ncr_floor = st.sidebar.checkbox("Apply NCR minimum wage floor to Entry")
ncr_daily_floor = st.sidebar.number_input(
    "NCR Daily Minimum Wage (PHP)",
    min_value=0,
    value=0,
    step=1,
    help="Enter manually from the official NWPC page if you want to apply a Manila/NCR floor."
)

# -----------------------------
# Load data
# -----------------------------
try:
    schedule_df = load_csv(dbm_upload, dbm_url)
    mapping_df = load_csv(map_upload, map_url)
    market_df = load_csv(market_upload, market_url)
except Exception as e:
    st.error(f"Failed to load CSV: {e}")
    st.stop()

if schedule_df is None or mapping_df is None or market_df is None:
    st.info(
        "Load 3 CSV files to run this app:\n"
        "1) DBM salary schedule CSV\n"
        "2) Job mapping CSV\n"
        "3) Market salary CSV"
    )
    st.markdown(f"""
### Required CSV structure

**1. DBM Salary Schedule CSV**
- Columns:
`SalaryGrade, Step1, Step2, Step3, Step4, Step5, Step6, Step7, Step8`

**2. Job Mapping CSV**
- Columns:
`Job, Entry_sg, Entry_step, Exp_sg, Exp_step, Mng_sg, Mng_step`

**3. Market Salary CSV**
- Columns:
`Job, Entry_non, Exp_non, Mng_non, non_url`

**Official references**
- DBM salary schedule: {DBM_OFFICIAL_URL}
- PSA OWS metadata: {PSA_OWS_URL}
- NWPC NCR wage reference: {NWPC_OFFICIAL_URL}
""")
    st.stop()

schedule_df = normalize_columns(schedule_df)
mapping_df = normalize_columns(mapping_df)
market_df = normalize_columns(market_df)

required_schedule_cols = ["SalaryGrade"] + [f"Step{i}" for i in range(1, 9)]
required_mapping_cols = ["Job", "Entry_sg", "Entry_step", "Exp_sg", "Exp_step", "Mng_sg", "Mng_step"]
required_market_cols = ["Job", "Entry_non", "Exp_non", "Mng_non", "non_url"]

for col in required_schedule_cols:
    if col not in schedule_df.columns:
        st.error(f"DBM schedule CSV is missing column: {col}")
        st.stop()

for col in required_mapping_cols:
    if col not in mapping_df.columns:
        st.error(f"Job mapping CSV is missing column: {col}")
        st.stop()

for col in required_market_cols:
    if col not in market_df.columns:
        st.error(f"Market salary CSV is missing column: {col}")
        st.stop()

# -----------------------------
# Build gov salary columns from DBM schedule
# -----------------------------
try:
    mapping_df["Entry_gov"] = mapping_df.apply(
        lambda r: lookup_salary(schedule_df, r["Entry_sg"], r["Entry_step"]), axis=1
    )
    mapping_df["Exp_gov"] = mapping_df.apply(
        lambda r: lookup_salary(schedule_df, r["Exp_sg"], r["Exp_step"]), axis=1
    )
    mapping_df["Mng_gov"] = mapping_df.apply(
        lambda r: lookup_salary(schedule_df, r["Mng_sg"], r["Mng_step"]), axis=1
    )
except Exception as e:
    st.error(f"Failed to map DBM salary schedule: {e}")
    st.stop()

mapping_df["gov_url"] = DBM_OFFICIAL_URL

# -----------------------------
# Merge
# -----------------------------
data = pd.merge(
    mapping_df[["Job", "Entry_gov", "Exp_gov", "Mng_gov", "gov_url"]],
    market_df[["Job", "Entry_non", "Exp_non", "Mng_non", "non_url"]],
    on="Job",
    how="inner"
)

if data.empty:
    st.error("No matching Job values found between Job Mapping CSV and Market Salary CSV.")
    st.stop()

# -----------------------------
# Calculation Function
# -----------------------------
def calc(gov, non):
    return (gov * 0.8 + non * 0.2) * multiplier

def apply_entry_floor(value):
    if apply_ncr_floor and ncr_daily_floor > 0:
        monthly_floor = ncr_daily_floor * 26
        return max(value, monthly_floor)
    return value

# -----------------------------
# Median or Single Job
# -----------------------------
if use_median:
    entry = calc(data["Entry_gov"].median(), data["Entry_non"].median())
    exp = calc(data["Exp_gov"].median(), data["Exp_non"].median())
    mng = calc(data["Mng_gov"].median(), data["Mng_non"].median())
    entry = apply_entry_floor(entry)
    title = "All Jobs Median"
    gov_source = DBM_OFFICIAL_URL
    market_source = PSA_OWS_URL
else:
    job = st.selectbox("💼 Select Job Role", data["Job"])
    row = data[data["Job"] == job].iloc[0]

    entry = calc(row["Entry_gov"], row["Entry_non"])
    exp = calc(row["Exp_gov"], row["Exp_non"])
    mng = calc(row["Mng_gov"], row["Mng_non"])
    entry = apply_entry_floor(entry)

    title = job
    gov_source = row["gov_url"]
    market_source = row["non_url"]

# -----------------------------
# Display
# -----------------------------
st.subheader(f"📊 {title} Salary (Monthly PHP)")

col1, col2, col3 = st.columns(3)
col1.metric("Entry Level", f"₱{entry:,.0f}")
col2.metric("Experienced", f"₱{exp:,.0f}")
col3.metric("Managerial", f"₱{mng:,.0f}")

# -----------------------------
# Chart
# -----------------------------
chart_data = pd.DataFrame({
    "Level": ["Entry", "Experienced", "Managerial"],
    "Salary": [entry, exp, mng]
}).set_index("Level")

st.bar_chart(chart_data)

# -----------------------------
# Sources
# -----------------------------
st.markdown("### 🔗 Sources")
st.write(f"**Government source:** {gov_source}")
st.write(f"**Market source:** {market_source}")
if apply_ncr_floor and ncr_daily_floor > 0:
    st.write(f"**NCR floor reference:** {NWPC_OFFICIAL_URL} (Manual daily floor: ₱{ncr_daily_floor:,.0f})")

# -----------------------------
# Debug / Preview
# -----------------------------
with st.expander("Preview merged dataset"):
    st.dataframe(data, use_container_width=True)
