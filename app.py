import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Job Recommender", layout="wide")
st.title("💼 Job Recommendation System")

st.markdown("Enter your skills or desired job title to get personalized job recommendations.")

# ✅ STEP 1: TEST LOADING FILES
st.write("Trying to load files...")

try:
    with open("tfidf_vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    with open("tfidf_matrix.pkl", "rb") as f:
        tfidf_matrix = pickle.load(f)
    job_df = pd.read_pickle("job_data.pkl")
    st.success("✅ Files loaded successfully!")
except Exception as e:
    st.error(f"❌ Failed to load files: {e}")
    st.stop()

# ✅ STEP 2: GET USER INPUT
query = st.text_input("🔍 Your Job Search Query (e.g. 'data analyst python')")

# ✅ STEP 3: MAKE RECOMMENDATIONS
if query:
    try:
        user_vec = vectorizer.transform([query.lower()])
        scores = cosine_similarity(user_vec, tfidf_matrix).flatten()
        top_indices = scores.argsort()[-5:][::-1]
        results = job_df.iloc[top_indices]

        st.subheader("📌 Recommended Jobs:")
        for _, row in results.iterrows():
            st.markdown(f"""
            *🧑‍💼 Title:* {row['title']}  
            *🌍 Country:* {row['country']}  
            *💼 Job Type:* {row['job_type']}  
            *💰 Hourly Rate:* ${row['total_avg_hourly']:.2f}  
            [🔗 View Job Posting]({row['link']})  
            ---
            """)
    except Exception as e:
        st.error(f"❌ Recommendation failed: {e}")
