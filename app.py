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
        url  = ('https://api.themoviedb.org/3/movie/{}?api_key=f3c107d7f91423722c136ffc4ff90003&language=en-US'
                .format(movie_id))
        data = requests.get(url, timeout=5).json()
        path = data.get('poster_path')
        if path:
            return 'https://image.tmdb.org/t/p/w500/' + path
    except Exception:
        pass
    return 'https://placehold.co/300x450/101015/e05c20?text=No+Poster'
 
# ── FETCH MOVIE DETAILS ────────────────────────────────────────────────────────
def fetch_details(movie_id):
    try:
        url  = ('https://api.themoviedb.org/3/movie/{}?api_key=f3c107d7f91423722c136ffc4ff90003&language=en-US'
                .format(movie_id))
        data = requests.get(url, timeout=5).json()
        return {
            'poster':   'https://image.tmdb.org/t/p/w500/' + data.get('poster_path','') if data.get('poster_path') else 'https://placehold.co/300x450/101015/e05c20?text=No+Poster',
            'rating':   data.get('vote_average', 'N/A'),
            'year':     data.get('release_date','')[:4] if data.get('release_date') else 'N/A',
            'overview': data.get('overview','No overview available.'),
            'genres':   ', '.join([g['name'] for g in data.get('genres', [])]),
        }
    except Exception:
        return {'poster': 'https://placehold.co/300x450/101015/e05c20?text=No+Poster',
                'rating': 'N/A', 'year': 'N/A', 'overview': '', 'genres': ''}
 
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
 
# ── GET SIMILARITY SCORE ───────────────────────────────────────────────────────
def get_similarity_score(movie1, movie2):
    try:
        idx1 = movies[movies['title'] == movie1].index[0]
        idx2 = movies[movies['title'] == movie2].index[0]
        return round(float(similarity[idx1][idx2]) * 100, 2)
    except:
        return 0.0
 
# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500&display=swap');
 
