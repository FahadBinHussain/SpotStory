import os
import requests
from PIL import Image, ImageDraw, ImageFont
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import io
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

# Load environment variables from .env file
load_dotenv()

# Set up Spotify API credentials from environment variables
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

# Set up Cloudinary configuration from environment variables
cloudinary.config(
  cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
  api_key=os.getenv('CLOUDINARY_API_KEY'),
  api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Ensure that the environment variables are loaded
if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    raise ValueError("Missing SPOTIPY_CLIENT_ID or SPOTIPY_CLIENT_SECRET environment variables")

# Set up Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

def get_spotify_track_info(track_url):
    """
    Fetches the track name and album cover URL from Spotify given a track URL.
    """
    track_info = sp.track(track_url)
    track_name = track_info['name']
    album_cover_url = track_info['album']['images'][0]['url']
    return track_name, album_cover_url

def generate_image(track_name, album_cover_url):
    """
    Generates an image with the track name overlaid on the album cover.
    Uploads the image to Cloudinary and returns the URL.
    """
    # Fetch album cover image
    response = requests.get(album_cover_url)
    album_cover = Image.open(io.BytesIO(response.content))

    # Create a new image with the same size as the album cover
    image = Image.new('RGB', album_cover.size)
    draw = ImageDraw.Draw(image)
    image.paste(album_cover, (0, 0))

    # Load a font with a larger size and ensure the font file is available
    font_path = os.path.join(os.path.dirname(__file__), 'arial.ttf')
    try:
        font = ImageFont.truetype(font_path, 40)  # Increase the font size
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size and position using textbbox
    text_bbox = draw.textbbox((0, 0), track_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (image.width - text_width) / 2
    text_y = (image.height - text_height) / 2

    # Add text to image
    draw.text((text_x, text_y), track_name, font=font, fill="white")

    # Save the image to a BytesIO object
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    # Upload the image to Cloudinary
    upload_result = cloudinary.uploader.upload(image_bytes, folder="spotstory")
    return upload_result['url']