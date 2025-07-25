import streamlit as st
import pickle
import difflib

# Load files
movies = pickle.load(open("C:/Users/HP/Downloads/movies.pkl", "rb"))         # numpy array of movie titles
similarity = pickle.load(open("C:/Users/HP/Downloads/similarity.sav", "rb")) # precomputed similarity matrix

# Recommendation logic
def recommend(movie_name):
    movie_name = movie_name.lower().strip()

    # Extract titles from NumPy array
    titles = [title[0].lower().strip() for title in movies]

    # Fuzzy match user input
    close_matches = difflib.get_close_matches(movie_name, titles, n=1, cutoff=0.6)

    if not close_matches:
        return None, None

    matched_title = close_matches[0]
    index = titles.index(matched_title)

    # Get similarity scores and top 5 matches (excluding self)
    distances = list(enumerate(similarity[index]))
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    recommended = [movies[i[0]][0] for i in sorted_movies]

    return recommended, matched_title

# UI
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

    # App Title
    st.markdown('<div class="title">Movie Recommender System</div>', unsafe_allow_html=True)
    st.write("Type in the name of a movie to get recommendations for similar ones.")

    # Input field
    user_input = st.text_input("Enter Movie Name:")

    # Recommend button
    if st.button("Recommend"):
        if not user_input.strip():
            st.warning("Please enter a movie name.")
        else:
            recommended_movies, matched_title = recommend(user_input)
            if recommended_movies is None:
                st.error("No close match found. Please try another movie.")
            else:
                st.success(f"Showing recommendations for: {matched_title.title()}")
                st.subheader("Top 5 Recommendations:")
                for movie in recommended_movies:
                    st.markdown(f'<div class="recommendation">{movie}</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("<br><div style='text-align:center; color:gray;'>Made with love using Streamlit</div>", unsafe_allow_html=True)

# Entry point
if __name__ == "__main__":
    main()
