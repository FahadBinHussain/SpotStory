import tkinter as tk
from tkinter import messagebox, simpledialog
from spotstory import get_spotify_track_info, generate_image

def main():
    # Create GUI to get track URL
    root = tk.Tk()
    root.withdraw()
    track_url = simpledialog.askstring("Input", "Enter Spotify track URL:", parent=root)
    if not track_url:
        messagebox.showerror("Error", "No URL provided")
        return

    track_name, album_cover_url = get_spotify_track_info(track_url)
    generate_image(track_name, album_cover_url)
    messagebox.showinfo("Success", "Image saved as spotstory.png")

if __name__ == "__main__":
    main()