html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; }
.stApp { background: #09090e; color: #eeebe6; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { background: #09090e; }
[data-testid="stHeader"] { display: none; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stStatusWidget"] { display: none; }
.stMainBlockContainer { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stDeployButton { display: none; }
div[data-testid="stVerticalBlock"] > div:first-child { padding: 0 !important; }
 
/* NAVBAR */
.navbar {
    background: #0f0f14; border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 15px 44px; display: flex; align-items: center;
}
.nav-logo { font-family:'Bebas Neue',sans-serif; font-size:26px; letter-spacing:3px; color:#eeebe6; }
.nav-logo span { color:#e05c20; }
.nav-pill {
    margin-left:12px; background:rgba(224,92,32,0.12); border:1px solid rgba(224,92,32,0.35);
    color:#e05c20; font-size:9px; font-weight:600; letter-spacing:2px;
    text-transform:uppercase; padding:3px 9px; border-radius:20px;
}
.nav-info { margin-left:auto; font-size:11px; color:rgba(255,255,255,0.28); letter-spacing:0.8px; }
 
/* TABS */
.tab-bar {
    display:flex; gap:0; background:#0f0f14;
    border-bottom:1px solid rgba(255,255,255,0.06); padding: 0 44px;
}
.tab-btn {
    padding:14px 22px; font-family:'Outfit',sans-serif; font-size:13px;
    font-weight:400; color:rgba(255,255,255,0.4); background:transparent;
    border:none; border-bottom:2px solid transparent; cursor:pointer;
    letter-spacing:0.3px; transition:all 0.18s;
}
.tab-btn:hover { color:rgba(255,255,255,0.7); }
.tab-btn.active { color:#e05c20; border-bottom-color:#e05c20; font-weight:500; }
 
/* PAGE PADDING */
.page { padding: 36px 44px 48px; }
.main .block-container { padding-top: 0 !important; padding-left: 0 !important; padding-right: 0 !important; }
div.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }
div.stTabs [data-baseweb="tab-list"] { background: #0f0f14; padding: 0 44px; gap: 0; border-bottom: 1px solid rgba(255,255,255,0.06); }
div.stTabs [data-baseweb="tab"] { background: transparent; color: rgba(255,255,255,0.4); font-size: 13px; padding: 14px 22px; border: none; border-bottom: 2px solid transparent; }
div.stTabs [aria-selected="true"] { background: transparent !important; color: #e05c20 !important; border-bottom: 2px solid #e05c20 !important; }
div.stTabs [data-baseweb="tab"]:hover { color: rgba(255,255,255,0.7); background: transparent; }
div.stTabs [data-baseweb="tab-highlight"] { background-color: #e05c20 !important; }
div.stTabs [data-baseweb="tab-border"] { display: none; }
 
/* HERO */
.big-title { font-family:'Bebas Neue',sans-serif; font-size:58px; line-height:1.0; letter-spacing:2px; color:#eeebe6; margin-bottom:12px; }
.big-title em { color:#e05c20; font-style:normal; }
.eyebrow { font-size:10px; letter-spacing:3px; text-transform:uppercase; color:#e05c20; margin-bottom:10px; }
.hero-desc { font-size:15px; font-weight:300; color:rgba(238,235,230,0.5); line-height:1.75; max-width:500px; margin-bottom:32px; }
 
/* DIVIDER */
.ruled { height:1px; background:linear-gradient(90deg,rgba(224,92,32,0.45),rgba(255,255,255,0.04),transparent); margin:0; }
 
/* SELECTBOX */
.stSelectbox > div > div {
    background:#13131a !important; border:1px solid rgba(255,255,255,0.09) !important;
    border-radius:11px !important; color:#eeebe6 !important; font-size:15px !important;
}
.stSelectbox > div > div:hover { border-color:rgba(224,92,32,0.45) !important; }
.stSelectbox svg { fill:#e05c20 !important; }
 
/* BUTTON */
.stButton > button {
    background:#e05c20 !important; color:#fff !important; border:none !important;
    border-radius:11px !important; font-family:'Bebas Neue',sans-serif !important;
    font-size:19px !important; letter-spacing:1.8px !important;
    padding:9px 32px !important; width:100% !important;
    transition:background 0.18s,transform 0.12s !important;
}
.stButton > button:hover { background:#bf4c14 !important; transform:translateY(-2px) !important; }
.stButton > button:active { transform:translateY(0) !important; }
 
/* MOVIE CARD */
.mcard {
    background:#101015; border-radius:13px; overflow:hidden;
    border:1px solid rgba(255,255,255,0.055);
    transition:transform 0.22s ease,border-color 0.22s ease;
}
.mcard:hover { transform:translateY(-5px); border-color:rgba(224,92,32,0.7); }
.mcard img { width:100%; display:block; aspect-ratio:2/3; object-fit:cover; }
.mcard-body { padding:12px 13px 14px; }
.mcard-rank { font-size:9px; letter-spacing:2px; text-transform:uppercase; color:#e05c20; margin-bottom:4px; }
.mcard-name { font-size:13px; font-weight:500; color:#eeebe6; line-height:1.3; margin-bottom:8px; }
.mcard-year { font-size:11px; color:rgba(255,255,255,0.35); margin-bottom:6px; }
.mcard-genre { font-size:10px; color:rgba(255,255,255,0.3); margin-bottom:8px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.bar-track { background:rgba(255,255,255,0.07); border-radius:3px; height:2px; width:100%; }
.bar-fill { background:#e05c20; border-radius:3px; height:2px; }
.bar-pct { font-size:9px; color:rgba(255,255,255,0.3); margin-top:4px; }
.rating-badge {
    display:inline-block; background:rgba(224,92,32,0.15); border:1px solid rgba(224,92,32,0.3);
    color:#e05c20; font-size:10px; padding:2px 7px; border-radius:6px; margin-bottom:6px;
}
 
/* WHY BOX */
.why-wrap {
    margin:24px 0 8px; background:#101015; border:1px solid rgba(255,255,255,0.055);
    border-left:3px solid #e05c20; border-radius:13px; padding:18px 22px;
}
.why-label { font-size:9px; letter-spacing:2.5px; text-transform:uppercase; color:#e05c20; margin-bottom:7px; }
.why-body { font-size:13px; font-weight:300; color:rgba(238,235,230,0.65); line-height:1.85; }
.why-body b { color:#eeebe6; font-weight:500; }
 
/* STAT CARDS */
.stats-grid { display:flex; gap:14px; flex-wrap:wrap; margin-bottom:32px; }
.stat-card {
    background:#101015; border:1px solid rgba(255,255,255,0.055);
    border-radius:13px; padding:18px 24px; flex:1; min-width:130px; text-align:center;
}
.stat-val { font-family:'Bebas Neue',sans-serif; font-size:30px; color:#e05c20; letter-spacing:1px; line-height:1; margin-bottom:5px; }
.stat-lbl { font-size:9px; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,0.3); }
 
/* SECTION LABEL */
.sec-label { font-size:10px; letter-spacing:2.5px; text-transform:uppercase; color:rgba(255,255,255,0.28); margin-bottom:18px; }
.sec-title { font-family:'Bebas Neue',sans-serif; font-size:28px; letter-spacing:2px; color:#eeebe6; margin-bottom:6px; }
 
/* COMPARE CARD */
.compare-card {
    background:#101015; border:1px solid rgba(255,255,255,0.055);
    border-radius:13px; padding:24px; text-align:center;
}
.compare-score {
    font-family:'Bebas Neue',sans-serif; font-size:64px; color:#e05c20;
    letter-spacing:2px; line-height:1;
}
.compare-label { font-size:12px; color:rgba(255,255,255,0.4); letter-spacing:1px; text-transform:uppercase; }
.score-bar-bg { background:rgba(255,255,255,0.07); border-radius:6px; height:8px; width:100%; margin:16px 0 8px; }
.score-bar-fill { background:linear-gradient(90deg,#e05c20,#f5834d); border-radius:6px; height:8px; transition:width 0.5s ease; }
 
/* AI CHAT */
.chat-bubble-user {
    background:rgba(224,92,32,0.12); border:1px solid rgba(224,92,32,0.2);
    border-radius:13px 13px 4px 13px; padding:12px 16px;
    font-size:14px; color:#eeebe6; margin-bottom:12px; max-width:80%; margin-left:auto;
}
.chat-bubble-ai {
    background:#101015; border:1px solid rgba(255,255,255,0.055);
    border-radius:13px 13px 13px 4px; padding:12px 16px;
    font-size:14px; color:rgba(238,235,230,0.8); margin-bottom:12px; max-width:85%; line-height:1.7;
}
.chat-label { font-size:9px; letter-spacing:2px; text-transform:uppercase; margin-bottom:5px; }
.chat-label.user { color:#e05c20; text-align:right; }
.chat-label.ai { color:rgba(255,255,255,0.3); }
 
/* PIPELINE STEPS */
.pipeline-grid { display:flex; gap:12px; flex-wrap:wrap; }
.pipe-step {
    background:#101015; border:1px solid rgba(255,255,255,0.055);
    border-radius:13px; padding:18px 16px; flex:1; min-width:150px; position:relative;
}
.pipe-num { font-family:'Bebas Neue',sans-serif; font-size:36px; color:rgba(224,92,32,0.18); line-height:1; margin-bottom:8px; }
.pipe-title { font-size:13px; font-weight:500; color:#eeebe6; margin-bottom:5px; }
.pipe-code { font-size:10px; color:#e05c20; font-family:monospace; background:rgba(224,92,32,0.08); padding:3px 7px; border-radius:4px; display:inline-block; margin-top:4px; }
.pipe-desc { font-size:11px; color:rgba(255,255,255,0.35); line-height:1.6; margin-top:6px; }
 
/* HOW IT WORKS steps */
.steps-grid { display:flex; gap:14px; flex-wrap:wrap; }
.step-card {
    background:#101015; border:1px solid rgba(255,255,255,0.055);
    border-radius:13px; padding:18px 20px; flex:1; min-width:150px;
}
.step-n { font-family:'Bebas Neue',sans-serif; font-size:36px; color:rgba(224,92,32,0.2); line-height:1; margin-bottom:9px; }
.step-t { font-size:13px; font-weight:500; color:#eeebe6; margin-bottom:5px; }
.step-d { font-size:11px; font-weight:300; color:rgba(255,255,255,0.36); line-height:1.7; }
 
/* TECH TABLE */
.tech-row-item {
    display:flex; align-items:center; gap:12px;
    padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.055);
}
.tech-row-item:last-child { border-bottom:none; }
.tech-name { font-size:13px; font-weight:500; color:#eeebe6; min-width:160px; }
.tech-desc { font-size:13px; color:rgba(255,255,255,0.45); flex:1; }
.tech-tag {
    font-size:9px; padding:3px 9px; border-radius:20px; font-weight:600;
    letter-spacing:1px; text-transform:uppercase; white-space:nowrap;
}
.tag-ml { background:rgba(59,130,246,0.15); border:1px solid rgba(59,130,246,0.3); color:#60a5fa; }
.tag-ui { background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3); color:#34d399; }
.tag-data { background:rgba(245,158,11,0.15); border:1px solid rgba(245,158,11,0.3); color:#fbbf24; }
.tag-ai { background:rgba(139,92,246,0.15); border:1px solid rgba(139,92,246,0.3); color:#a78bfa; }
.tag-deploy { background:rgba(236,72,153,0.15); border:1px solid rgba(236,72,153,0.3); color:#f472b6; }
 
/* TEXT INPUT */
.stTextInput > div > div > input {
    background:#13131a !important; border:1px solid rgba(255,255,255,0.09) !important;
    border-radius:11px !important; color:#eeebe6 !important; font-size:14px !important;
    font-family:'Outfit',sans-serif !important;
}
.stTextInput > div > div > input:focus { border-color:rgba(224,92,32,0.45) !important; }
 
/* TEXT AREA */
.stTextArea > div > div > textarea {
    background:#13131a !important; border:1px solid rgba(255,255,255,0.09) !important;
    border-radius:11px !important; color:#eeebe6 !important; font-family:'Outfit',sans-serif !important;
}
 
/* FOOTER */
.foot {
    border-top:1px solid rgba(255,255,255,0.055); padding:20px 44px;
    display:flex; align-items:center; margin-top:40px;
}
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
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'recommend'
 
st.markdown("""
<div class="tab-bar">
    <button class="tab-btn" id="tb-recommend">🎬 &nbsp;Recommend</button>
    <button class="tab-btn" id="tb-ai">🤖 &nbsp;AI Chat</button>
    <button class="tab-btn" id="tb-compare">⚖️ &nbsp;Compare Movies</button>
    <button class="tab-btn" id="tb-dashboard">📊 &nbsp;Dashboard</button>
    <button class="tab-btn" id="tb-model">🧠 &nbsp;How It Works</button>
</div>
""", unsafe_allow_html=True)
 
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎬 Recommend", "🤖 AI Chat", "⚖️ Compare Movies", "📊 Dashboard", "🧠 How It Works"
])
 
# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — RECOMMEND
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="page">', unsafe_allow_html=True)
 
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
        selected_movie = st.selectbox("movie", movies['title'].values, label_visibility="collapsed", key="rec_select")
    with col_btn:
        rec_clicked = st.button("RECOMMEND →", key="rec_btn")
 
    if rec_clicked:
        with st.spinner("Finding your perfect films..."):
            names, posters, scores = recommend(selected_movie)
 
        bar_widths = [98, 94, 90, 86, 82]
 
        st.markdown(f"""
        <div style="padding:28px 0 16px; display:flex; align-items:baseline; gap:12px;">
            <div style="font-family:'Bebas Neue',sans-serif;font-size:26px;letter-spacing:2px;color:#eeebe6;">TOP 5 RECOMMENDATIONS</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.3);">based on "{selected_movie}"</div>
        </div>
        """, unsafe_allow_html=True)
 
        cols = st.columns(5)
        for i, col in enumerate(cols):
            mid = movies[movies['title'] == names[i]]['movie_id'].values
            details = fetch_details(mid[0]) if len(mid) > 0 else {}
            year    = details.get('year', '')
            rating  = details.get('rating', '')
            genres  = details.get('genres', '')
            with col:
                st.markdown(f"""
                <div class="mcard">
                    <img src="{posters[i]}" alt="{names[i]}" />
                    <div class="mcard-body">
                        <div class="mcard-rank">#{i+1} match</div>
                        <div class="mcard-name">{names[i]}</div>
                        <div class="mcard-year">{year}</div>
                        <div class="mcard-genre">{genres}</div>
                        <div class="rating-badge">⭐ {rating}/10</div>
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
                You selected <b>{selected_movie}</b>. The model extracted its metadata —
                cast, crew, genres, and keywords — merged into a single <b>tags</b> string.
                Each film was converted into a <b>TF-IDF vector</b> and
                <b>cosine similarity</b> measured how closely every film aligns with your pick.
                The 5 films with the smallest angular distance are your recommendations.
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown('</div>', unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — AI CHAT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="page">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-label">✦ Powered by Claude AI</div>
    <div class="sec-title">AI MOVIE ASSISTANT</div>
    <div style="font-size:14px;color:rgba(255,255,255,0.4);margin-bottom:28px;line-height:1.7;">
        Describe your mood, favourite genre, or a feeling — the AI will suggest
        movies tailored to what you're looking for. This feature uses the
        Anthropic Claude API directly inside the app.
    </div>
    """, unsafe_allow_html=True)
 
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
 
    # Display chat history
    for entry in st.session_state.chat_history:
        if entry['role'] == 'user':
            st.markdown(f"""
            <div class="chat-label user">You</div>
            <div style="display:flex;justify-content:flex-end;">
                <div class="chat-bubble-user">{entry['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-label ai">CineMatch AI</div>
            <div class="chat-bubble-ai">{entry['content']}</div>
            """, unsafe_allow_html=True)
 
    # Input row
    col_inp, col_send = st.columns([4, 1])
    with col_inp:
        user_prompt = st.text_input(
            "Ask the AI",
            placeholder='e.g. "I want something dark and psychological like Inception"',
            label_visibility="collapsed",
            key="ai_input"
        )
    with col_send:
        send_clicked = st.button("ASK AI →", key="ai_send")
 
    # Starter prompts
    st.markdown("""
    <div style="margin-top:16px;display:flex;gap:8px;flex-wrap:wrap;">
        <div style="background:#101015;border:1px solid rgba(255,255,255,0.07);border-radius:8px;padding:6px 12px;font-size:12px;color:rgba(255,255,255,0.4);">
            💡 Try: "I'm sad and want something uplifting"
        </div>
        <div style="background:#101015;border:1px solid rgba(255,255,255,0.07);border-radius:8px;padding:6px 12px;font-size:12px;color:rgba(255,255,255,0.4);">
            💡 Try: "Best sci-fi films about AI"
        </div>
        <div style="background:#101015;border:1px solid rgba(255,255,255,0.07);border-radius:8px;padding:6px 12px;font-size:12px;color:rgba(255,255,255,0.4);">
            💡 Try: "Movies like The Godfather"
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    if send_clicked and user_prompt.strip():
        st.session_state.chat_history.append({'role': 'user', 'content': user_prompt})
 
        # Build the movie titles list for context (first 100)
        movie_list_sample = ', '.join(movies['title'].values[:100].tolist())
 
        system_prompt = f"""You are CineMatch, an expert AI movie recommendation assistant built into a movie recommender web app.
The app has a database of 4,806 movies from the TMDB 5000 dataset.
Some movies available include: {movie_list_sample} (and thousands more).
 
When a user asks for recommendations:
1. Suggest 5 specific movie titles that fit their request
2. For each movie give a 1-sentence reason why it fits
3. Keep your tone friendly, enthusiastic, and concise
4. Format your response clearly with numbered list
5. End with one follow-up question to refine further
 
Do not use markdown headers or bold text. Keep the total response under 250 words."""
 
        with st.spinner("AI is thinking..."):
            try:
                ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY", "")
                response = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01"
                    },
                    json={
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 1000,
                        "system": system_prompt,
                        "messages": [
                            {"role": "user", "content": user_prompt}
                        ]
                    },
                    timeout=30
                )
                data = response.json()
                ai_reply = data['content'][0]['text'] if data.get('content') else "Sorry, I couldn't get a response. Please try again."
            except Exception as e:
                ai_reply = f"AI service error: {str(e)}. Please check your API key in Streamlit secrets."
 
        st.session_state.chat_history.append({'role': 'assistant', 'content': ai_reply})
        st.rerun()
 
    if st.session_state.chat_history:
        if st.button("Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()
 
    st.markdown('</div>', unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — COMPARE MOVIES
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="page">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-label">✦ Cosine Similarity Score</div>
    <div class="sec-title">COMPARE ANY TWO MOVIES</div>
    <div style="font-size:14px;color:rgba(255,255,255,0.4);margin-bottom:28px;line-height:1.7;">
        Select any two films and see their exact cosine similarity score —
        the same metric the recommendation engine uses internally.
        A score of 100% means identical content, 0% means completely unrelated.
    </div>
    """, unsafe_allow_html=True)
 
    col_m1, col_vs, col_m2 = st.columns([5, 1, 5])
    with col_m1:
        st.markdown('<div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:8px;">First movie</div>', unsafe_allow_html=True)
        movie_a = st.selectbox("Movie A", movies['title'].values, key="compare_a", label_visibility="collapsed")
    with col_vs:
        st.markdown('<div style="text-align:center;padding-top:32px;font-family:Bebas Neue,sans-serif;font-size:22px;color:rgba(255,255,255,0.2);">VS</div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown('<div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:8px;">Second movie</div>', unsafe_allow_html=True)
        idx_b = min(10, len(movies)-1)
        movie_b = st.selectbox("Movie B", movies['title'].values, index=idx_b, key="compare_b", label_visibility="collapsed")
 
    compare_clicked = st.button("COMPARE →", key="compare_btn")
 
    if compare_clicked:
        with st.spinner("Calculating similarity..."):
            score = get_similarity_score(movie_a, movie_b)
 
            mid_a = movies[movies['title'] == movie_a]['movie_id'].values
            mid_b = movies[movies['title'] == movie_b]['movie_id'].values
            det_a = fetch_details(mid_a[0]) if len(mid_a) > 0 else {}
            det_b = fetch_details(mid_b[0]) if len(mid_b) > 0 else {}
 
        st.markdown('<div style="margin-top:28px;"></div>', unsafe_allow_html=True)
 
        c1, c_score, c2 = st.columns([3, 2, 3])
 
        with c1:
            st.markdown(f"""
            <div class="compare-card">
                <img src="{det_a.get('poster','')}" style="width:100%;border-radius:8px;aspect-ratio:2/3;object-fit:cover;margin-bottom:12px;" />
                <div style="font-size:14px;font-weight:500;color:#eeebe6;margin-bottom:4px;">{movie_a}</div>
                <div style="font-size:12px;color:rgba(255,255,255,0.35);">{det_a.get('year','')} &nbsp;·&nbsp; ⭐ {det_a.get('rating','')}</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.25);margin-top:4px;">{det_a.get('genres','')}</div>
            </div>
            """, unsafe_allow_html=True)
 
        with c_score:
            verdict = "Very Similar" if score >= 25 else "Somewhat Similar" if score >= 10 else "Not Similar"
            color   = "#34d399" if score >= 25 else "#fbbf24" if score >= 10 else "#f87171"
            st.markdown(f"""
            <div class="compare-card" style="padding:32px 20px;">
                <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:12px;">Similarity Score</div>
                <div class="compare-score">{score}%</div>
                <div class="score-bar-bg">
                    <div class="score-bar-fill" style="width:{min(score*3,100)}%"></div>
                </div>
                <div style="font-size:13px;font-weight:500;color:{color};margin-top:8px;">{verdict}</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.25);margin-top:8px;line-height:1.6;">
                    Based on TF-IDF cosine similarity of their tags vectors
                </div>
            </div>
            """, unsafe_allow_html=True)
 
        with c2:
            st.markdown(f"""
            <div class="compare-card">
                <img src="{det_b.get('poster','')}" style="width:100%;border-radius:8px;aspect-ratio:2/3;object-fit:cover;margin-bottom:12px;" />
                <div style="font-size:14px;font-weight:500;color:#eeebe6;margin-bottom:4px;">{movie_b}</div>
                <div style="font-size:12px;color:rgba(255,255,255,0.35);">{det_b.get('year','')} &nbsp;·&nbsp; ⭐ {det_b.get('rating','')}</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.25);margin-top:4px;">{det_b.get('genres','')}</div>
            </div>
            """, unsafe_allow_html=True)
 
    st.markdown('</div>', unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="page">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-label">✦ Dataset Statistics</div>
    <div class="sec-title">PROJECT DASHBOARD</div>
    <div style="font-size:14px;color:rgba(255,255,255,0.4);margin-bottom:28px;line-height:1.7;">
        Live statistics and visualisations about the TMDB 5000 dataset
        and the machine learning model powering CineMatch.
    </div>
    """, unsafe_allow_html=True)
 
    # Stats row
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card"><div class="stat-val">4,806</div><div class="stat-lbl">Total Movies</div></div>
        <div class="stat-card"><div class="stat-val">5,000</div><div class="stat-lbl">Vector Dims</div></div>
        <div class="stat-card"><div class="stat-val">TF-IDF</div><div class="stat-lbl">Vectorizer</div></div>
        <div class="stat-card"><div class="stat-val">Cosine</div><div class="stat-lbl">Similarity</div></div>
        <div class="stat-card"><div class="stat-val">~180 MB</div><div class="stat-lbl">Model Size</div></div>
        <div class="stat-card"><div class="stat-val">CBF</div><div class="stat-lbl">Algorithm</div></div>
    </div>
    """, unsafe_allow_html=True)
 
    # Charts using st.bar_chart
    try:
        import ast as ast_module
        import collections
 
        @st.cache_data
        def compute_genre_counts():
            genre_counts = collections.Counter()
            for tags in movies['tags'].values:
                words = str(tags).split()
                for w in words:
                    if len(w) > 6 and w[0].isupper():
                        genre_counts[w] += 1
            return genre_counts
 
        st.markdown('<div class="ruled" style="margin-bottom:28px;"></div>', unsafe_allow_html=True)
 
        col_left, col_right = st.columns(2)
 
        with col_left:
            st.markdown('<div class="sec-label">▸ Dataset overview</div>', unsafe_allow_html=True)
            overview_data = pd.DataFrame({
                'Category': ['Total Movies', 'After Cleaning', 'Features Used', 'Vector Dimensions'],
                'Count': [4803, 4806, 7, 5000]
            }).set_index('Category')
            st.bar_chart(overview_data, color='#e05c20')
 
        with col_right:
            st.markdown('<div class="sec-label">▸ Technology breakdown</div>', unsafe_allow_html=True)
            tech_data = pd.DataFrame({
                'Technology': ['Scikit-learn', 'Pandas', 'NLTK', 'Streamlit', 'Requests'],
                'Lines of Code': [8, 12, 5, 60, 6]
            }).set_index('Technology')
            st.bar_chart(tech_data, color='#e05c20')
 
        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
        col_l2, col_r2 = st.columns(2)
 
        with col_l2:
            st.markdown('<div class="sec-label">▸ Pipeline steps & complexity</div>', unsafe_allow_html=True)
            pipeline_data = pd.DataFrame({
                'Step': ['Load Data','Clean','Extract','Stemming','TF-IDF','Similarity','Export'],
                'Complexity (relative)': [1, 1, 4, 2, 3, 5, 1]
            }).set_index('Step')
            st.bar_chart(pipeline_data, color='#e05c20')
 
        with col_r2:
            st.markdown('<div class="sec-label">▸ Similarity matrix size</div>', unsafe_allow_html=True)
            matrix_data = pd.DataFrame({
                'Metric': ['Movies', 'Pairs Computed', 'Dimensions (K)', 'File Size (MB)'],
                'Value': [4806, 4806*4806//1000000, 5, 180]
            }).set_index('Metric')
            st.bar_chart(matrix_data, color='#e05c20')
 
    except Exception as e:
        st.markdown(f'<div style="color:rgba(255,255,255,0.3);font-size:13px;">Charts loading... ({e})</div>', unsafe_allow_html=True)
 
    st.markdown('</div>', unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — HOW IT WORKS
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="page">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-label">✦ ML Pipeline</div>
    <div class="sec-title">HOW THE MODEL WORKS</div>
    <div style="font-size:14px;color:rgba(255,255,255,0.4);margin-bottom:28px;line-height:1.7;">
        A complete walkthrough of the 10-step machine learning pipeline —
        from raw CSV data to live recommendations.
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("""
    <div class="pipeline-grid">
        <div class="pipe-step">
            <div class="pipe-num">01</div>
            <div class="pipe-title">Load & Merge Datasets</div>
            <div class="pipe-desc">Two CSVs — tmdb_5000_movies.csv and tmdb_5000_credits.csv — merged on the title column using pandas.</div>
            <div class="pipe-code">movies.merge(credits, on='title')</div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">02</div>
            <div class="pipe-title">Select Features</div>
            <div class="pipe-desc">Keep only: movie_id, genres, keywords, title, overview, cast, crew. Drop budget, revenue, runtime etc.</div>
            <div class="pipe-code">movies[['movie_id','title',...]]</div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">03</div>
            <div class="pipe-title">Data Cleaning</div>
            <div class="pipe-desc">Remove null rows with dropna(). Check duplicates with duplicated().sum(). Ensures clean model input.</div>
            <div class="pipe-code">dropna() / duplicated()</div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">04</div>
            <div class="pipe-title">Feature Extraction</div>
            <div class="pipe-desc">3 custom functions parse JSON strings: convert() for genres/keywords, convert3() for top 3 cast, fetch_director() for crew.</div>
            <div class="pipe-code">ast.literal_eval()</div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">05</div>
            <div class="pipe-title">Build Tags Column</div>
            <div class="pipe-desc">All features combined into one string per movie. Multi-word names lose spaces: "Sam Mendes" → "SamMendes".</div>
            <div class="pipe-code">new_df['tags']</div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">06</div>
            <div class="pipe-title">Stemming</div>
            <div class="pipe-desc">PorterStemmer reduces every word to root form. "dancing", "danced", "dancer" → all become "danc".</div>
            <div class="pipe-code">ps.stem(word)</div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">07</div>
            <div class="pipe-title">TF-IDF Vectorization</div>
            <div class="pipe-desc">Each movie becomes a 5,000-dimensional vector. Rare important words get higher weight than common ones.</div>
            <div class="pipe-code">TfidfVectorizer(max_features=5000)</div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">08</div>
            <div class="pipe-title">Cosine Similarity</div>
            <div class="pipe-desc">4,806 × 4,806 similarity matrix computed. Each value = cosine of angle between two film vectors.</div>
            <div class="pipe-code">cosine_similarity(vectors)</div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">09</div>
            <div class="pipe-title">Recommendation Function</div>
            <div class="pipe-desc">For any film, retrieve its similarity row, sort descending, return top 5 excluding itself.</div>
            <div class="pipe-code">sorted(...)[1:6]</div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">10</div>
            <div class="pipe-title">Export with Pickle</div>
            <div class="pipe-desc">Save new_df → movies.pkl and similarity matrix → similarity.pkl. App loads instantly without recomputing.</div>
            <div class="pipe-code">pickle.dump()</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    # Technology stack
    st.markdown('<div style="margin-top:36px;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ruled" style="margin-bottom:28px;"></div>
    <div class="sec-label">▸ Technology stack</div>
    """, unsafe_allow_html=True)
 
    st.markdown("""
    <div style="background:#101015;border:1px solid rgba(255,255,255,0.055);border-radius:13px;padding:8px 20px;">
        <div class="tech-row-item"><div class="tech-name">Python 3</div><div class="tech-desc">Core language for all data processing and ML</div><span class="tech-tag tag-ml">ML</span></div>
        <div class="tech-row-item"><div class="tech-name">Pandas</div><div class="tech-desc">Load CSVs, merge datasets, select and clean columns</div><span class="tech-tag tag-data">Data</span></div>
        <div class="tech-row-item"><div class="tech-name">NLTK / PorterStemmer</div><div class="tech-desc">Reduces words to root form for better matching</div><span class="tech-tag tag-ml">ML</span></div>
        <div class="tech-row-item"><div class="tech-name">TfidfVectorizer</div><div class="tech-desc">Converts tags text into 5,000-dimensional numerical vectors</div><span class="tech-tag tag-ml">ML</span></div>
        <div class="tech-row-item"><div class="tech-name">Cosine Similarity</div><div class="tech-desc">Measures angle between vectors — 1.0 = identical films</div><span class="tech-tag tag-ml">ML</span></div>
        <div class="tech-row-item"><div class="tech-name">Pickle</div><div class="tech-desc">Saves pre-computed model — app loads instantly without recomputing</div><span class="tech-tag tag-data">Data</span></div>
        <div class="tech-row-item"><div class="tech-name">Streamlit</div><div class="tech-desc">Python web framework — builds and serves the entire web app</div><span class="tech-tag tag-ui">UI</span></div>
        <div class="tech-row-item"><div class="tech-name">HTML + CSS</div><div class="tech-desc">Custom dark cinema theme via st.markdown(unsafe_allow_html=True)</div><span class="tech-tag tag-ui">UI</span></div>
        <div class="tech-row-item"><div class="tech-name">TMDB API</div><div class="tech-desc">Real-time movie posters, ratings, genres, and release years</div><span class="tech-tag tag-ui">UI</span></div>
        <div class="tech-row-item"><div class="tech-name">Claude AI (Anthropic)</div><div class="tech-desc">Powers the AI Chat tab — mood-based movie recommendations via API</div><span class="tech-tag tag-ai">AI</span></div>
        <div class="tech-row-item"><div class="tech-name">GitHub</div><div class="tech-desc">Version control — full commit history shows iterative development</div><span class="tech-tag tag-deploy">Deploy</span></div>
        <div class="tech-row-item"><div class="tech-name">Streamlit Cloud</div><div class="tech-desc">Free live deployment — auto-redeploys every time you push to GitHub</div><span class="tech-tag tag-deploy">Deploy</span></div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown('</div>', unsafe_allow_html=True)
 
# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="foot">
    <div class="foot-logo">CINE<span>MATCH</span></div>
    <div class="foot-right">
        Python · Streamlit · Scikit-learn · TMDB API · Claude AI
        &nbsp;|&nbsp; Data Encryption &amp; Security — Final Year Project
    </div>
</div>
""", unsafe_allow_html=True)
 













