import streamlit as st
from textwrap import dedent

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Manila Salary Summary | 政府データ要約",
    page_icon="📊",
    layout="wide",
)


# -----------------------------
# i18n strings
# -----------------------------
TEXT = {
    "ja": {
        "page_title": "📊 マニラ給与レンジ要約（政府データベース）",
        "page_subtitle": "Philippine Statistics Authority（PSA）の公開データをもとにした、Entry / Supervisor / Manager の擬似サマリー画面です。",
        "lang_label": "表示言語",
        "summary_title": "最終まとめ（政府データ100%ベースの目安）",
        "level": "レベル",
        "salary_range": "月給（目安）",
        "entry_desc": "初級職・事務職・補助的業務を想定",
        "supervisor_desc": "中堅職・技術職・監督職相当を想定",
        "manager_desc": "管理職・上位専門職を想定",
        "card_note": "※ いずれも PSA の職種別平均賃金をもとに、役職概念へ読み替えた参考レンジです。",
        "assumption_title": "このページの前提",
        "assumption_body": dedent("""
        - これは **政府の公開データのみ** を使って整理した参考ページです。
        - PSA（Philippine Statistics Authority）の **2024 Occupational Wages Survey (OWS)** を主な根拠にしています。
        - PSA は **職種別の平均賃金** を公開していますが、**Entry / Supervisor / Manager のような役職別データは直接は公開していません**。
        - そのため、このページでは PSA の職種カテゴリをもとに、実務上わかりやすい 3 レベルへ再整理しています。
        - ここでの数値は **基本給＋定額手当** ベースの平均月額賃金であり、残業代・賞与・インセンティブ等は含みません。
        """),
        "flow_title": "算出までの流れ",
        "flow_steps": [
            "1. PSA の 2024 Occupational Wages Survey (OWS) から、平均月額賃金を確認",
            "2. ベンチマーク職種として、General office clerks と Elementary occupations の値を参照",
            "3. 上位カテゴリとして Professionals や Managers 相当の水準を参照",
            "4. 直接の『役職別』統計がないため、職種別データを実務向けに Entry / Supervisor / Manager へ再マッピング",
            "5. 一点の数字ではなく、読みやすいレンジ（目安）として表示",
        ],
        "mapping_title": "役職レベルへの読み替えイメージ",
        "mapping_cols": ["レベル", "主に参照した職種・考え方", "レンジの考え方"],
        "mapping_rows": [
            ["Entry", "Elementary occupations / General office clerks", "初級・補助的業務の平均値を中心に設定"],
            ["Supervisor", "Technicians / Associate professionals などの中位層", "Entry と Manager の中間層として設定"],
            ["Manager", "Managers / 上位 Professionals", "管理職・上位専門職の平均値を中心に設定"],
        ],
        "source_title": "根拠ソース",
        "source_intro": "以下はページ内の説明に対応する主要ソースです。",
        "source_label_1": "PSA: 2024 Occupational Wages Survey（ハイライト）",
        "source_label_2": "PSA: Occupational Wages Survey トップページ",
        "source_label_3": "PSA OpenSTAT: Occupational Wages Survey テーブル一覧",
        "source_label_4": "PSA OpenSTAT: 参照対象テーブル例（OWS）",
        "data_points_title": "ページ内で使っている代表値（補足）",
        "dp1": "全国平均月給：₱21,544（2024）",
        "dp2": "NCR 平均月給：₱29,310（2024）",
        "dp3": "General office clerks：全国 ₱19,721、NCR ₱22,903",
        "dp4": "Elementary occupations：全国 ₱13,506、NCR ₱15,991",
        "important_title": "注意点",
        "important_body": dedent("""
        - このページのレンジは、**政府公開データを役職別に見やすく再整理した推定レンジ**です。
        - PSA は平均値ベースのため、外資系・一部高給職・地域差によって実勢とズレる場合があります。
        - 採用提示額や個別オファーの判断には、求人市場データや社内等級制度と併用するのが実務的です。
        """),
        "footer": "Pseudo page for internal reference / このページは説明用の擬似画面です。",
    },
    "en": {
        "page_title": "📊 Manila Salary Range Summary (Government-Data Based)",
        "page_subtitle": "A simplified pseudo page based on publicly available data from the Philippine Statistics Authority (PSA), showing indicative ranges for Entry / Supervisor / Manager levels.",
        "lang_label": "Language",
        "summary_title": "Final Summary (100% based on government data)",
        "level": "Level",
        "salary_range": "Indicative Monthly Salary",
        "entry_desc": "Assumes junior, clerical, and support roles",
        "supervisor_desc": "Assumes mid-level, technical, and supervisory-equivalent roles",
        "manager_desc": "Assumes managerial and higher-level professional roles",
        "card_note": "*These are indicative ranges reconstructed from PSA occupation-based wage data, not official rank-based salary bands.*",
        "assumption_title": "Key assumptions behind this page",
        "assumption_body": dedent("""
        - This page uses **public government data only**.
        - The main source is the **2024 Occupational Wages Survey (OWS)** published by the Philippine Statistics Authority (PSA).
        - PSA publishes **occupation-based average wages**, but does **not directly publish salary data by rank such as Entry / Supervisor / Manager**.
        - Therefore, this page reorganizes PSA occupation categories into 3 practical business-friendly levels.
        - Figures shown here are based on **average monthly wage = basic pay + regular cash allowances**, excluding overtime pay, bonuses, and incentives.
        """),
        "flow_title": "How the ranges were derived",
        "flow_steps": [
            "1. Start with the PSA 2024 Occupational Wages Survey (OWS) average monthly wage figures",
            "2. Use benchmark occupations such as General office clerks and Elementary occupations",
            "3. Reference higher-level categories such as Professionals and Managers-equivalent roles",
            "4. Since PSA does not publish direct rank-based statistics, map occupation-based data into Entry / Supervisor / Manager levels",
            "5. Present the result as a practical salary range instead of a single figure",
        ],
        "mapping_title": "Illustrative mapping to business levels",
        "mapping_cols": ["Level", "Main occupation references", "How the range was framed"],
        "mapping_rows": [
            ["Entry", "Elementary occupations / General office clerks", "Centered around junior and support-role averages"],
            ["Supervisor", "Technicians / Associate professionals and similar mid-tier roles", "Positioned as the middle layer between Entry and Manager"],
            ["Manager", "Managers / higher Professionals", "Centered around managerial and higher-level professional averages"],
        ],
        "source_title": "Source links",
        "source_intro": "Main sources referenced in this page:",
        "source_label_1": "PSA: 2024 Occupational Wages Survey (Highlights)",
        "source_label_2": "PSA: Occupational Wages Survey main page",
        "source_label_3": "PSA OpenSTAT: Occupational Wages Survey tables",
        "source_label_4": "PSA OpenSTAT: Example OWS table referenced",
        "data_points_title": "Representative figures used on this page",
        "dp1": "National average monthly wage: ₱21,544 (2024)",
        "dp2": "NCR average monthly wage: ₱29,310 (2024)",
        "dp3": "General office clerks: National ₱19,721, NCR ₱22,903",
        "dp4": "Elementary occupations: National ₱13,506, NCR ₱15,991",
        "important_title": "Notes",
        "important_body": dedent("""
        - These ranges are **reconstructed business-friendly estimates** from official government data.
        - PSA data is average-based, so actual market salaries may differ depending on industry mix, foreign firms, seniority structure, and regional concentration.
        - For hiring decisions or offers, it is best to use this together with market salary benchmarks and your internal grading framework.
        """),
        "footer": "Pseudo page for internal reference.",
    },
}


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    lang = st.radio(TEXT["ja"]["lang_label"], options=["ja", "en"], format_func=lambda x: "日本語" if x == "ja" else "English")
    st.markdown("---")
    multiplier = st.number_input("Multiplier / 倍率", min_value=0.10, max_value=3.00, value=1.00, step=0.05)
    st.caption("Used only for scenario viewing / シミュレーション表示用")

