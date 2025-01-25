## Spotstory

Spotstory is an open-source project that generates images based on Spotify track information. It provides both a desktop GUI and a web interface.

### Offline Usage

To use Spotstory offline with the desktop GUI:

1. Ensure you have Python installed.
2. Install the required dependencies:
   `pip install -r requirements.txt`

3. Run the desktop application:
`python main_desktop.py`
Online Usage
To use Spotstory online:

Deploy the application to a platform like Render using the provided render.yaml configuration.
Interact with the web interface by sending POST requests to the /generate_image endpoint with a JSON payload containing the track_url.
sh
curl -X POST http://your-render-url/generate_image -H "Content-Type: application/json" -d '{"track_url": "spotify_track_url_here"}'
Dependencies
requests
pillow
spotipy
python-dotenv
flask
tkinter
Environment Variables
Ensure you have a .env file with the following variables:

Code
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret