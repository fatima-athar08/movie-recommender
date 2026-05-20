import streamlit as st
import pickle
import requests
import pandas as pd

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch — AI Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── LOAD DATA ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    movies_raw = pickle.load(open('movies.pkl', 'rb'))
    sim        = pickle.load(open('similarity.pkl', 'rb'))
    df = movies_raw if isinstance(movies_raw, pd.DataFrame) else pd.DataFrame(movies_raw)
    return df, sim

movies, similarity = load_data()

# ── FETCH POSTER ───────────────────────────────────────────────────────────────
def fetch_poster(movie_id):
    try:
        url  = 'https://api.themoviedb.org/3/movie/{}?api_key=f3c107d7f91423722c136ffc4ff90003&language=en-US'.format(movie_id)
        data = requests.get(url, timeout=5).json()
        path = data.get('poster_path')
        if path:
            return 'https://image.tmdb.org/t/p/w500/' + path
    except Exception:
        pass
    return 'https://placehold.co/300x450/101015/e05c20?text=No+Poster'

# ── FETCH DETAILS ──────────────────────────────────────────────────────────────
def fetch_details(movie_id):
    try:
        url  = 'https://api.themoviedb.org/3/movie/{}?api_key=f3c107d7f91423722c136ffc4ff90003&language=en-US'.format(movie_id)
        data = requests.get(url, timeout=5).json()
        return {
            'poster':  'https://image.tmdb.org/t/p/w500/' + data['poster_path'] if data.get('poster_path') else 'https://placehold.co/300x450/101015/e05c20?text=No+Poster',
            'rating':  data.get('vote_average', 'N/A'),
            'year':    data.get('release_date', '')[:4] or 'N/A',
            'genres':  ', '.join([g['name'] for g in data.get('genres', [])]),
        }
    except Exception:
        return {'poster': 'https://placehold.co/300x450/101015/e05c20?text=No+Poster',
                'rating': 'N/A', 'year': 'N/A', 'genres': ''}

# ── RECOMMEND ──────────────────────────────────────────────────────────────────
def recommend(movie):
    idx       = movies[movies['title'] == movie].index[0]
    distances = similarity[idx]
    top5      = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    titles, posters, scores = [], [], []
    for i, score in top5:
        titles.append(movies.iloc[i].title)
        posters.append(fetch_poster(movies.iloc[i].movie_id))
        scores.append(round(score * 100, 1))
    return titles, posters, scores

# ── SIMILARITY SCORE ───────────────────────────────────────────────────────────
def get_similarity_score(m1, m2):
    try:
        i1 = movies[movies['title'] == m1].index[0]
        i2 = movies[movies['title'] == m2].index[0]
        return round(float(similarity[i1][i2]) * 100, 2)
    except:
        return 0.0

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500&display=swap');

/* ── GLOBAL ── */
html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; }
.stApp, [data-testid="stAppViewContainer"] { background: #09090e !important; color: #eeebe6; }

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
.stDeployButton { display: none !important; }

/* ── PADDING FIX ── */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 100% !important;
}

.stMainBlockContainer {
    padding-top: 2rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 100% !important;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 2rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 100% !important;
}
/* ── NAVBAR ── */
.navbar {
    background: #0f0f14;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 15px 44px;
    display: flex;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 999;
}
.nav-logo { font-family:'Bebas Neue',sans-serif; font-size:26px; letter-spacing:3px; color:#eeebe6; }
.nav-logo span { color:#e05c20; }
.nav-pill {
    margin-left:12px; background:rgba(224,92,32,0.12); border:1px solid rgba(224,92,32,0.35);
    color:#e05c20; font-size:9px; font-weight:600; letter-spacing:2px;
    text-transform:uppercase; padding:3px 9px; border-radius:20px;
}
.nav-info { margin-left:auto; font-size:11px; color:rgba(255,255,255,0.28); }
/* ── CONTENT SPACING BELOW NAVBAR ── */
.main .block-container {
    margin-top: 20px !important;
}

/* TAB CONTENT SPACING */
div.stTabs [data-baseweb="tab-panel"] {
    padding-top: 25px !important;
}
/* ── TABS ── */
div.stTabs [data-baseweb="tab-list"] {
    background: #0f0f14 !important;
    padding: 0 44px !important;
    gap: 0 !important;
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
}
div.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(255,255,255,0.4) !important;
    font-size: 13px !important;
    font-family: 'Outfit', sans-serif !important;
    padding: 14px 22px !important;
    border-bottom: 2px solid transparent !important;
}
div.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #e05c20 !important;
    border-bottom: 2px solid #e05c20 !important;
}
div.stTabs [data-baseweb="tab"]:hover { color: rgba(255,255,255,0.7) !important; }
div.stTabs [data-baseweb="tab-highlight"] { background: transparent !important; }
div.stTabs [data-baseweb="tab-border"] { display: none !important; }
div.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; background: transparent !important; }

