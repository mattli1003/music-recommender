# music-recommender

Welcome to the Music Recommender System! This project allows users to discover new music based on their favorite songs, artists, and moods. Built using Streamlit and the Spotify API, this app provides personalized music recommendations to enhance your listening experience.

**Features:**

1. More Songs Like This: Find songs similar to the one you love
2. Songs With Similar BPM: Discover tracks with a similar tempo
3. Top Tracks From This Artist: Get the top hits from your favorite artist

**To run this project, you need to have the following installed:**

1. Python
2. Spotipy (pip install spotipy)
3. Streamlit (pip install streamlit)

**Run the streamlit app:**

streamlit run MusicRecommender.py

**Interact with the app:**

1. Song and Artist Input: Type the name of a song and its artist in the format Song by Artist
2. Choose a Category: Select one of the available categories (More Songs Like This, Songs With Similar BPM, Top Tracks From This Artist)
3. Number of Recommendations: For categories that require a number of recommendations, specify the desired number (e.g., 10)
4. Show Recommendations: Click the "Show Recommendations" button to get your personalized music recommendations

**Code Functions**

1. get_song_album_cover_url(track): Returns the album cover URL for a given track.
2. get_recommendations(track_id=None, artist_id=None, target_bpm=None, outputs=None): Fetches song recommendations based on the provided parameters.
3. get_artist_top_tracks(artist_id, limit=20): Retrieves the top tracks for a given artist.

**Acknowledgments**

Special thanks to Spotipy for providing the Python interface to the Spotify API.
Thanks to the Streamlit team for creating an easy-to-use framework for building web apps.
