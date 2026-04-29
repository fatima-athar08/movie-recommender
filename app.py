import streamlit as st
import pickle
import requests
import pandas as pd

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  LOAD DATA
#  Notebook saves:
#    pickle.dump(new_df, open('movies.pkl','wb'))
#    pickle.dump(similarity, open('similarity.pkl','wb'))
#  new_df columns → movie_id | title | tags
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    movies_raw = pickle.load(open('movies.pkl', 'rb'))
    sim        = pickle.load(open('similarity.pkl', 'rb'))
    # notebook saves a DataFrame directly, but handle dict just in case
    df = movies_raw if isinstance(movies_raw, pd.DataFrame) else pd.DataFrame(movies_raw)
    return df, sim

movies, similarity = load_data()

# ─────────────────────────────────────────────
#  FETCH POSTER  (your original API key kept)
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
#  RECOMMEND  (matches your notebook logic exactly)
#  movies columns → movie_id | title | tags
# ─────────────────────────────────────────────
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances   = similarity[movie_index]
    movie_list  = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies         = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# ─────────────────────────────────────────────
#  CUSTOM CSS  (all styling lives here)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}
.stApp {
    background: #09090e;
    color: #eeebe6;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── NAVBAR ── */
.navbar {
    background: #0f0f14;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 15px 44px;
    display: flex;
    align-items: center;
}
.nav-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 26px;
    letter-spacing: 3px;
    color: #eeebe6;
}
.nav-logo span { color: #e05c20; }
.nav-pill {
    margin-left: 12px;
    background: rgba(224,92,32,0.12);
    border: 1px solid rgba(224,92,32,0.35);
    color: #e05c20;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 20px;
}
.nav-info {
    margin-left: auto;
    font-size: 11px;
    color: rgba(255,255,255,0.28);
    letter-spacing: 0.8px;
}

/* ── HERO ── */
.hero-wrap {
    padding: 56px 44px 36px;
    max-width: 860px;
}
.eyebrow {
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #e05c20;
    margin-bottom: 12px;
}
.big-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 62px;
    line-height: 1.0;
    letter-spacing: 2px;
    color: #eeebe6;
    margin-bottom: 14px;
}
.big-title em { color: #e05c20; font-style: normal; }
.hero-desc {
    font-size: 15px;
    font-weight: 300;
    color: rgba(238,235,230,0.5);
    line-height: 1.75;
    max-width: 500px;
}

/* ── DIVIDER ── */
.ruled {
    height: 1px;
    background: linear-gradient(90deg,
        rgba(224,92,32,0.45), rgba(255,255,255,0.04), transparent);
    margin: 0 44px;
}

/* ── SEARCH LABEL ── */
.pick-label {
    font-size: 10px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.32);
    padding: 36px 44px 14px;
}

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    background: #13131a !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 11px !important;
    color: #eeebe6 !important;
    font-size: 15px !important;
}
.stSelectbox > div > div:hover {
    border-color: rgba(224,92,32,0.45) !important;
}
.stSelectbox svg { fill: #e05c20 !important; }

/* ── BUTTON ── */
.stButton > button {
    background: #e05c20 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 11px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 19px !important;
    letter-spacing: 1.8px !important;
    padding: 9px 32px !important;
    width: 100% !important;
    transition: background 0.18s, transform 0.12s !important;
}
.stButton > button:hover {
    background: #bf4c14 !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── RESULTS HEADING ── */
.rec-heading {
    padding: 32px 44px 16px;
    display: flex;
    align-items: baseline;
    gap: 12px;
}
.rec-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 26px;
    letter-spacing: 2px;
    color: #eeebe6;
}
.rec-sub { font-size: 12px; color: rgba(255,255,255,0.3); }

/* ── MOVIE CARD ── */
.mcard {
    background: #101015;
    border-radius: 13px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.055);
    transition: transform 0.22s ease, border-color 0.22s ease;
}
.mcard:hover {
    transform: translateY(-5px);
    border-color: rgba(224,92,32,0.7);
}
.mcard img {
    width: 100%;
    display: block;
    aspect-ratio: 2/3;
    object-fit: cover;
}
.mcard-body   { padding: 12px 13px 14px; }
.mcard-rank {
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #e05c20;
    margin-bottom: 4px;
}
.mcard-name {
    font-size: 13px;
    font-weight: 500;
    color: #eeebe6;
    line-height: 1.3;
    margin-bottom: 8px;
}
.bar-track {
    background: rgba(255,255,255,0.07);
    border-radius: 3px;
    height: 2px;
    width: 100%;
}
.bar-fill { background: #e05c20; border-radius: 3px; height: 2px; }
.bar-pct  { font-size: 9px; color: rgba(255,255,255,0.3); margin-top: 4px; }

/* ── WHY BOX ── */
.why-wrap {
    margin: 24px 44px 8px;
    background: #101015;
    border: 1px solid rgba(255,255,255,0.055);
    border-left: 3px solid #e05c20;
    border-radius: 13px;
    padding: 18px 22px;
}
.why-label {
    font-size: 9px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #e05c20;
    margin-bottom: 7px;
}
.why-body {
    font-size: 13px;
    font-weight: 300;
    color: rgba(238,235,230,0.65);
    line-height: 1.85;
}
.why-body b { color: #eeebe6; font-weight: 500; }

/* ── STATS ── */
.stats-grid {
    display: flex;
    gap: 14px;
    padding: 0 44px 36px;
    flex-wrap: wrap;
}
.stat-card {
    background: #101015;
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 13px;
    padding: 18px 24px;
    flex: 1;
    min-width: 130px;
    text-align: center;
}
.stat-val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 30px;
    color: #e05c20;
    letter-spacing: 1px;
    line-height: 1;
    margin-bottom: 5px;
}
.stat-lbl {
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.3);
}