T = TEXT[lang]


# -----------------------------
# Data
# -----------------------------
base_ranges = {
    "Entry": (16000, 23000),
    "Supervisor": (28000, 40000),
    "Manager": (50000, 70000),
}

descriptions = {
    "ja": {
        "Entry": T["entry_desc"],
        "Supervisor": T["supervisor_desc"],
        "Manager": T["manager_desc"],
    },
    "en": {
        "Entry": T["entry_desc"],
        "Supervisor": T["supervisor_desc"],
        "Manager": T["manager_desc"],
    },
}


def fmt_php(v: float) -> str:
    return f"₱{v:,.0f}"


def fmt_range(low: float, high: float) -> str:
    return f"{fmt_php(low)} – {fmt_php(high)}"


scaled_ranges = {
    k: (v[0] * multiplier, v[1] * multiplier)
    for k, v in base_ranges.items()
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
    .mini-note {
        font-size: 0.85rem;
        color: #666;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Header
# -----------------------------
st.markdown(f"<div class='hero-box'><h1>{T['page_title']}</h1><p>{T['page_subtitle']}</p></div>", unsafe_allow_html=True)


# -----------------------------
# Summary cards
# -----------------------------
st.subheader(T["summary_title"])
col1, col2, col3 = st.columns(3)
for col, level in zip([col1, col2, col3], ["Entry", "Supervisor", "Manager"]):
    low, high = scaled_ranges[level]
    with col:
        st.markdown(
            f"""
            <div class='salary-card'>
                <div class='salary-level'>{level}</div>
                <div class='salary-range'>{fmt_range(low, high)}</div>
                <div class='salary-desc'>{descriptions[lang][level]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.caption(T["card_note"])


# -----------------------------
# Context and methodology
# -----------------------------
left, right = st.columns([1.1, 0.9])

with left:
    st.subheader(T["assumption_title"])
    st.markdown(T["assumption_body"])

    st.subheader(T["flow_title"])
    for step in T["flow_steps"]:
        st.markdown(f"- {step}")

with right:
    st.subheader(T["mapping_title"])
    st.table({
        T["mapping_cols"][0]: [r[0] for r in T["mapping_rows"]],
        T["mapping_cols"][1]: [r[1] for r in T["mapping_rows"]],
        T["mapping_cols"][2]: [r[2] for r in T["mapping_rows"]],
    })


# -----------------------------
# Representative data points
# -----------------------------
st.subheader(T["data_points_title"])
col_a, col_b = st.columns(2)
with col_a:
    st.info(T["dp1"])
    st.info(T["dp2"])
with col_b:
    st.info(T["dp3"])
    st.info(T["dp4"])


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

    4. [{T['source_label_4']}](https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__1B__OWS/0031B3E1030.px/?rxid=d9f6019f-7d26-4fb9-9196-afc7f5ecce3e)
    """
)


# -----------------------------
# Notes
# -----------------------------
st.subheader(T["important_title"])
st.markdown(T["important_body"])

st.markdown("---")
st.caption(T["footer"])
