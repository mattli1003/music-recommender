import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# client id and secret from creating personal spotify web api app
CLIENT_ID = "70696b3eac40462aaab33de92be1c606"
CLIENT_SECRET = "4195eaf9ff6c407bba13fcb5e7d638f5"

st.set_page_config(layout="wide")

st.header('Music Recommender System')
st.text('Created by Matt Li')

col1, col2, col3 = st.columns([3, 1, 1])
with col1: 
    st.markdown("""
            ### Welcome to the Music Recommender System!

            Discover new music based on your favorite songs and artists. 
            Simply input the name of a song and its artist, choose a category, 
            and get personalized recommendations.

            #### Features:
            - **More Songs Like This:** Find songs similar to the one you love.
            - **Songs With Similar BPM:** Discover tracks with a similar tempo.
            - **Top 10 Tracks From This Artist:** Get the top hits from your favorite artist.

            Enjoy exploring new music tailored to your tastes!
            """)
    
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    search_query = st.text_input("Name of a song and artist (Format: Song by Artist)")
    category = st.selectbox('Choose a category', ['Choose a Category', 'More Songs Like This', 'Songs With Similar BPM', 'Top 10 Tracks From This Artist'])

outputs = None
if category == 'More Songs Like This' or category == 'Songs With Similar BPM':
    with col1:
        outputs = st.text_input("Number of recommendations")

# initializing the spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(track):
    if track and track["album"]["images"]:
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"
  
def get_recommendations(track_id=None, artist_id=None, target_bpm=None, outputs=None):
    seed_tracks = [track_id] if track_id else None
    seed_artists = [artist_id] if artist_id else None

    recommendations_params = {
        'seed_tracks': seed_tracks,
        'seed_artists': seed_artists,
        'limit': min(outputs, 100)
    }

    if target_bpm:
        recommendations_params['target_tempo'] = target_bpm

    recommended_tracks = []
    retrieved = 0

    while retrieved < outputs:
        results = sp.recommendations(**recommendations_params)
        tracks = results['tracks']
        recommended_tracks.extend(tracks)
        retrieved += len(tracks)
        if len(tracks) < 100:
            break  # if fewer than 100 tracks are returned, we're done
        recommendations_params['limit'] = min(outputs - retrieved, 100)

    recommended_music_names = []
    recommended_artist_names = []
    recommended_music_posters = []
    recommended_music_previews = []

    for track in recommended_tracks[:outputs]:  # ensure we don't exceed the requested number
        artist_name = ", ".join([artist["name"] for artist in track["artists"]])
        song_name = track["name"]
        album_cover_url = get_song_album_cover_url(track)
        preview_url = track["preview_url"]

        recommended_music_names.append(song_name)
        recommended_artist_names.append(artist_name)
        recommended_music_posters.append(album_cover_url)
        recommended_music_previews.append(preview_url)

    return recommended_music_names, recommended_artist_names, recommended_music_posters, recommended_music_previews

def get_artist_top_tracks(artist_id):
    results = sp.artist_top_tracks(artist_id)
    top_tracks = results['tracks'][:10]
    
    top_track_names = []
    top_artist_names = []
    top_track_posters = []
    top_track_previews = []

    for track in top_tracks:
        artist_name = ", ".join([artist["name"] for artist in track["artists"]])
        song_name = track["name"]
        album_cover_url = get_song_album_cover_url(track)
        preview_url = track["preview_url"]
        
        top_track_names.append(song_name)
        top_artist_names.append(artist_name)
        top_track_posters.append(album_cover_url)
        top_track_previews.append(preview_url)
    
    return top_track_names, top_artist_names, top_track_posters, top_track_previews

if st.button('Show Recommendation'):
    if category == 'Choose a Category':
         st.write("Please select a category")
    elif (category == 'More Songs Like This' or category == 'Songs With Similar BPM') and not outputs.isdigit():
        st.write("Please input a valid integer for the number of recommendations")
    elif " by " in search_query:
        song, artist = search_query.split(" by ", 1)
        results = sp.search(q=f"track:{song} artist:{artist}", type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_id = track['id']
            
            if category == 'More Songs Like This':
                recommended_music_names, recommended_artist_names, recommended_music_posters, recommended_music_previews = get_recommendations(track_id=track_id, outputs=int(outputs))
            elif category == 'Top 10 Tracks From This Artist':
                artist_id = track['artists'][0]['id']
                recommended_music_names, recommended_artist_names, recommended_music_posters, recommended_music_previews = get_artist_top_tracks(artist_id=artist_id)
            elif category == 'Songs With Similar BPM':
                track_features = sp.audio_features([track_id])[0]
                bpm = track_features['tempo']
                recommended_music_names, recommended_artist_names, recommended_music_posters, recommended_music_previews = get_recommendations(track_id=track_id, target_bpm=bpm, outputs=int(outputs))

            cols = st.columns(5)
            num_recommendations = len(recommended_music_names)
            for i in range(100000):
                if i < num_recommendations:
                    with cols[i % 5]:
                        st.text(f"{recommended_music_names[i]} by {recommended_artist_names[i]}")
                        if recommended_music_previews[i]:
                            st.audio(recommended_music_previews[i])
                        else:
                            st.text("No preview available")
                        st.image(recommended_music_posters[i])
                
        else:
            st.write("No results found. Please try a different song and artist.")
    else:
        st.write("Please enter the song and artist in the format 'song by artist'.")
