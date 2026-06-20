import yt_dlp

def download_youtube_as_mp3(video_url):
    # Configure downloading options
    ydl_opts = {
        'format': 'bestaudio/best',      # Fetch the highest quality audio stream
        'outtmpl': '%(title)s.%(ext)s',  # Set output filename to video title
        'postprocessors': [{             # Extract and convert audio to MP3 using FFmpeg
            'key': 'FFmpegExtractAudio', # Use FFmpeg to extract audio
            'preferredcodec': 'mp3',     # mp3 format
            'preferredquality': '192',   # Audio quality in kbps
        }],
    }

    try:
        print("Extracting audio and downloading...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Download and conversion complete!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Prompt user for the URL
    url = input("Please enter the YouTube Video URL: ")
    download_youtube_as_mp3(url)