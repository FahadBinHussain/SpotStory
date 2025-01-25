from flask import Flask, request, render_template, redirect, url_for
from spotstory import get_spotify_track_info, generate_image
import os

app = Flask(__name__)

# Route for the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Route for generating the image from a form submission
@app.route('/generate_image', methods=['POST'])
def generate_image_form():
    track_url = request.form.get('track_url')
    if not track_url:
        return redirect(url_for('index', error='No track URL provided'))

    track_name, album_cover_url = get_spotify_track_info(track_url)
    image_url = generate_image(track_name, album_cover_url)

    return redirect(url_for('show_image', image_url=image_url))

# Route to display the generated image
@app.route('/show_image')
def show_image():
    image_url = request.args.get('image_url')
    return render_template('show_image.html', image_url=image_url)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)