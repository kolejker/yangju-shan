import yt_dlp
import random
import os
import subprocess

async def get_random_video_url(channels):
    channel_url = random.choice(channels)

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)

    video_entries = info.get('entries', [])
    if not video_entries:
        raise Exception("no video mod osu")

    video = random.choice(video_entries)
    video_url = f"https://www.youtube.com/watch?v={video['id']}"
    return video_url

async def download_and_compress(video_url):
    temp_filename = 'video.mp4'
    compressed_filename = 'compressed_video.mp4'

    ydl_opts = {
        'format': 'bestvideo[height<=240]+bestaudio/best[height<=240]/best[height<=240]/best',
        'outtmpl': temp_filename,
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    size_bytes = os.path.getsize(temp_filename)
    if size_bytes <= 10 * 1024 * 1024:
        return temp_filename

    ydl_opts_info = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(video_url, download=False)
    duration = info.get('duration', 60)
    target_bitrate = (10 * 1024 * 1024 * 8) / duration
    target_bitrate_k = target_bitrate / 1000

    cmd = [
        'ffmpeg', '-y', '-i', temp_filename,
        '-b:v', f'{int(target_bitrate_k)}k',
        '-bufsize', f'{int(target_bitrate_k)}k',
        '-maxrate', f'{int(target_bitrate_k)}k',
        compressed_filename
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(compressed_filename) and os.path.getsize(compressed_filename) <= 10 * 1024 * 1024:
        os.remove(temp_filename)
        return compressed_filename
    else:
        if os.path.getsize(temp_filename) <= 10 * 1024 * 1024:
            os.remove(compressed_filename)
            return temp_filename
        os.remove(temp_filename)
        if os.path.exists(compressed_filename):
            os.remove(compressed_filename)
        return None