/* ── SECTION LABELS ── */
.eyebrow { font-size:10px; letter-spacing:3px; text-transform:uppercase; color:#e05c20; margin-bottom:10px; }
.big-title { font-family:'Bebas Neue',sans-serif; font-size:58px; line-height:1.0; letter-spacing:2px; color:#eeebe6; margin-bottom:12px; }
.big-title em { color:#e05c20; font-style:normal; }
.hero-desc { font-size:15px; font-weight:300; color:rgba(238,235,230,0.5); line-height:1.75; max-width:500px; margin-bottom:28px; }
.sec-label { font-size:10px; letter-spacing:2.5px; text-transform:uppercase; color:rgba(255,255,255,0.28); margin-bottom:10px; }
.sec-title { font-family:'Bebas Neue',sans-serif; font-size:28px; letter-spacing:2px; color:#eeebe6; margin-bottom:6px; }
.sec-desc { font-size:14px; color:rgba(255,255,255,0.4); margin-bottom:28px; line-height:1.7; }

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    background:#13131a !important; border:1px solid rgba(255,255,255,0.09) !important;
    border-radius:11px !important; color:#eeebe6 !important; font-size:15px !important;
}
.stSelectbox > div > div:hover { border-color:rgba(224,92,32,0.45) !important; }
.stSelectbox svg { fill:#e05c20 !important; }

/* ── BUTTON ── */
.stButton > button {
    background:#e05c20 !important; color:#fff !important; border:none !important;
    border-radius:11px !important; font-family:'Bebas Neue',sans-serif !important;
    font-size:19px !important; letter-spacing:1.8px !important;
    padding:9px 32px !important; width:100% !important;
}
.stButton > button:hover { background:#bf4c14 !important; }

/* ── MOVIE CARD ── */
.mcard {
    background:#101015; border-radius:13px; overflow:hidden;
    border:1px solid rgba(255,255,255,0.055);
    transition:transform 0.22s ease, border-color 0.22s ease;
}
.mcard:hover { transform:translateY(-5px); border-color:rgba(224,92,32,0.7); }
.mcard img { width:100%; display:block; aspect-ratio:2/3; object-fit:cover; }
.mcard-body { padding:12px 13px 14px; }
.mcard-rank { font-size:9px; letter-spacing:2px; text-transform:uppercase; color:#e05c20; margin-bottom:4px; }
.mcard-name { font-size:13px; font-weight:500; color:#eeebe6; line-height:1.3; margin-bottom:6px; }
.mcard-meta { font-size:11px; color:rgba(255,255,255,0.3); margin-bottom:4px; }
.mcard-genre { font-size:10px; color:rgba(255,255,255,0.25); margin-bottom:7px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.rating-badge { display:inline-block; background:rgba(224,92,32,0.15); border:1px solid rgba(224,92,32,0.3); color:#e05c20; font-size:10px; padding:2px 7px; border-radius:6px; margin-bottom:6px; }
.bar-track { background:rgba(255,255,255,0.07); border-radius:3px; height:2px; width:100%; }
.bar-fill { background:#e05c20; border-radius:3px; height:2px; }
.bar-pct { font-size:9px; color:rgba(255,255,255,0.3); margin-top:4px; }

/* ── WHY BOX ── */
.why-wrap {
    background:#101015; border:1px solid rgba(255,255,255,0.055);
    border-left:3px solid #e05c20; border-radius:13px; padding:18px 22px; margin-top:20px;
}
.why-label { font-size:9px; letter-spacing:2.5px; text-transform:uppercase; color:#e05c20; margin-bottom:7px; }
.why-body { font-size:13px; font-weight:300; color:rgba(238,235,230,0.65); line-height:1.85; }
.why-body b { color:#eeebe6; font-weight:500; }

/* ── CHAT ── */
.chat-user {
    background:rgba(224,92,32,0.12); border:1px solid rgba(224,92,32,0.2);
    border-radius:13px 13px 4px 13px; padding:12px 16px;
    font-size:14px; color:#eeebe6; margin-bottom:12px; max-width:80%; margin-left:auto;
}
.chat-ai {
    background:#101015; border:1px solid rgba(255,255,255,0.055);
    border-radius:13px 13px 13px 4px; padding:12px 16px;
    font-size:14px; color:rgba(238,235,230,0.8); margin-bottom:12px; max-width:85%; line-height:1.7;
}
.chat-lbl { font-size:9px; letter-spacing:2px; text-transform:uppercase; margin-bottom:5px; }
.chat-lbl-user { color:#e05c20; text-align:right; }
.chat-lbl-ai { color:rgba(255,255,255,0.3); }

/* ── STATS ── */
.stats-grid { display:flex; gap:14px; flex-wrap:wrap; margin-bottom:28px; }
.stat-card {
    background:#101015; border:1px solid rgba(255,255,255,0.055);
    border-radius:13px; padding:18px 24px; flex:1; min-width:130px; text-align:center;
}
.stat-val { font-family:'Bebas Neue',sans-serif; font-size:30px; color:#e05c20; line-height:1; margin-bottom:5px; }
.stat-lbl { font-size:9px; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,0.3); }

/* ── COMPARE ── */
.compare-card { background:#101015; border:1px solid rgba(255,255,255,0.055); border-radius:13px; padding:20px; text-align:center; }
.big-score { font-family:'Bebas Neue',sans-serif; font-size:58px; color:#e05c20; line-height:1; }
.score-bar-bg { background:rgba(255,255,255,0.07); border-radius:6px; height:8px; width:100%; margin:14px 0 8px; }
.score-bar-fill { background:linear-gradient(90deg,#e05c20,#f5834d); border-radius:6px; height:8px; }

/* ── PIPELINE ── */
.pipeline-grid { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:24px; }
.pipe-step { background:#101015; border:1px solid rgba(255,255,255,0.055); border-radius:13px; padding:16px; flex:1; min-width:140px; }
.pipe-num { font-family:'Bebas Neue',sans-serif; font-size:34px; color:rgba(224,92,32,0.2); line-height:1; margin-bottom:7px; }
.pipe-title { font-size:13px; font-weight:500; color:#eeebe6; margin-bottom:4px; }
.pipe-code { font-size:10px; color:#e05c20; font-family:monospace; background:rgba(224,92,32,0.08); padding:3px 7px; border-radius:4px; display:inline-block; margin-top:4px; }
.pipe-desc { font-size:11px; color:rgba(255,255,255,0.35); line-height:1.6; margin-top:5px; }

/* ── TECH TABLE ── */
.tech-table { background:#101015; border:1px solid rgba(255,255,255,0.055); border-radius:13px; overflow:hidden; }
.tech-row-item { display:flex; align-items:center; gap:12px; padding:12px 18px; border-bottom:1px solid rgba(255,255,255,0.04); }
.tech-row-item:last-child { border-bottom:none; }
.tech-nm { font-size:13px; font-weight:500; color:#eeebe6; min-width:170px; }
.tech-dc { font-size:12px; color:rgba(255,255,255,0.4); flex:1; }
.tech-tg { font-size:9px; padding:3px 9px; border-radius:20px; letter-spacing:1px; font-weight:600; text-transform:uppercase; white-space:nowrap; }
.tg-ml  { background:rgba(59,130,246,0.15); border:1px solid rgba(59,130,246,0.3); color:#60a5fa; }
.tg-ui  { background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3); color:#34d399; }
.tg-ai  { background:rgba(139,92,246,0.15); border:1px solid rgba(139,92,246,0.3); color:#a78bfa; }
.tg-dep { background:rgba(236,72,153,0.15); border:1px solid rgba(236,72,153,0.3); color:#f472b6; }
.tg-dt  { background:rgba(245,158,11,0.15); border:1px solid rgba(245,158,11,0.3); color:#fbbf24; }

/* ── TEXT INPUT ── */
.stTextInput > div > div > input {
    background:#13131a !important; border:1px solid rgba(255,255,255,0.09) !important;
    border-radius:11px !important; color:#eeebe6 !important; font-family:'Outfit',sans-serif !important;
}

/* ── RULED LINE ── */
.ruled { height:1px; background:linear-gradient(90deg,rgba(224,92,32,0.45),rgba(255,255,255,0.04),transparent); margin:28px 0; }

/* ── FOOTER ── */
.foot { border-top:1px solid rgba(255,255,255,0.055); padding:20px 44px; display:flex; align-items:center; margin-top:40px; }
.foot-logo { font-family:'Bebas Neue',sans-serif; font-size:16px; letter-spacing:2px; color:rgba(255,255,255,0.2); }
.foot-logo span { color:rgba(224,92,32,0.45); }
.foot-right { margin-left:auto; font-size:10px; color:rgba(255,255,255,0.18); }
.stSpinner > div { border-top-color:#e05c20 !important; }
</style>
""", unsafe_allow_html=True)

# ── NAVBAR ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="nav-logo">CINE<span>MATCH</span></div>
    <div class="nav-pill">AI Powered</div>
    <div class="nav-info">TF-IDF &nbsp;·&nbsp; Cosine Similarity &nbsp;·&nbsp; TMDB 5000</div>
</div>
""", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🎬 Recommend", "⚖️ Compare Movies", "📊 Dashboard", "🧠 How It Works"
])
# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — RECOMMEND
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    with st.container():
        st.markdown('', unsafe_allow_html=True)
        st.markdown("""
        <div class="eyebrow">✦ Machine Learning · Content-Based Filtering</div>
        <div class="big-title">FIND YOUR<br>NEXT <em>FAVOURITE</em><br>FILM.</div>
        <div class="hero-desc">
            An AI-powered recommendation engine trained on 5,000+ movies.
            Pick any title and instantly discover films that share the same
            themes, cast, genre, and directorial style.
        </div>
        """, unsafe_allow_html=True)

        col_sel, col_btn, col_gap = st.columns([3, 1, 2])
        with col_sel:
            selected_movie = st.selectbox("movie", movies['title'].values,
                                          label_visibility="collapsed", key="rec_select")
        with col_btn:
            rec_clicked = st.button("RECOMMEND →", key="rec_btn")

        if rec_clicked:
            with st.spinner("Finding your perfect films..."):
                names, posters, scores = recommend(selected_movie)

            bar_widths = [98, 94, 90, 86, 82]

            st.markdown(f"""
            <div style="padding:24px 0 14px; display:flex; align-items:baseline; gap:12px;">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:26px;letter-spacing:2px;color:#eeebe6;">TOP 5 RECOMMENDATIONS</div>
                <div style="font-size:12px;color:rgba(255,255,255,0.3);">based on "{selected_movie}"</div>
            </div>
            """, unsafe_allow_html=True)

            cols = st.columns(5)
            for i, col in enumerate(cols):
                mid = movies[movies['title'] == names[i]]['movie_id'].values
                det = fetch_details(mid[0]) if len(mid) > 0 else {}
                with col:
                    st.markdown(f"""
                    <div class="mcard">
                        <img src="{posters[i]}" alt="{names[i]}" />
                        <div class="mcard-body">
                            <div class="mcard-rank">#{i+1} match</div>
                            <div class="mcard-name">{names[i]}</div>
                            <div class="mcard-meta">{det.get('year','')} &nbsp;·&nbsp; {det.get('genres','')}</div>
                            <div class="rating-badge">⭐ {det.get('rating','N/A')}/10</div>
                            <div class="bar-track">
                                <div class="bar-fill" style="width:{bar_widths[i]}%"></div>
                            </div>
                            <div class="bar-pct">{bar_widths[i]}% similarity</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="why-wrap">
                <div class="why-label">✦ Why these recommendations?</div>
                <div class="why-body">
                    You selected <b>{selected_movie}</b>. The model extracted cast, crew,
                    genres, and keywords — merged into a <b>tags</b> string per film.
                    Each film was converted into a <b>TF-IDF vector</b> and
                    <b>cosine similarity</b> found the 5 closest matches.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — COMPARE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    with st.container():
        st.markdown('', unsafe_allow_html=True)
        st.markdown("""
        <div class="sec-label">✦ Cosine Similarity Score</div>
        <div class="sec-title">COMPARE ANY TWO MOVIES</div>
        <div class="sec-desc">
            Select any two films and see their exact cosine similarity score —
            the same metric the recommendation engine uses internally.
        </div>
        """, unsafe_allow_html=True)

        c1, c_vs, c2 = st.columns([5, 1, 5])
        with c1:
            st.markdown('<div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:8px;">First movie</div>', unsafe_allow_html=True)
            movie_a = st.selectbox("Movie A", movies['title'].values,
                                   key="compare_a", label_visibility="collapsed")
        with c_vs:
            st.markdown('<div style="text-align:center;padding-top:28px;font-family:\'Bebas Neue\',sans-serif;font-size:20px;color:rgba(255,255,255,0.2);">VS</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:8px;">Second movie</div>', unsafe_allow_html=True)
            movie_b = st.selectbox("Movie B", movies['title'].values,
                                   index=10, key="compare_b", label_visibility="collapsed")

        compare_clicked = st.button("COMPARE →", key="compare_btn")

        if compare_clicked:
            with st.spinner("Calculating similarity..."):
                score = get_similarity_score(movie_a, movie_b)
                mid_a = movies[movies['title'] == movie_a]['movie_id'].values
                mid_b = movies[movies['title'] == movie_b]['movie_id'].values
                det_a = fetch_details(mid_a[0]) if len(mid_a) > 0 else {}
                det_b = fetch_details(mid_b[0]) if len(mid_b) > 0 else {}

            st.markdown('<div style="margin-top:24px;"></div>', unsafe_allow_html=True)
            col_a, col_sc, col_b = st.columns([3, 2, 3])

            verdict = "Very Similar" if score >= 25 else "Somewhat Similar" if score >= 10 else "Not Very Similar"
            vcolor  = "#34d399" if score >= 25 else "#fbbf24" if score >= 10 else "#f87171"
            bar_w   = min(score * 3, 100)

            with col_a:
                st.markdown(f"""
                <div class="compare-card">
                    <img src="{det_a.get('poster','')}" style="width:100%;border-radius:8px;aspect-ratio:2/3;object-fit:cover;margin-bottom:12px;" />
                    <div style="font-size:14px;font-weight:500;color:#eeebe6;margin-bottom:4px;">{movie_a}</div>
                    <div style="font-size:12px;color:rgba(255,255,255,0.35);">{det_a.get('year','')} · ⭐ {det_a.get('rating','')}</div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.2);margin-top:3px;">{det_a.get('genres','')}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_sc:
                st.markdown(f"""
                <div class="compare-card" style="padding:28px 16px;">
                    <div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:10px;">Similarity Score</div>
                    <div class="big-score">{score}%</div>
                    <div class="score-bar-bg">
                        <div class="score-bar-fill" style="width:{bar_w}%"></div>
                    </div>
                    <div style="font-size:13px;font-weight:500;color:{vcolor};margin-top:6px;">{verdict}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.2);margin-top:8px;line-height:1.6;">Based on TF-IDF cosine similarity of their tags vectors</div>
                </div>
                """, unsafe_allow_html=True)

            with col_b:
                st.markdown(f"""
                <div class="compare-card">
                    <img src="{det_b.get('poster','')}" style="width:100%;border-radius:8px;aspect-ratio:2/3;object-fit:cover;margin-bottom:12px;" />
                    <div style="font-size:14px;font-weight:500;color:#eeebe6;margin-bottom:4px;">{movie_b}</div>
                    <div style="font-size:12px;color:rgba(255,255,255,0.35);">{det_b.get('year','')} · ⭐ {det_b.get('rating','')}</div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.2);margin-top:3px;">{det_b.get('genres','')}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    with st.container():
        st.markdown('', unsafe_allow_html=True)
        st.markdown("""
        <div class="sec-label">✦ Dataset Statistics</div>
        <div class="sec-title">PROJECT DASHBOARD</div>
        <div class="sec-desc">Live statistics and visualisations about the TMDB 5000 dataset and ML model.</div>
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-val">4,806</div><div class="stat-lbl">Total Movies</div></div>
            <div class="stat-card"><div class="stat-val">5,000</div><div class="stat-lbl">Vector Dims</div></div>
            <div class="stat-card"><div class="stat-val">TF-IDF</div><div class="stat-lbl">Vectorizer</div></div>
            <div class="stat-card"><div class="stat-val">Cosine</div><div class="stat-lbl">Similarity</div></div>
            <div class="stat-card"><div class="stat-val">~180 MB</div><div class="stat-lbl">Model Size</div></div>
            <div class="stat-card"><div class="stat-val">CBF</div><div class="stat-lbl">Algorithm</div></div>
        </div>
        <div class="ruled"></div>
        """, unsafe_allow_html=True)

        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown('<div class="sec-label">▸ Pipeline complexity by step</div>', unsafe_allow_html=True)
            st.bar_chart(pd.DataFrame({
                'Step': ['Load','Clean','Extract','Stemming','TF-IDF','Similarity','Export'],
                'Complexity': [1, 1, 4, 2, 3, 5, 1]
            }).set_index('Step'), color='#e05c20')

        with col_right:
            st.markdown('<div class="sec-label">▸ Technology breakdown (lines of code)</div>', unsafe_allow_html=True)
            st.bar_chart(pd.DataFrame({
                'Library': ['Pandas','Streamlit','Scikit-learn','NLTK','Requests'],
                'Lines': [12, 60, 8, 5, 6]
            }).set_index('Library'), color='#e05c20')

        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
        col_l2, col_r2 = st.columns(2)
        with col_l2:
            st.markdown('<div class="sec-label">▸ Dataset overview</div>', unsafe_allow_html=True)
            st.bar_chart(pd.DataFrame({
                'Metric': ['Raw Movies','After Cleaning','Features Used','Max Vectors (K)'],
                'Count': [4803, 4806, 7, 5]
            }).set_index('Metric'), color='#e05c20')

        with col_r2:
            st.markdown('<div class="sec-label">▸ Similarity matrix stats</div>', unsafe_allow_html=True)
            st.bar_chart(pd.DataFrame({
                'Metric': ['Movies','Pairs (M)','Dimensions (K)','File Size (MB)'],
                'Value': [4806, 23, 5, 180]
            }).set_index('Metric'), color='#e05c20')

        st.markdown('', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — HOW IT WORKS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    with st.container():
        st.markdown('', unsafe_allow_html=True)
        st.markdown("""
        <div class="sec-label">✦ ML Pipeline</div>
        <div class="sec-title">HOW THE MODEL WORKS</div>
        <div class="sec-desc">Complete walkthrough of the 10-step ML pipeline from raw CSV to live recommendations.</div>

        <div class="pipeline-grid">
            <div class="pipe-step"><div class="pipe-num">01</div><div class="pipe-title">Load & Merge</div><div class="pipe-desc">Two CSVs merged on title column using pandas.</div><div class="pipe-code">movies.merge(credits)</div></div>
            <div class="pipe-step"><div class="pipe-num">02</div><div class="pipe-title">Select Features</div><div class="pipe-desc">Keep movie_id, genres, keywords, title, overview, cast, crew.</div><div class="pipe-code">movies[['title',...]]</div></div>
            <div class="pipe-step"><div class="pipe-num">03</div><div class="pipe-title">Data Cleaning</div><div class="pipe-desc">Remove null rows and check duplicates.</div><div class="pipe-code">dropna()</div></div>
            <div class="pipe-step"><div class="pipe-num">04</div><div class="pipe-title">Feature Extraction</div><div class="pipe-desc">3 functions parse JSON: convert(), convert3(), fetch_director().</div><div class="pipe-code">ast.literal_eval()</div></div>
            <div class="pipe-step"><div class="pipe-num">05</div><div class="pipe-title">Build Tags</div><div class="pipe-desc">All features merged into one string per movie.</div><div class="pipe-code">new_df['tags']</div></div>
            <div class="pipe-step"><div class="pipe-num">06</div><div class="pipe-title">Stemming</div><div class="pipe-desc">PorterStemmer reduces words to root form.</div><div class="pipe-code">ps.stem(word)</div></div>
            <div class="pipe-step"><div class="pipe-num">07</div><div class="pipe-title">TF-IDF Vectors</div><div class="pipe-desc">Each movie → 5,000-dimensional numerical vector.</div><div class="pipe-code">TfidfVectorizer()</div></div>
            <div class="pipe-step"><div class="pipe-num">08</div><div class="pipe-title">Cosine Similarity</div><div class="pipe-desc">4806×4806 similarity matrix computed.</div><div class="pipe-code">cosine_similarity()</div></div>
            <div class="pipe-step"><div class="pipe-num">09</div><div class="pipe-title">Recommend</div><div class="pipe-desc">Sort by score, return top 5 excluding itself.</div><div class="pipe-code">sorted(...)[1:6]</div></div>
            <div class="pipe-step"><div class="pipe-num">10</div><div class="pipe-title">Export</div><div class="pipe-desc">Save movies.pkl and similarity.pkl for fast loading.</div><div class="pipe-code">pickle.dump()</div></div>
        </div>

        <div class="ruled"></div>
        <div class="sec-label">▸ Technology stack</div>
        <div class="tech-table">
            <div class="tech-row-item"><div class="tech-nm">Python 3</div><div class="tech-dc">Core language for all data processing and ML</div><span class="tech-tg tg-ml">ML</span></div>
            <div class="tech-row-item"><div class="tech-nm">Pandas</div><div class="tech-dc">Load CSVs, merge datasets, clean columns</div><span class="tech-tg tg-dt">Data</span></div>
            <div class="tech-row-item"><div class="tech-nm">NLTK / PorterStemmer</div><div class="tech-dc">Reduces words to root form for better matching</div><span class="tech-tg tg-ml">ML</span></div>
            <div class="tech-row-item"><div class="tech-nm">TfidfVectorizer</div><div class="tech-dc">Converts tags text into 5,000-dimensional vectors</div><span class="tech-tg tg-ml">ML</span></div>
            <div class="tech-row-item"><div class="tech-nm">Cosine Similarity</div><div class="tech-dc">Measures angle between vectors — 1.0 = identical</div><span class="tech-tg tg-ml">ML</span></div>
            <div class="tech-row-item"><div class="tech-nm">Pickle</div><div class="tech-dc">Saves pre-computed model for instant loading</div><span class="tech-tg tg-dt">Data</span></div>
            <div class="tech-row-item"><div class="tech-nm">Streamlit</div><div class="tech-dc">Python web framework — builds and serves the app</div><span class="tech-tg tg-ui">UI</span></div>
            <div class="tech-row-item"><div class="tech-nm">HTML + CSS</div><div class="tech-dc">Custom dark theme via st.markdown(unsafe_allow_html)</div><span class="tech-tg tg-ui">UI</span></div>
            <div class="tech-row-item"><div class="tech-nm">TMDB API</div><div class="tech-dc">Real-time movie posters, ratings, genres</div><span class="tech-tg tg-ui">UI</span></div>
            <div class="tech-row-item"><div class="tech-nm">Claude AI (Anthropic)</div><div class="tech-dc">Powers AI Chat tab — mood-based recommendations</div><span class="tech-tg tg-ai">AI</span></div>
            <div class="tech-row-item"><div class="tech-nm">GitHub + Streamlit Cloud</div><div class="tech-dc">Version control and live deployment</div><span class="tech-tg tg-dep">Deploy</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('', unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="foot">
    <div class="foot-logo">CINE<span>MATCH</span></div>
    <div class="foot-right">
        Python · Streamlit · Scikit-learn · TMDB API    
        &nbsp;|&nbsp; Data Encryption &amp; Security — Final Year Project
    </div>
</div>
""", unsafe_allow_html=True)

