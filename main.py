import os
import requests
from PIL import Image, ImageDraw, ImageFont
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import io
from dotenv import load_dotenv
import argparse
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

# Load environment variables from .env file
load_dotenv()

# Set up Spotify API credentials from environment variables
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

# Ensure that the environment variables are loaded
if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    raise ValueError("Missing SPOTIPY_CLIENT_ID or SPOTIPY_CLIENT_SECRET environment variables")

# Set up Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                           client_secret=SPOTIPY_CLIENT_SECRET))

def get_spotify_track_info(track_url):
    track_info = sp.track(track_url)
    track_name = track_info['name']
    album_cover_url = track_info['album']['images'][0]['url']
    return track_name, album_cover_url

def generate_image(track_name, album_cover_url):
    # Fetch album cover image
    response = requests.get(album_cover_url)
    album_cover = Image.open(io.BytesIO(response.content))

    # Create a new image with the same size as the album cover
    image = Image.new('RGB', album_cover.size)
    draw = ImageDraw.Draw(image)
    image.paste(album_cover, (0, 0))

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", 40)
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

    # Save the image
    image.save('spotstory.png')

def main(track_url=None):
    if track_url is None:
        # Create GUI to get track URL
        root = tk.Tk()
        root.withdraw()
        track_url = simpledialog.askstring("Input", "Enter Spotify track URL:", parent=root)
        if not track_url:
            messagebox.showerror("Error", "No URL provided")
            return

    track_name, album_cover_url = get_spotify_track_info(track_url)
    generate_image(track_name, album_cover_url)
    print("Image saved as spotstory.png")
    if track_url is None:
        messagebox.showinfo("Success", "Image saved as spotstory.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate an image from a Spotify track URL.')
    parser.add_argument('track_url', type=str, nargs='?', help='The Spotify track URL')
    args = parser.parse_args()

    main(args.track_url)