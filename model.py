import streamlit as st
import pickle
import joblib
import difflib
import numpy as np

# Load files (use relative paths)
movies = pickle.load(open("movies.pkl", "rb"))  # list of movie titles
similarity = joblib.load("similarity_sparse.pkl")  # sparse similarity matrix

# Recommendation function
def recommend(movie_name):
    movie_name = movie_name.lower().strip()
    titles = [title[0].lower().strip() for title in movies]

    # Fuzzy match the movie name
    close_matches = difflib.get_close_matches(movie_name, titles, n=1, cutoff=0.6)
    if not close_matches:
        return None, None

    matched_title = close_matches[0]
    index = titles.index(matched_title)

    # Handle sparse matrix properly
    row = similarity.getrow(index).toarray().flatten()
    distances = list(enumerate(row))
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    recommended = [movies[i[0]][0] for i in sorted_movies if i[1] > 0]
    return recommended, matched_title

# Streamlit UI
def main():
    st.set_page_config(page_title="Movie Recommender", layout="centered")

    # CSS Styling
    st.markdown("""
        <style>
        .title {
            color: #1e272e;
            font-size: 36px;
            text-align: center;
            margin-bottom: 25px;
        }
        .recommendation {
            background-color: #dff9fb;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 10px;
            font-size: 18px;
            color: #130f40;
        }
        </style>
    """, unsafe_allow_html=True)

    # App title and input
    st.markdown('<div class="title">Movie Recommender System</div>', unsafe_allow_html=True)
    st.write("Type in the name of a movie to get recommendations for similar ones.")

    user_input = st.text_input("Enter Movie Name:")

    if st.button("Recommend"):
        if not user_input.strip():
            st.warning("Please enter a movie name.")
        else:
            recommended_movies, matched_title = recommend(user_input)

            if recommended_movies is None or not recommended_movies:
                st.error("No recommendations found. Try another movie.")
            else:
                st.success(f"Showing recommendations for: {matched_title.title()}")
                st.subheader("Top 5 Recommendations:")
                for movie in recommended_movies:
                    st.markdown(f'<div class="recommendation">{movie}</div>', unsafe_allow_html=True)

    st.markdown("<br><div style='text-align:center; color:gray;'>Made with love using Streamlit</div>", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
