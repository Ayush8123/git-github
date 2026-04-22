import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
import time
from datetime import datetime, timedelta

# ── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Talent Intelligence Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;600;700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}
.main { background-color: #060d1a; }
.stApp { background: linear-gradient(135deg, #060d1a 0%, #0b1628 50%, #071020 100%); }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1e35 0%, #081525 100%) !important;
    border-right: 1px solid rgba(0,200,255,0.12);
}
[data-testid="stSidebar"] * { color: #c8e6ff !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stFileUploader label { color: #6ec6ff !important; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; }

/* ── KPI Cards ── */
.kpi-card {
    background: linear-gradient(135deg, rgba(0,180,255,0.08) 0%, rgba(0,80,180,0.12) 100%);
    border: 1px solid rgba(0,200,255,0.2);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.2s, border-color 0.2s;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: -40%;
    left: -40%;
    width: 80%;
    height: 80%;
    background: radial-gradient(circle, rgba(0,200,255,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.kpi-card:hover { transform: translateY(-3px); border-color: rgba(0,200,255,0.45); }
.kpi-value { font-family: 'Space Mono', monospace; font-size: 2.4rem; font-weight: 700; color: #00d4ff; line-height: 1; margin-bottom: 6px; }
.kpi-label { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em; color: #7aabcc; }
.kpi-delta { font-size: 0.75rem; color: #4ade80; margin-top: 6px; }

/* ── Section Headers ── */
.section-header {
    font-family: 'Outfit', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #00d4ff;
    border-left: 3px solid #00d4ff;
    padding-left: 12px;
    margin: 28px 0 16px 0;
}

/* ── Match Score Ring Container ── */
.match-score-container {
    background: linear-gradient(135deg, rgba(0,180,255,0.06), rgba(0,50,120,0.15));
    border: 1px solid rgba(0,200,255,0.2);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
}

/* ── Chat bubbles ── */
.chat-user {
    background: linear-gradient(135deg, rgba(0,150,255,0.2), rgba(0,80,180,0.3));
    border: 1px solid rgba(0,180,255,0.3);
    border-radius: 16px 16px 4px 16px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #cce8ff;
    font-size: 0.92rem;
}
.chat-ai {
    background: linear-gradient(135deg, rgba(0,30,70,0.8), rgba(0,20,50,0.9));
    border: 1px solid rgba(0,200,255,0.15);
    border-radius: 16px 16px 16px 4px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #b0d8f0;
    font-size: 0.92rem;
}
.chat-label-user { font-size: 0.7rem; color: #6ec6ff; text-align: right; margin-bottom: 2px; text-transform: uppercase; letter-spacing: 0.06em; }
.chat-label-ai { font-size: 0.7rem; color: #00d4ff; margin-bottom: 2px; text-transform: uppercase; letter-spacing: 0.06em; }

/* ── Skill Pills ── */
.skill-pill-match {
    display: inline-block;
    background: rgba(74,222,128,0.15);
    border: 1px solid rgba(74,222,128,0.4);
    color: #4ade80;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    margin: 3px 2px;
    font-family: 'Space Mono', monospace;
}
.skill-pill-missing {
    display: inline-block;
    background: rgba(248,113,113,0.12);
    border: 1px solid rgba(248,113,113,0.35);
    color: #f87171;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    margin: 3px 2px;
    font-family: 'Space Mono', monospace;
}

/* ── Status Badges ── */
.badge-shortlisted { background: rgba(74,222,128,0.15); border: 1px solid rgba(74,222,128,0.4); color: #4ade80; border-radius: 6px; padding: 2px 10px; font-size: 0.75rem; }
.badge-interview { background: rgba(0,180,255,0.15); border: 1px solid rgba(0,180,255,0.4); color: #00d4ff; border-radius: 6px; padding: 2px 10px; font-size: 0.75rem; }
.badge-review { background: rgba(251,191,36,0.12); border: 1px solid rgba(251,191,36,0.35); color: #fbbf24; border-radius: 6px; padding: 2px 10px; font-size: 0.75rem; }
.badge-rejected { background: rgba(248,113,113,0.12); border: 1px solid rgba(248,113,113,0.3); color: #f87171; border-radius: 6px; padding: 2px 10px; font-size: 0.75rem; }

/* ── Dataframe override ── */
.dataframe { font-family: 'Outfit', sans-serif !important; }
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* ── General text ── */
h1 { font-family: 'Outfit', sans-serif !important; font-weight: 800 !important; color: #e8f4ff !important; }
h2, h3 { font-family: 'Outfit', sans-serif !important; color: #c8e6ff !important; }
p, li { color: #9abbd4 !important; }
label { color: #7aabcc !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: rgba(0,30,70,0.5); border-radius: 10px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] { color: #7aabcc; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.07em; }
.stTabs [aria-selected="true"] { background: rgba(0,200,255,0.15) !important; color: #00d4ff !important; border-radius: 8px; }

/* ── Upload ── */
[data-testid="stFileUploader"] { background: rgba(0,30,70,0.4); border: 1px dashed rgba(0,200,255,0.25); border-radius: 12px; padding: 8px; }
[data-testid="stFileUploader"] * { color: #7aabcc !important; }

/* ── Text area / Input ── */
.stTextArea textarea { background: rgba(0,20,50,0.7) !important; border: 1px solid rgba(0,180,255,0.2) !important; color: #c8e6ff !important; border-radius: 10px !important; font-family: 'Outfit', sans-serif !important; }
.stTextInput input { background: rgba(0,20,50,0.7) !important; border: 1px solid rgba(0,180,255,0.2) !important; color: #c8e6ff !important; border-radius: 10px !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,180,255,0.2), rgba(0,80,200,0.3)) !important;
    border: 1px solid rgba(0,200,255,0.4) !important;
    color: #00d4ff !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,200,255,0.3), rgba(0,100,220,0.4)) !important;
    transform: translateY(-1px) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div { background: rgba(0,20,50,0.7) !important; border: 1px solid rgba(0,180,255,0.2) !important; color: #c8e6ff !important; border-radius: 10px !important; }

/* ── Progress bars ── */
.stProgress > div > div > div { background: linear-gradient(90deg, #00d4ff, #0080ff) !important; border-radius: 4px !important; }

/* ── Metric ── */
[data-testid="metric-container"] { background: rgba(0,30,70,0.3); border-radius: 12px; padding: 12px; border: 1px solid rgba(0,180,255,0.12); }

/* ── Divider ── */
hr { border-color: rgba(0,180,255,0.12) !important; }
</style>
""", unsafe_allow_html=True)

# ── Fake Data ────────────────────────────────────────────────────────────────
CANDIDATES = [
    {"name": "Arjun Mehta",     "role": "Data Engineer",        "match": 94, "exp": "6 yrs", "skills": "Spark, Kafka, Python, Airflow", "status": "Interview"},
    {"name": "Priya Sharma",    "role": "ML Engineer",          "match": 89, "exp": "4 yrs", "skills": "TensorFlow, Python, Docker, GCP", "status": "Shortlisted"},
    {"name": "Chen Wei",        "role": "Data Engineer",        "match": 85, "exp": "5 yrs", "skills": "Spark, Python, Hadoop, SQL",    "status": "Shortlisted"},
    {"name": "Sofia Reyes",     "role": "Data Scientist",       "match": 81, "exp": "3 yrs", "skills": "Python, Scikit-learn, R, SQL",  "status": "Review"},
    {"name": "Rahul Nair",      "role": "MLOps Engineer",       "match": 78, "exp": "4 yrs", "skills": "Kubernetes, Docker, MLflow",   "status": "Review"},
    {"name": "Emily Johnson",   "role": "Data Analyst",         "match": 73, "exp": "2 yrs", "skills": "SQL, Tableau, Python, Excel",  "status": "Review"},
    {"name": "Marcus Williams", "role": "Data Engineer",        "match": 68, "exp": "3 yrs", "skills": "Python, SQL, dbt, Redshift",   "status": "Review"},
    {"name": "Aisha Patel",     "role": "ML Engineer",          "match": 61, "exp": "2 yrs", "skills": "Python, PyTorch, NLP",         "status": "Rejected"},
    {"name": "James O'Brien",   "role": "Data Scientist",       "match": 57, "exp": "1 yr",  "skills": "R, Python, Statistics",        "status": "Rejected"},
    {"name": "Yuna Kim",        "role": "Analytics Engineer",   "match": 52, "exp": "2 yrs", "skills": "SQL, dbt, Looker, Python",     "status": "Rejected"},
]

PARSED_RESUME = {
    "name": "Alex Rivera",
    "email": "alex.rivera@email.com",
    "skills": ["Python", "Apache Spark", "SQL", "Machine Learning", "AWS", "TensorFlow", "Pandas", "Git"],
    "experience": [
        {"title": "Senior Data Engineer", "company": "TechCorp Inc.", "duration": "2021 – Present", "desc": "Built data pipelines processing 10TB/day using Spark and Kafka."},
        {"title": "Data Engineer", "company": "StartupXYZ", "duration": "2019 – 2021", "desc": "Designed ETL workflows on AWS Glue and Redshift."},
    ],
    "education": [{"degree": "B.Tech Computer Science", "school": "IIT Bombay", "year": "2019"}],
    "projects": [
        {"name": "Real-time Fraud Detection", "tech": "Kafka, Spark Streaming, Python", "impact": "Reduced fraud by 34%"},
        {"name": "ML Feature Store", "tech": "AWS SageMaker, Python, Redis", "impact": "Cut model training time by 60%"},
    ],
}

JD_SKILLS = ["Python", "Apache Spark", "Kafka", "Airflow", "Docker", "Kubernetes", "SQL", "dbt", "Redshift", "AWS"]

SKILL_GAPS = {"Kafka": 7, "Airflow": 6, "Docker": 5, "Kubernetes": 4, "dbt": 3, "Redshift": 3, "Terraform": 2, "Go": 2}

PIPELINE = {"Total Resumes": 248, "Parsed": 231, "Matched (>60%)": 189, "Shortlisted": 47, "Interview": 18}

AI_RESPONSES = {
    "top candidates for data engineer": "📊 **Top Data Engineer Candidates:**\n\n1. **Arjun Mehta** — 94% match | 6 yrs | Spark, Kafka, Airflow ✅\n2. **Chen Wei** — 85% match | 5 yrs | Spark, Hadoop, SQL ✅\n3. **Marcus Williams** — 68% match | 3 yrs | Python, dbt, Redshift ⚠️\n\nArjun Mehta is the strongest fit — he meets 9/10 JD requirements and has direct Kafka and Airflow experience.",
    "average match score": "📈 **Average Match Score:** 73.8%\n\nBreakdown by role:\n• Data Engineer: 82.3%\n• ML Engineer: 75.0%\n• Data Scientist: 69.0%\n• Others: 62.5%",
    "shortlisted candidates": "✅ **Shortlisted Candidates (3):**\n\n• **Arjun Mehta** — Data Engineer — 94%\n• **Priya Sharma** — ML Engineer — 89%\n• **Chen Wei** — Data Engineer — 85%\n\nAll three exceed the 80% threshold and are cleared for technical screening.",
    "skill gaps": "🔍 **Top Skill Gaps in Candidate Pool:**\n\n1. Kafka — missing in 7 candidates\n2. Airflow — missing in 6 candidates\n3. Docker — missing in 5 candidates\n4. Kubernetes — missing in 4 candidates\n\n💡 Recommendation: Consider upskilling current pipeline or expanding JD criteria for Docker/K8s.",
    "default": "🤖 I can help you with:\n• **Top candidates** for any role\n• **Match score** statistics\n• **Shortlisted** candidates summary\n• **Skill gaps** in the talent pool\n• Candidate **comparison** analysis\n\nTry: *'Show top candidates for ML Engineer'*",
}

def get_ai_response(query: str) -> str:
    q = query.lower()
    for key in AI_RESPONSES:
        if key in q:
            return AI_RESPONSES[key]
    if "ml engineer" in q or "machine learning" in q:
        return "🤖 **Top ML Engineer Candidates:**\n\n1. **Priya Sharma** — 89% match | 4 yrs | TensorFlow, Docker, GCP ✅\n2. **Aisha Patel** — 61% match | 2 yrs | PyTorch, NLP ⚠️\n\nPriya Sharma is the clear frontrunner — strong MLOps knowledge and production deployment experience."
    if "reject" in q:
        return "❌ **Rejected Candidates (3):** Aisha Patel (61%), James O'Brien (57%), Yuna Kim (52%).\n\nAll fell below the 65% threshold. Consider keeping Aisha Patel in talent pool for junior openings."
    return AI_RESPONSES["default"]

def make_gauge(value, title, color="#00d4ff"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"color": "#7aabcc", "size": 13, "family": "Outfit"}},
        number={"suffix": "%", "font": {"color": color, "size": 32, "family": "Space Mono"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#1e3a5f", "tickfont": {"color": "#4a6f8f", "size": 10}},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "rgba(0,20,50,0.3)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40],  "color": "rgba(248,113,113,0.08)"},
                {"range": [40, 70], "color": "rgba(251,191,36,0.08)"},
                {"range": [70, 100],"color": "rgba(74,222,128,0.08)"},
            ],
            "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.8, "value": value},
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=10, l=20, r=20),
        height=200,
        font={"family": "Outfit"},
    )
    return fig

def make_skill_gap_chart():
    skills = list(SKILL_GAPS.keys())
    counts = list(SKILL_GAPS.values())
    colors = ["#00d4ff" if c >= 5 else "#fbbf24" if c >= 3 else "#4ade80" for c in counts]
    fig = go.Figure(go.Bar(
        x=skills, y=counts,
        marker=dict(
            color=colors,
            opacity=0.85,
            line=dict(color="rgba(0,200,255,0.3)", width=1),
        ),
        text=counts,
        textposition="outside",
        textfont=dict(color="#7aabcc", size=11, family="Space Mono"),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,10,30,0.4)",
        xaxis=dict(tickfont=dict(color="#7aabcc", family="Outfit"), gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,180,255,0.1)"),
        yaxis=dict(tickfont=dict(color="#4a6f8f", family="Space Mono"), gridcolor="rgba(0,180,255,0.07)", linecolor="rgba(0,0,0,0)"),
        margin=dict(t=20, b=10, l=30, r=20),
        height=280,
    )
    return fig

def make_funnel():
    stages = list(PIPELINE.keys())
    values = list(PIPELINE.values())
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent initial",
        textfont=dict(color="#e8f4ff", family="Outfit", size=12),
        marker=dict(
            color=["rgba(0,180,255,0.7)", "rgba(0,160,230,0.65)", "rgba(0,140,200,0.6)", "rgba(74,222,128,0.6)", "rgba(0,220,180,0.7)"],
            line=dict(color=["rgba(0,200,255,0.4)"]*5, width=1),
        ),
        connector=dict(line=dict(color="rgba(0,180,255,0.15)", width=1)),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#7aabcc", family="Outfit"),
        margin=dict(t=10, b=10, l=20, r=20),
        height=300,
    )
    return fig

def make_match_distribution():
    scores = [c["match"] for c in CANDIDATES]
    names  = [c["name"].split()[0] for c in CANDIDATES]
    colors = ["#4ade80" if s >= 80 else "#fbbf24" if s >= 65 else "#f87171" for s in scores]
    fig = go.Figure(go.Bar(
        x=names, y=scores,
        marker=dict(color=colors, opacity=0.8, line=dict(color="rgba(255,255,255,0.05)", width=0.5)),
        text=[f"{s}%" for s in scores],
        textposition="outside",
        textfont=dict(color="#7aabcc", size=10, family="Space Mono"),
    ))
    fig.add_hline(y=80, line_dash="dot", line_color="rgba(74,222,128,0.5)", annotation_text="Shortlist Threshold",
                  annotation_font=dict(color="#4ade80", size=10))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,10,30,0.4)",
        xaxis=dict(tickfont=dict(color="#7aabcc", family="Outfit"), gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(range=[0,110], tickfont=dict(color="#4a6f8f", family="Space Mono"), gridcolor="rgba(0,180,255,0.07)"),
        margin=dict(t=30, b=10, l=30, r=10),
        height=280,
    )
    return fig

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧠 AI Talent Intelligence")
    st.markdown("---")
    st.markdown("**Navigation**")
    page = st.radio("", ["📊 Overview", "📄 Resume Analyzer", "🏆 Leaderboard", "📈 Analytics", "💬 AI Recruiter"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Active Filters**")
    role_filter = st.selectbox("Role", ["All Roles", "Data Engineer", "ML Engineer", "Data Scientist", "MLOps Engineer"])
    score_filter = st.slider("Min Match Score", 0, 100, 50)
    st.markdown("---")
    st.markdown("**Cycle**")
    st.markdown('<span style="color:#4ade80;font-size:0.8rem">● Q1 2025 Hiring Active</span>', unsafe_allow_html=True)
    st.markdown('<span style="color:#fbbf24;font-size:0.75rem">Updated: Mar 16, 2025 · 09:42 AM</span>', unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("# 🧠 AI Talent Intelligence Dashboard")
    st.markdown('<p style="color:#4a7a9b;font-size:0.9rem;margin-top:-10px">Recruitment Intelligence Platform · Powered by</p>', unsafe_allow_html=True)
with col_h2:
    st.markdown('<div style="text-align:right;padding-top:20px"><span style="background:rgba(74,222,128,0.15);border:1px solid rgba(74,222,128,0.4);color:#4ade80;border-radius:20px;padding:4px 14px;font-size:0.8rem">● System Online</span></div>', unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if "📊 Overview" in page:

    # KPI Cards
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        ("248", "Total Candidates", "↑ 12% this week"),
        ("73.8%", "Avg Match Score", "↑ 4.2pts from last cycle"),
        ("47", "Shortlisted", "19% shortlist rate"),
        ("8", "Open Roles", "3 critical priority"),
    ]
    for col, (val, lbl, delta) in zip([k1,k2,k3,k4], kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{lbl}</div>
                <div class="kpi-delta">{delta}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts row
    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.markdown('<div class="section-header">Candidate Match Distribution</div>', unsafe_allow_html=True)
        st.plotly_chart(make_match_distribution(), use_container_width=True, config={"displayModeBar": False})
    with col_r:
        st.markdown('<div class="section-header">Hiring Pipeline Funnel</div>', unsafe_allow_html=True)
        st.plotly_chart(make_funnel(), use_container_width=True, config={"displayModeBar": False})

    # Skill gap
    st.markdown('<div class="section-header">Skill Gap Analysis · Candidate Pool</div>', unsafe_allow_html=True)
    st.plotly_chart(make_skill_gap_chart(), use_container_width=True, config={"displayModeBar": False})


# ════════════════════════════════════════════════════════════════════════════
# PAGE: RESUME ANALYZER
# ════════════════════════════════════════════════════════════════════════════
elif "📄 Resume Analyzer" in page:

    col_upload, col_jd = st.columns(2)
    with col_upload:
        st.markdown('<div class="section-header">Resume Upload</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload PDF Resume", type=["pdf"], key="resume_upload")

        if uploaded:
            with st.spinner("🔍 Parsing resume with AI..."):
                time.sleep(1.2)
            st.success("✅ Resume parsed successfully!")
            st.markdown("**Extracted Profile**")
            st.markdown(f"👤 **{PARSED_RESUME['name']}** · {PARSED_RESUME['email']}")

            st.markdown("**🛠 Skills Detected**")
            pills = " ".join([f'<span class="skill-pill-match">{s}</span>' for s in PARSED_RESUME["skills"]])
            st.markdown(pills, unsafe_allow_html=True)

            st.markdown("**💼 Experience**")
            for exp in PARSED_RESUME["experience"]:
                st.markdown(f"• **{exp['title']}** @ {exp['company']} _{exp['duration']}_")
                st.markdown(f"  <small style='color:#4a6f8f'>{exp['desc']}</small>", unsafe_allow_html=True)

            st.markdown("**🎓 Education**")
            for ed in PARSED_RESUME["education"]:
                st.markdown(f"• {ed['degree']} · {ed['school']} · {ed['year']}")

            st.markdown("**🚀 Projects**")
            for p in PARSED_RESUME["projects"]:
                st.markdown(f"• **{p['name']}** — _{p['tech']}_")
                st.markdown(f"  <small style='color:#4ade80'>Impact: {p['impact']}</small>", unsafe_allow_html=True)

    with col_jd:
        st.markdown('<div class="section-header">Job Description</div>', unsafe_allow_html=True)
        jd_text = st.text_area(
            "Paste Job Description",
            value="We are hiring a Senior Data Engineer...\n\nRequired Skills:\n- Python, Apache Spark\n- Kafka, Airflow\n- Docker, Kubernetes\n- SQL, dbt, Redshift\n- AWS / GCP cloud experience",
            height=200,
            key="jd_input"
        )
        if jd_text:
            with st.spinner("🔎 Extracting JD requirements..."):
                time.sleep(0.6)
            st.markdown("**Required Skills Identified**")
            jd_pills = " ".join([f'<span class="skill-pill-match">{s}</span>' for s in JD_SKILLS])
            st.markdown(jd_pills, unsafe_allow_html=True)

    # Match Engine
    if uploaded and jd_text:
        st.markdown("---")
        st.markdown('<div class="section-header">Candidate Match Engine</div>', unsafe_allow_html=True)

        g1, g2, g3, g4 = st.columns(4)
        with g1:
            st.plotly_chart(make_gauge(87, "Overall Match"), use_container_width=True, config={"displayModeBar": False})
        with g2:
            st.plotly_chart(make_gauge(80, "Skill Match", "#4ade80"), use_container_width=True, config={"displayModeBar": False})
        with g3:
            st.plotly_chart(make_gauge(92, "Experience Fit", "#fbbf24"), use_container_width=True, config={"displayModeBar": False})
        with g4:
            st.plotly_chart(make_gauge(85, "Domain Fit", "#a78bfa"), use_container_width=True, config={"displayModeBar": False})

        # Explainability Panel
        st.markdown('<div class="section-header">Explainability Panel</div>', unsafe_allow_html=True)
        ep_l, ep_r = st.columns(2)
        with ep_l:
            matched = ["Python", "Apache Spark", "SQL", "AWS", "Machine Learning"]
            missing = ["Kafka", "Airflow", "Docker", "Kubernetes", "dbt"]
            st.markdown("**✅ Matched Skills**")
            st.markdown(" ".join([f'<span class="skill-pill-match">{s}</span>' for s in matched]), unsafe_allow_html=True)
            st.markdown("<br>**❌ Missing Skills**", unsafe_allow_html=True)
            st.markdown(" ".join([f'<span class="skill-pill-missing">{s}</span>' for s in missing]), unsafe_allow_html=True)
        with ep_r:
            st.markdown("**📋 Evidence from Resume**")
            evidence = [
                ("Python", "5+ years of Python development across multiple ML projects"),
                ("Apache Spark", "Built pipelines processing 10TB/day using Spark on AWS EMR"),
                ("SQL", "Designed Redshift schemas and wrote complex analytical queries"),
                ("AWS", "Deployed infrastructure on AWS using Glue, EMR, S3, Lambda"),
            ]
            for skill, ev in evidence:
                st.markdown(f'<div style="background:rgba(0,30,70,0.4);border:1px solid rgba(0,180,255,0.1);border-radius:8px;padding:8px 12px;margin:5px 0"><span style="color:#00d4ff;font-size:0.78rem;font-family:Space Mono">{skill}</span><br><span style="color:#7aabcc;font-size:0.82rem">{ev}</span></div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: LEADERBOARD
# ════════════════════════════════════════════════════════════════════════════
elif "🏆 Leaderboard" in page:
    st.markdown('<div class="section-header">Candidate Leaderboard</div>', unsafe_allow_html=True)

    filtered = [c for c in CANDIDATES if c["match"] >= score_filter]
    if role_filter != "All Roles":
        filtered = [c for c in filtered if c["role"] == role_filter]

    def status_badge(s):
        cls_map = {"Shortlisted": "badge-shortlisted", "Interview": "badge-interview",
                   "Review": "badge-review", "Rejected": "badge-rejected"}
        css_cls = cls_map.get(s, "badge-review")
        return f'<span class="{css_cls}">{s}</span>'

    def score_bar(v):
        color = "#4ade80" if v>=80 else "#fbbf24" if v>=65 else "#f87171"
        return f'<div style="background:rgba(0,20,50,0.5);border-radius:4px;overflow:hidden;height:8px;width:100%;margin-top:4px"><div style="width:{v}%;height:8px;background:{color};border-radius:4px"></div></div><span style="font-family:Space Mono;font-size:0.75rem;color:{color}">{v}%</span>'

    header_cols = st.columns([0.4, 2, 2, 2, 1, 2.5, 1.5])
    headers = ["#", "Name", "Role", "Skills", "Exp", "Match Score", "Status"]
    for col, h in zip(header_cols, headers):
        col.markdown(f'<div style="color:#4a7a9b;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;padding-bottom:8px;border-bottom:1px solid rgba(0,180,255,0.15)">{h}</div>', unsafe_allow_html=True)

    for i, c in enumerate(filtered, 1):
        row = st.columns([0.4, 2, 2, 2, 1, 2.5, 1.5])
        rank_icon = "🥇" if i==1 else "🥈" if i==2 else "🥉" if i==3 else f"#{i}"
        row[0].markdown(f'<div style="padding:10px 0;color:#4a6f8f;font-family:Space Mono;font-size:0.8rem">{rank_icon}</div>', unsafe_allow_html=True)
        row[1].markdown(f'<div style="padding:10px 0;color:#c8e6ff;font-weight:600">{c["name"]}</div>', unsafe_allow_html=True)
        row[2].markdown(f'<div style="padding:10px 0;color:#7aabcc;font-size:0.88rem">{c["role"]}</div>', unsafe_allow_html=True)
        row[3].markdown(f'<div style="padding:10px 0;color:#7aabcc;font-size:0.8rem">{c["skills"]}</div>', unsafe_allow_html=True)
        row[4].markdown(f'<div style="padding:10px 0;color:#7aabcc;font-size:0.85rem;font-family:Space Mono">{c["exp"]}</div>', unsafe_allow_html=True)
        row[5].markdown(f'<div style="padding:10px 0">{score_bar(c["match"])}</div>', unsafe_allow_html=True)
        row[6].markdown(f'<div style="padding:10px 0">{status_badge(c["status"])}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"Showing **{len(filtered)}** of {len(CANDIDATES)} candidates · Filter: {role_filter} · Min Score: {score_filter}%")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ════════════════════════════════════════════════════════════════════════════
elif "📈 Analytics" in page:
    st.markdown('<div class="section-header">Skill Gap Visualization</div>', unsafe_allow_html=True)
    st.plotly_chart(make_skill_gap_chart(), use_container_width=True, config={"displayModeBar": False})

    col_f, col_d = st.columns(2)
    with col_f:
        st.markdown('<div class="section-header">Pipeline Funnel</div>', unsafe_allow_html=True)
        st.plotly_chart(make_funnel(), use_container_width=True, config={"displayModeBar": False})
    with col_d:
        st.markdown('<div class="section-header">Role Distribution</div>', unsafe_allow_html=True)
        roles = [c["role"] for c in CANDIDATES]
        role_counts = pd.Series(roles).value_counts()
        fig_pie = go.Figure(go.Pie(
            labels=role_counts.index.tolist(),
            values=role_counts.values.tolist(),
            hole=0.55,
            marker=dict(colors=["#00d4ff","#4ade80","#fbbf24","#a78bfa","#f87171"],
                        line=dict(color="rgba(0,10,30,0.8)", width=2)),
            textfont=dict(color="#c8e6ff", family="Outfit", size=12),
            textinfo="label+percent",
        ))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            height=280,
            annotations=[dict(text="Roles", x=0.5, y=0.5, font_size=14, font_color="#7aabcc", showarrow=False)]
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    # Match score over time
    st.markdown('<div class="section-header">Match Score Trend (Last 8 Weeks)</div>', unsafe_allow_html=True)
    dates = pd.date_range(end="2025-03-16", periods=8, freq="W")
    scores_trend = [65, 67, 70, 69, 72, 74, 73, 74]
    shortlist_trend = [30, 33, 38, 36, 41, 44, 45, 47]
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=dates, y=scores_trend, mode="lines+markers", name="Avg Match Score",
        line=dict(color="#00d4ff", width=2.5), marker=dict(color="#00d4ff", size=7),
        fill="tozeroy", fillcolor="rgba(0,180,255,0.05)"))
    fig_trend.add_trace(go.Scatter(x=dates, y=shortlist_trend, mode="lines+markers", name="Shortlisted",
        line=dict(color="#4ade80", width=2, dash="dot"), marker=dict(color="#4ade80", size=6)))
    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,10,30,0.4)",
        xaxis=dict(tickfont=dict(color="#7aabcc"), gridcolor="rgba(0,180,255,0.07)"),
        yaxis=dict(tickfont=dict(color="#4a6f8f"), gridcolor="rgba(0,180,255,0.07)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#7aabcc")),
        margin=dict(t=10, b=10, l=30, r=10), height=250,
    )
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})


# ════════════════════════════════════════════════════════════════════════════
# PAGE: AI RECRUITER CHATBOT
# ════════════════════════════════════════════════════════════════════════════
elif "💬 AI Recruiter" in page:
    st.markdown('<div class="section-header">AI Recruiter Assistant</div>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            ("ai", "👋 Hello! I'm your AI Recruiter. Ask me anything about the candidate pipeline, match scores, skill gaps, or shortlisted talent.\n\nTry: *'Show top candidates for Data Engineer role'*")
        ]

    # Render chat
    chat_container = st.container()
    with chat_container:
        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.markdown(f'<div class="chat-label-user">You</div><div class="chat-user">{msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-label-ai">🧠 AI Recruiter</div><div class="chat-ai">{msg}</div>', unsafe_allow_html=True)

    # Suggestions
    st.markdown("<br>", unsafe_allow_html=True)
    suggestion_cols = st.columns(4)
    suggestions = ["Top Data Engineer candidates", "Average match score", "Shortlisted candidates", "Skill gaps in pool"]
    for col, sug in zip(suggestion_cols, suggestions):
        if col.button(sug, key=f"sug_{sug}"):
            st.session_state.chat_history.append(("user", sug))
            with st.spinner("🧠 Thinking..."):
                time.sleep(0.8)
            st.session_state.chat_history.append(("ai", get_ai_response(sug)))
            st.rerun()

    # Input
    user_input = st.chat_input("Ask the AI Recruiter...")
    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        with st.spinner("🧠 Analyzing..."):
            time.sleep(0.9)
        st.session_state.chat_history.append(("ai", get_ai_response(user_input)))
        st.rerun()