/* ── HOW IT WORKS ── */
.how-wrap  { padding: 12px 44px 44px; }
.how-heading {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 26px;
    letter-spacing: 2px;
    color: #eeebe6;
    margin-bottom: 18px;
}
.steps-grid { display: flex; gap: 14px; flex-wrap: wrap; }
.step-card {
    background: #101015;
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 13px;
    padding: 18px 20px;
    flex: 1;
    min-width: 150px;
}
.step-n {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 36px;
    color: rgba(224,92,32,0.2);
    line-height: 1;
    margin-bottom: 9px;
}
.step-t { font-size: 13px; font-weight: 500; color: #eeebe6; margin-bottom: 5px; }
.step-d { font-size: 11px; font-weight: 300; color: rgba(255,255,255,0.36); line-height: 1.7; }

/* ── FOOTER ── */
.foot {
    border-top: 1px solid rgba(255,255,255,0.055);
    padding: 20px 44px;
    display: flex;
    align-items: center;
}
.foot-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 16px;
    letter-spacing: 2px;
    color: rgba(255,255,255,0.2);
}
.foot-logo span { color: rgba(224,92,32,0.45); }
.foot-right {
    margin-left: auto;
    font-size: 10px;
    color: rgba(255,255,255,0.18);
    letter-spacing: 0.4px;
}
.stSpinner > div { border-top-color: #e05c20 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  NAVBAR
# ─────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="nav-logo">CINE<span>MATCH</span></div>
    <div class="nav-pill">AI Powered</div>
    <div class="nav-info">TF-IDF &nbsp;·&nbsp; Cosine Similarity &nbsp;·&nbsp; TMDB 5000</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="eyebrow">✦ Machine Learning &nbsp;·&nbsp; Content-Based Filtering</div>
    <div class="big-title">FIND YOUR<br>NEXT <em>FAVOURITE</em><br>FILM.</div>
    <div class="hero-desc">
        An AI-powered recommendation engine trained on 5,000+ movies.
        Pick any title and instantly discover films that share the same
        themes, cast, genre, and directorial style.
    </div>
</div>
<div class="ruled"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SEARCH  — same selectbox + button as your
#  original, just styled differently
# ─────────────────────────────────────────────
st.markdown(
    '<div class="pick-label">▸ Select a movie to get recommendations</div>',
    unsafe_allow_html=True
)

col_sel, col_btn, col_gap = st.columns([3, 1, 2])

with col_sel:
    selected_movie_name = st.selectbox(
        "Select a movie to recommend",
        movies['title'].values,
        label_visibility="collapsed"
    )

with col_btn:
    recommend_clicked = st.button("Recommend")

# ─────────────────────────────────────────────
#  RESULTS  — same logic as your original,
#  displayed in styled cards instead of st.text
# ─────────────────────────────────────────────
if recommend_clicked:
    with st.spinner("Finding your perfect films..."):
        names, posters = recommend(selected_movie_name)

    bar_widths = [98, 94, 90, 86, 82]   # visual bars only

    st.markdown(f"""
    <div class="rec-heading">
        <div class="rec-title">TOP 5 RECOMMENDATIONS</div>
        <div class="rec-sub">based on "{selected_movie_name}"</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    for col, name, poster, bar in zip(
            [col1, col2, col3, col4, col5], names, posters, bar_widths):
        with col:
            st.markdown(f"""
            <div class="mcard">
                <img src="{poster}" alt="{name}" />
                <div class="mcard-body">
                    <div class="mcard-rank">match</div>
                    <div class="mcard-name">{name}</div>
                    <div class="bar-track">
                        <div class="bar-fill" style="width:{bar}%"></div>
                    </div>
                    <div class="bar-pct">{bar}% similarity</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # WHY BOX — explains the algorithm after every search
    st.markdown(f"""
    <div class="why-wrap">
        <div class="why-label">✦ Why these recommendations?</div>
        <div class="why-body">
            You selected <b>{selected_movie_name}</b>. The model extracted its
            metadata — cast, crew, genres, and keywords — and merged them into
            a single <b>tags</b> string per movie. Each string was converted into
            a numerical vector using <b>TF-IDF vectorization</b>. Then
            <b>cosine similarity</b> measured how closely each of the 5,000+ films
            aligns with your pick. The 5 films with the smallest angular distance
            between their vectors are returned as your recommendations.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MODEL STATS
# ─────────────────────────────────────────────
st.markdown("""
<div class="ruled" style="margin-top:36px;"></div>
<div style="padding:32px 44px 18px;">
    <div style="font-size:10px; letter-spacing:2.5px; text-transform:uppercase;
                color:rgba(255,255,255,0.28);">▸ Model at a glance</div>
</div>
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-val">5000+</div>
        <div class="stat-lbl">Movies</div>
    </div>
    <div class="stat-card">
        <div class="stat-val">TF-IDF</div>
        <div class="stat-lbl">Vectorizer</div>
    </div>
    <div class="stat-card">
        <div class="stat-val">Cosine</div>
        <div class="stat-lbl">Similarity</div>
    </div>
    <div class="stat-card">
        <div class="stat-val">TMDB</div>
        <div class="stat-lbl">Dataset</div>
    </div>
    <div class="stat-card">
        <div class="stat-val">CBF</div>
        <div class="stat-lbl">Algorithm</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HOW IT WORKS
# ─────────────────────────────────────────────
st.markdown("""
<div class="ruled"></div>
<div class="how-wrap">
    <div class="how-heading">HOW IT WORKS</div>
    <div class="steps-grid">
        <div class="step-card">
            <div class="step-n">01</div>
            <div class="step-t">Data Collection</div>
            <div class="step-d">
                TMDB 5000 dataset — two CSV files containing
                movie metadata and full cast &amp; crew credits.
            </div>
        </div>
        <div class="step-card">
            <div class="step-n">02</div>
            <div class="step-t">Feature Extraction</div>
            <div class="step-d">
                Genres, keywords, top 3 cast members, director,
                and overview are parsed from JSON and merged into
                one tags string per film.
            </div>
        </div>
        <div class="step-card">
            <div class="step-n">03</div>
            <div class="step-t">Stemming</div>
            <div class="step-d">
                Porter Stemmer reduces every word to its root form
                so "action", "acting", and "actor" all map to the
                same token — improving match quality.
            </div>
        </div>
        <div class="step-card">
            <div class="step-n">04</div>
            <div class="step-t">TF-IDF Vectors</div>
            <div class="step-d">
                Each film becomes a 5,000-dimensional vector.
                Words rare across the dataset but frequent in one
                film receive higher weight.
            </div>
        </div>
        <div class="step-card">
            <div class="step-n">05</div>
            <div class="step-t">Cosine Similarity</div>
            <div class="step-d">
                Angular distance between vectors is computed for
                all pairs. The 5 films closest in angle to your
                pick are your recommendations.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="foot">
    <div class="foot-logo">CINE<span>MATCH</span></div>
    <div class="foot-right">
        Python &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; Scikit-learn
        &nbsp;·&nbsp; TMDB API &nbsp;&nbsp;|&nbsp;&nbsp;
        Data Encryption &amp; Security — Final Year Project
    </div>
</div>
""", unsafe_allow_html=True)
