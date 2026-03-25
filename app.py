import streamlit as st
from textwrap import dedent

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Salary Dashboard",
    page_icon="📊",
    layout="wide",
)

# -----------------------------
# Text（多言語）
# -----------------------------
TEXT = {
    "ja": {
        "lang": "表示言語",
        "region": "地区選択",
        "coef_mode": "係数の決め方",
        "manual": "手入力",
        "min_wage": "最低賃金比率",
        "blended": "最低賃金＋物価",
        "entry_label": "Entry（G6, G5）",
        "supervisor_label": "Supervisor（G4）",
        "manager_label": "Manager（G3）",
        "summary": "給与レンジ（地区補正後）",
    },
    "en": {
        "lang": "Language",
        "region": "Select Region",
        "coef_mode": "Coefficient Method",
        "manual": "Manual",
        "min_wage": "Min Wage Ratio",
        "blended": "Min Wage + Price",
        "entry_label": "Entry (G6, G5)",
        "supervisor_label": "Supervisor (G4)",
        "manager_label": "Manager (G3)",
        "summary": "Salary Range (Adjusted)",
    },
}

# -----------------------------
# Manila baseline
# -----------------------------
BASE_RANGES = {
    "Entry": (16000, 23000),
    "Supervisor": (28000, 40000),
    "Manager": (50000, 70000),
}

# -----------------------------
# 地区データ（最低賃金）
# -----------------------------
REGIONS = {
    "Manila": 695,
    "Davao": 525,
    "Tawi-Tawi": 386,
    "General Santos": 460,
}

# -----------------------------
# Helper
# -----------------------------
def fmt(v):
    return f"₱{v:,.0f}"

def fmt_range(a, b):
    return f"{fmt(a)} - {fmt(b)}"

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    lang = st.radio(TEXT["ja"]["lang"], ["ja", "en"], format_func=lambda x: "日本語" if x=="ja" else "English")
    T = TEXT[lang]

    region = st.selectbox(T["region"], list(REGIONS.keys()))

    mode = st.radio(T["coef_mode"], [T["manual"], T["min_wage"], T["blended"]])

    manual_coef = st.number_input("Coefficient", 0.1, 3.0, 1.0, 0.05)

    price_index = st.number_input("Price Index (Manila=1)", 0.1, 3.0, 1.0, 0.01)

# -----------------------------
# 係数計算
# -----------------------------
manila = REGIONS["Manila"]
selected = REGIONS[region]

ratio = selected / manila

if mode == T["manual"]:
    coef = manual_coef
elif mode == T["min_wage"]:
    coef = ratio
else:
    coef = (ratio + price_index) / 2

# -----------------------------
# スケーリング
# -----------------------------
scaled = {
    k: (v[0] * coef, v[1] * coef)
    for k, v in BASE_RANGES.items()
}

# -----------------------------
# UI
# -----------------------------
st.title("📊 Salary Dashboard")

st.metric("Applied Coefficient", f"{coef:.2f}x")

st.subheader(T["summary"])

label_map = {
    "Entry": T["entry_label"],
    "Supervisor": T["supervisor_label"],
    "Manager": T["manager_label"],
}

col1, col2, col3 = st.columns(3)

for col, level in zip([col1, col2, col3], ["Entry", "Supervisor", "Manager"]):
    low, high = scaled[level]
    with col:
        st.markdown(f"""
        ### {label_map[level]}
        **{fmt_range(low, high)}**
        """)

st.markdown("---")

# -----------------------------
# 補足説明
# -----------------------------
st.markdown(dedent("""
### ロジック
- Manila（NCR）を基準給与とする
- 地区の最低賃金 or 物価で係数を算出
- その係数を給与レンジに掛ける

### 注意
- PSAベース（基本給＋手当）
- ボーナス含まない
- 地区差はあくまで推定
"""))
