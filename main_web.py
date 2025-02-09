from flask import Flask, request, render_template, redirect, url_for
from spotstory import get_spotify_track_info, generate_image, get_youtube_video_info
import os
import threading
import requests
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Warm-up system to prevent cold starts
def warm_up():
    time.sleep(10)  # Wait for app to initialize
    while True:
        try:
            # Ping both health check AND a mock Spotify endpoint
            requests.get(f"http://localhost:5000/health")
            requests.post(f"http://localhost:5000/generate_image", data={
                "track_url": "https://open.spotify.com/track/11dFghVXANMlKmJXsNCbNl"  # Sample track
            }, timeout=10)
        except Exception as e:
            pass
        time.sleep(300)  # 5 minutes

if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
    threading.Thread(target=warm_up, daemon=True).start()

# Route for the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

# Route for generating the image from a form submission
@app.route('/generate_image', methods=['POST'])
def generate_image_form():
    track_url = request.form.get('track_url')
    if not track_url:
        return redirect(url_for('index', error='No URL provided'))

    try:
        if 'spotify.com' in track_url:
            title, image_url = get_spotify_track_info(track_url)
        elif 'youtube.com' in track_url or 'youtu.be' in track_url:
            title, image_url = get_youtube_video_info(track_url)
        else:
            return redirect(url_for('index', error='Invalid URL - must be Spotify or YouTube'))
            
        generated_url = generate_image(title, image_url)
        return redirect(url_for('show_image', image_url=generated_url))
        
    except Exception as e:
        return redirect(url_for('index', error=str(e)))

# Route to display the generated image
@app.route('/show_image')
def show_image():
    image_url = request.args.get('image_url')
    return render_template('show_image.html', image_url=image_url)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)