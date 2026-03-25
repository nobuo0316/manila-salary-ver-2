import streamlit as st
from textwrap import dedent

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Regional Salary Summary | 政府データ要約",
    page_icon="📊",
    layout="wide",
)


# -----------------------------
# Text / i18n
# -----------------------------
TEXT = {
    "ja": {
        "page_title": "📊 地域別給与レンジ要約（政府データベース）",
        "page_subtitle": "PSA / NWPC の公開データをもとに、Manila・Davao・Tawi-Tawi・General Santos の参考給与レンジを比較できる擬似ページです。",
        "lang_label": "表示言語",
        "region_label": "地区を選択",
        "coef_mode_label": "係数の決め方",
        "manual_mode": "手入力係数",
        "min_wage_mode": "最低賃金比率で自動算出",
        "blended_mode": "最低賃金 + 物価指数で算出",
        "manual_coef_label": "手入力係数",
        "manual_coef_help": "例：0.67 / 0.80 / 1.00 / 1.15",
        "price_index_label": "物価指数（Manila=1.00）",
        "price_index_help": "公的な地域CPIや独自の生活コスト指数を入力してください。例：0.82",
        "summary_title": "最終まとめ（政府データ100%ベースの目安）",
        "level": "レベル",
        "salary_range": "月給（目安）",
        "entry_desc": "初級職・事務職・補助的業務を想定",
        "middle manager_desc": "中堅職・技術職・監督職相当を想定",
        "manager_desc": "管理職・上位専門職を想定",
        "region_info_title": "選択地区の前提データ",
        "coef_result": "適用係数",
        "basis_title": "係数の算出ロジック",
        "basis_manual": "選択した地区に対して、手入力された係数をそのまま適用します。",
        "basis_min_wage": "地区の最低賃金 ÷ Manila(NCR) の最低賃金で係数を算出します。",
        "basis_blended": "(最低賃金比率 × 50%) + (物価指数 × 50%) で係数を算出します。",
        "assumption_title": "このページの前提",
        "assumption_body": dedent("""
        - これは **政府の公開データのみ** を中心に整理した参考ページです。
        - ベースレンジは PSA（Philippine Statistics Authority）の **2024 Occupational Wages Survey (OWS)** をもとにした Manila 想定レンジです。
        - 地区補正は NWPC（National Wages and Productivity Commission）の **地域別最低賃金** を使って調整できるようにしています。
        - Tawi-Tawi は単独地域統計ではなく、**BARMM の最低賃金を代理値**として使っています。
        - General Santos は **Region XII / SOCCSKSARGEN** の最低賃金を代理値として使っています。
        - 物価指数は公式の地域CPIや任意の生活コスト指数を入れられるようにしてあります。
        - 表示レンジは **基本給＋定額手当ベース** の参考値であり、残業代・賞与・インセンティブ等は含みません。
        """),
        "flow_title": "算出までの流れ",
        "flow_steps": [
            "1. Manila（NCR）の基準レンジをベース値として設定",
            "2. 地区を選択",
            "3. 手入力係数、または最低賃金比率 / 最低賃金＋物価指数から係数を算出",
            "4. 基準レンジに係数を掛けて、地区別の参考レンジを表示",
            "5. ソースURLと代理値の前提をページ下部に補足",
        ],
        "source_title": "根拠ソース",
        "source_intro": "以下はページ内の説明に対応する主要ソースです。",
        "source_label_1": "PSA: 2024 Occupational Wages Survey（ハイライト）",
        "source_label_2": "PSA: Occupational Wages Survey トップページ",
        "source_label_3": "PSA OpenSTAT: Occupational Wages Survey テーブル一覧",
        "source_label_4": "NWPC: NCR 最低賃金",
        "source_label_5": "NWPC: Davao Region 最低賃金",
        "source_label_6": "NWPC: BARMM 最低賃金（Tawi-Tawi の代理値）",
        "source_label_7": "NWPC: Region XII 最低賃金（General Santos の代理値）",
        "source_label_8": "PSA OpenSTAT: 参照対象テーブル例（OWS）",
        "notes_title": "注意点",
        "notes_body": dedent("""
        - Manila 以外のレンジは **地区係数による換算値** です。
        - Tawi-Tawi と General Santos は、このページでは **地域単位の公的賃金データを代理値として使用**しています。
        - 物価指数を併用する場合、係数はあくまで社内試算用の補正値です。
        - 厳密な採用提示額や等級設計には、求人市場データや自社制度も併用してください。
        """),
        "footer": "Pseudo page for internal reference / このページは説明用の擬似画面です。",
        "table_region": "地区",
        "table_proxy": "使用データ",
        "table_min_wage": "最低賃金（日額・非農業）",
        "table_notes": "補足",
        "proxy_notes_tawi": "Tawi-Tawi 単独ではなく BARMM の公的最低賃金を利用",
        "proxy_notes_gensan": "General Santos 単独ではなく Region XII の公的最低賃金を利用",
        "proxy_notes_manila": "NCR を Manila の基準値として利用",
        "proxy_notes_davao": "Davao Region を Davao の基準値として利用",
    },
    "en": {
        "page_title": "📊 Regional Salary Range Summary (Government-Data Based)",
        "page_subtitle": "A pseudo page using public PSA / NWPC data to compare indicative salary ranges for Manila, Davao, Tawi-Tawi, and General Santos.",
        "lang_label": "Language",
        "region_label": "Select region",
        "coef_mode_label": "Coefficient method",
        "manual_mode": "Manual coefficient",
        "min_wage_mode": "Auto by minimum wage ratio",
        "blended_mode": "Auto by minimum wage + price index",
        "manual_coef_label": "Manual coefficient",
        "manual_coef_help": "Example: 0.67 / 0.80 / 1.00 / 1.15",
        "price_index_label": "Price index (Manila=1.00)",
        "price_index_help": "Enter an official regional CPI proxy or your own cost-of-living index. Example: 0.82",
        "summary_title": "Final Summary (100% government-data-based baseline)",
        "level": "Level",
        "salary_range": "Indicative Monthly Salary",
        "entry_desc": "Assumes junior, clerical, and support roles",
        "middle manager_desc": "Assumes mid-level, technical, and middle managery-equivalent roles",
        "manager_desc": "Assumes managerial and higher-level professional roles",
        "region_info_title": "Selected location assumptions",
        "coef_result": "Applied coefficient",
        "basis_title": "Coefficient logic",
        "basis_manual": "Applies the manually entered coefficient directly to the Manila baseline ranges.",
        "basis_min_wage": "Coefficient is derived from: selected location minimum wage ÷ Manila (NCR) minimum wage.",
        "basis_blended": "Coefficient is derived from: (minimum wage ratio × 50%) + (price index × 50%).",
        "assumption_title": "Key assumptions behind this page",
        "assumption_body": dedent("""
        - This page is built primarily from **public government data only**.
        - The baseline salary bands are Manila-oriented ranges reconstructed from the PSA **2024 Occupational Wages Survey (OWS)**.
        - Regional adjustments can be made using NWPC **regional minimum wage** data.
        - Tawi-Tawi uses **BARMM minimum wage** as a proxy because a standalone public wage table is not directly provided here.
        - General Santos uses **Region XII / SOCCSKSARGEN minimum wage** as a proxy.
        - The price index field allows an official regional CPI proxy or an internally chosen cost-of-living index.
        - The displayed ranges are **basic pay + regular cash allowances** references and exclude overtime, bonuses, and incentives.
        """),
        "flow_title": "How the ranges are derived",
        "flow_steps": [
            "1. Use Manila (NCR) as the baseline salary range",
            "2. Select a location",
            "3. Choose manual coefficient or auto-calculate from minimum wage ratio / minimum wage + price index",
            "4. Apply the coefficient to the baseline salary ranges",
            "5. Show source URLs and proxy assumptions below",
        ],
        "source_title": "Source links",
        "source_intro": "Main sources referenced in this page:",
        "source_label_1": "PSA: 2024 Occupational Wages Survey (Highlights)",
        "source_label_2": "PSA: Occupational Wages Survey main page",
        "source_label_3": "PSA OpenSTAT: Occupational Wages Survey tables",
        "source_label_4": "NWPC: NCR minimum wage",
        "source_label_5": "NWPC: Davao Region minimum wage",
        "source_label_6": "NWPC: BARMM minimum wage (proxy for Tawi-Tawi)",
        "source_label_7": "NWPC: Region XII minimum wage (proxy for General Santos)",
        "source_label_8": "PSA OpenSTAT: Example OWS table referenced",
        "notes_title": "Notes",
        "notes_body": dedent("""
        - Salary ranges outside Manila are **coefficient-adjusted estimates**.
        - In this page, Tawi-Tawi and General Santos use **regional public wage proxies** rather than city-only official salary tables.
        - If a price index is added, the result should still be treated as an internal planning estimate.
        - For actual hiring offers or grading design, combine this with market salary benchmarks and your internal framework.
        """),
        "footer": "Pseudo page for internal reference.",
        "table_region": "Location",
        "table_proxy": "Data used",
        "table_min_wage": "Minimum wage (daily, non-agri)",
        "table_notes": "Notes",
        "proxy_notes_tawi": "Uses BARMM public minimum wage as proxy for Tawi-Tawi",
        "proxy_notes_gensan": "Uses Region XII public minimum wage as proxy for General Santos",
        "proxy_notes_manila": "Uses NCR as Manila baseline",
        "proxy_notes_davao": "Uses Davao Region as Davao baseline",
    },
}


