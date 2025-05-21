import os
import sys
import yt_dlp

def download_youtube_to_mp3(url, output_folder="music", cookies_file=None):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': True,
    }

    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading and converting audio from: {url}")
        ydl.download([url])
        print(f"Download and conversion completed. Files saved in '{output_folder}' folder.")

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python youtube_to_mp3.py <YouTube URL> [cookies_file]")
        sys.exit(1)

    url = sys.argv[1]
    cookies_file = sys.argv[2] if len(sys.argv) == 3 else None
    download_youtube_to_mp3(url, cookies_file=cookies_file)

if __name__ == "__main__":
    main()
