# 🎬 CineMatch — AI Movie Recommender System

> An AI-powered movie recommendation web application built with Python, Streamlit, and Machine Learning. Deployed live on Streamlit Cloud.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://movie-recommender-kdqsoxqmw6nyjjpzfna3zd.streamlit.app/)

---

## 🖥️ Live Demo

🔗 **[movie-recommender-kdqsoxqmw6nyjjpzfna3zd.streamlit.app](https://movie-recommender-kdqsoxqmw6nyjjpzfna3zd.streamlit.app/)**

---

## 📌 About The Project

CineMatch is a content-based movie recommendation system trained on the TMDB 5000 Movie Dataset. It extracts metadata from over 4,800 films — including genres, cast, crew, and keywords — converts them into TF-IDF vectors, and uses cosine similarity to find the most similar films for any selected title.

The app is built as a single-page multi-tab web application using Streamlit with a custom dark cinema-themed UI built using HTML and CSS.

---

## ✨ Features

| Tab | Description |
|---|---|
| 🎬 **Recommend** | Select any movie and get 5 similar film recommendations with posters, ratings, and genres |
| ⚖️ **Compare Movies** | Pick two films and see their exact cosine similarity score with a visual progress bar |
| 📊 **Dashboard** | Live charts showing dataset statistics, pipeline complexity, and technology breakdown |
| 🧠 **How It Works** | Full 10-step ML pipeline walkthrough with code snippets and technology stack |

---

## 🧠 How It Works

```
Raw CSV Data
    ↓
Merge & Clean (Pandas)
    ↓
Feature Extraction (genres, cast, crew, keywords)
    ↓
Build Tags Column
    ↓
Text Preprocessing (Porter Stemmer)
    ↓
TF-IDF Vectorization (5,000 dimensions)
    ↓
Cosine Similarity Matrix (4806 × 4806)
    ↓
Export with Pickle
    ↓
Streamlit Web App → Live Recommendations
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| Pandas | Data loading, merging, and cleaning |
| NLTK / PorterStemmer | Text preprocessing — stemming words to root form |
| Scikit-learn (TF-IDF) | Convert movie tags into 5,000-dimensional vectors |
| Scikit-learn (Cosine Similarity) | Measure similarity between film vectors |
| Pickle | Save and load pre-computed model files |
| Streamlit | Web application framework |
| HTML + CSS | Custom dark cinema UI via st.markdown() |
| TMDB API | Real-time movie posters, ratings, and genres |
| GitHub | Version control |
| Streamlit Cloud | Live deployment |

---

## 📂 Project Structure

```
cinematch/
│
├── app.py                          # Main Streamlit web application
├── movie-recommender-system.ipynb  # Jupyter notebook — full ML pipeline
├── movies.pkl                      # Processed movie dataframe (serialised)
├── similarity.pkl                  # Pre-computed cosine similarity matrix (~180 MB)
├── tmdb_5000_movies.csv            # Raw movie metadata dataset
├── tmdb_5000_credits.csv           # Raw cast and crew dataset
├── requirements.txt                # Python dependencies
├── .streamlit/                     # Streamlit configuration
└── README.md                       # Project documentation
```

---

## 🚀 Run Locally

### Prerequisites
- Python 3.8+
- pip

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/fatima-athar08/movie-recommender.git
cd movie-recommender
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

**4. Open in browser**
```
http://localhost:8501
```

> **Note:** Make sure `movies.pkl` and `similarity.pkl` are in the same folder as `app.py`. If missing, run all cells in the Jupyter notebook first to generate them.

---

## 📓 Rebuild the Model

To retrain the model from scratch, open and run all cells in:
```
movie-recommender-system.ipynb
```

This will:
1. Load and merge the two CSV datasets
2. Extract and clean features
3. Apply stemming
4. Compute TF-IDF vectors
5. Calculate the cosine similarity matrix
6. Save `movies.pkl` and `similarity.pkl`

---

## 📊 Dataset

**Source:** [TMDB 5000 Movie Dataset — Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

| File | Contents |
|---|---|
| `tmdb_5000_movies.csv` | Movie ID, title, genres, keywords, overview |
| `tmdb_5000_credits.csv` | Full cast and crew per movie |

| Statistic | Value |
|---|---|
| Total movies | 4,806 |
| Features used | genres, keywords, cast (top 3), director, overview |
| Vector dimensions | 5,000 |
| Similarity matrix size | 4,806 × 4,806 |
| Model file size | ~180 MB |

---

## 🔑 Algorithm

**Content-Based Filtering** — recommends films based on their own metadata rather than user behaviour.

1. **TF-IDF** — assigns higher weight to words that are important in one specific film but rare across all films
2. **Cosine Similarity** — measures the angular distance between two vectors. Score of 1.0 = identical films, 0 = completely unrelated

---

## 👩‍💻 Author

**Fatima Athar**
B.S. Information Technology — University of Agriculture Faisalabad
GitHub: [@fatima-athar08](https://github.com/fatima-athar08)

---