# -----------------------------
# Baseline Manila salary ranges
# -----------------------------
BASE_RANGES = {
    "Entry": (16000, 23000),
    "middle manager": (28000, 40000),
    "Manager": (50000, 70000),
}

# Minimum wage defaults (current values as of Mar 26, 2026 where applicable)
# Non-agriculture daily minimum wage.
REGIONS = {
    "Manila": {
        "display_ja": "Manila (NCR)",
        "display_en": "Manila (NCR)",
        "min_wage": 695.0,
        "source_type": "NCR",
        "price_index_default": 1.00,
        "source_url": "https://nwpc.dole.gov.ph/ncr/",
        "note_ja": "NCR を Manila の基準値として利用",
        "note_en": "Uses NCR as Manila baseline",
    },
    "Davao": {
        "display_ja": "Davao",
        "display_en": "Davao",
        "min_wage": 525.0,
        "source_type": "Region XI",
        "price_index_default": 0.82,
        "source_url": "https://nwpc.dole.gov.ph/region-xi/",
        "note_ja": "Davao Region を Davao の基準値として利用",
        "note_en": "Uses Davao Region as Davao baseline",
    },
    "Tawi-Tawi": {
        "display_ja": "Tawi-Tawi",
        "display_en": "Tawi-Tawi",
        "min_wage": 386.0,
        "source_type": "BARMM",
        "price_index_default": 0.70,
        "source_url": "https://nwpc.dole.gov.ph/barmm/",
        "note_ja": "Tawi-Tawi 単独ではなく BARMM の公的最低賃金を利用",
        "note_en": "Uses BARMM public minimum wage as proxy for Tawi-Tawi",
    },
    "General Santos": {
        "display_ja": "General Santos",
        "display_en": "General Santos",
        "min_wage": 460.0,
        "source_type": "Region XII / SOCCSKSARGEN",
        "price_index_default": 0.78,
        "source_url": "https://nwpc.dole.gov.ph/region-xii/",
        "note_ja": "General Santos 単独ではなく Region XII の公的最低賃金を利用",
        "note_en": "Uses Region XII public minimum wage as proxy for General Santos",
    },
}


def fmt_php(v: float) -> str:
    return f"₱{v:,.0f}"


def fmt_range(low: float, high: float) -> str:
    return f"{fmt_php(low)} – {fmt_php(high)}"


# -----------------------------
# Sidebar / controls
# -----------------------------
with st.sidebar:
    lang = st.radio(
        TEXT["ja"]["lang_label"],
        options=["ja", "en"],
        format_func=lambda x: "日本語" if x == "ja" else "English",
    )
    T = TEXT[lang]

    region_keys = list(REGIONS.keys())
    region = st.selectbox(
        T["region_label"],
        options=region_keys,
        format_func=lambda x: REGIONS[x]["display_ja"] if lang == "ja" else REGIONS[x]["display_en"],
    )

    coef_mode_map = {
        T["manual_mode"]: "manual",
        T["min_wage_mode"]: "min_wage",
        T["blended_mode"]: "blended",
    }
    coef_mode_label = st.radio(T["coef_mode_label"], options=list(coef_mode_map.keys()))
    coef_mode = coef_mode_map[coef_mode_label]

    manual_coef = st.number_input(
        T["manual_coef_label"],
        min_value=0.10,
        max_value=3.00,
        value=1.00,
        step=0.05,
        help=T["manual_coef_help"],
    )

    price_index = st.number_input(
        T["price_index_label"],
        min_value=0.10,
        max_value=3.00,
        value=float(REGIONS[region]["price_index_default"]),
        step=0.01,
        help=T["price_index_help"],
    )


# -----------------------------
# Coefficient logic
# -----------------------------
manila_min_wage = REGIONS["Manila"]["min_wage"]
selected_min_wage = REGIONS[region]["min_wage"]
min_wage_ratio = selected_min_wage / manila_min_wage if manila_min_wage else 1.0

if coef_mode == "manual":
    applied_coef = manual_coef
    basis_text = T["basis_manual"]
elif coef_mode == "min_wage":
    applied_coef = min_wage_ratio
    basis_text = T["basis_min_wage"]
else:
    applied_coef = (min_wage_ratio * 0.5) + (price_index * 0.5)
    basis_text = T["basis_blended"]

scaled_ranges = {
    k: (v[0] * applied_coef, v[1] * applied_coef)
    for k, v in BASE_RANGES.items()
}


# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .hero-box {
        padding: 1.2rem 1.4rem;
        border: 1px solid rgba(120,120,120,.2);
        border-radius: 18px;
        background: linear-gradient(180deg, rgba(240,242,246,0.55), rgba(255,255,255,0.9));
        margin-bottom: 1rem;
    }
    .salary-card {
        border: 1px solid rgba(120,120,120,.18);
        border-radius: 18px;
        padding: 1rem 1rem 0.8rem 1rem;
        background: white;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        min-height: 180px;
    }
    .salary-level {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }
    .salary-range {
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .salary-desc {
        font-size: 0.95rem;
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    f"<div class='hero-box'><h1>{T['page_title']}</h1><p>{T['page_subtitle']}</p></div>",
    unsafe_allow_html=True,
)


# -----------------------------
# Top info
# -----------------------------
info_col1, info_col2, info_col3 = st.columns(3)
with info_col1:
    st.metric(T["coef_result"], f"{applied_coef:.2f}x")
with info_col2:
    st.metric(T["table_min_wage"], fmt_php(selected_min_wage))
with info_col3:
    st.metric("Min wage ratio vs Manila", f"{min_wage_ratio:.2f}x")

st.caption(basis_text)


# -----------------------------
# Summary cards
# -----------------------------
st.subheader(T["summary_title"])
entry_desc = T["entry_desc"]
middle manager_desc = T["middle manager_desc"]
manager_desc = T["manager_desc"]
card_desc = {
    "Entry": entry_desc,
    "middle manager": middle manager_desc,
    "Manager": manager_desc,
}

col1, col2, col3 = st.columns(3)
for col, level in zip([col1, col2, col3], ["Entry", "middle manager", "Manager"]):
    low, high = scaled_ranges[level]
    with col:
        st.markdown(
            f"""
            <div class='salary-card'>
                <div class='salary-level'>{level}</div>
                <div class='salary-range'>{fmt_range(low, high)}</div>
                <div class='salary-desc'>{card_desc[level]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------
# Region info
# -----------------------------
st.subheader(T["region_info_title"])
region_df = {
    T["table_region"]: [REGIONS[k]["display_ja"] if lang == "ja" else REGIONS[k]["display_en"] for k in REGIONS],
    T["table_proxy"]: [REGIONS[k]["source_type"] for k in REGIONS],
    T["table_min_wage"]: [fmt_php(REGIONS[k]["min_wage"]) for k in REGIONS],
    T["table_notes"]: [REGIONS[k]["note_ja"] if lang == "ja" else REGIONS[k]["note_en"] for k in REGIONS],
}
st.table(region_df)


# -----------------------------
# Methodology and assumptions
# -----------------------------
left, right = st.columns([1.1, 0.9])
with left:
    st.subheader(T["assumption_title"])
    st.markdown(T["assumption_body"])
with right:
    st.subheader(T["flow_title"])
    for step in T["flow_steps"]:
        st.markdown(f"- {step}")


# -----------------------------
# Sources
# -----------------------------
st.subheader(T["source_title"])
st.markdown(T["source_intro"])

st.markdown(
    f"""
1. [{T['source_label_1']}](https://psa.gov.ph/content/highlights-2024-occupational-wages-survey-ows)

2. [{T['source_label_2']}](https://psa.gov.ph/statistics/occupational-wages-survey)

3. [{T['source_label_3']}](https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__1B__OWS/?tablelist=true)

4. [{T['source_label_4']}](https://nwpc.dole.gov.ph/ncr/)

5. [{T['source_label_5']}](https://nwpc.dole.gov.ph/region-xi/)

6. [{T['source_label_6']}](https://nwpc.dole.gov.ph/barmm/)

7. [{T['source_label_7']}](https://nwpc.dole.gov.ph/region-xii/)

8. [{T['source_label_8']}](https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__1B__OWS/0031B3E1030.px/?rxid=d9f6019f-7d26-4fb9-9196-afc7f5ecce3e)
"""
)


# -----------------------------
# Notes
# -----------------------------
st.subheader(T["notes_title"])
st.markdown(T["notes_body"])

st.markdown("---")
st.caption(T["footer"])
