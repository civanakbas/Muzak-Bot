import asyncio

import discord
import yt_dlp

from muzak.utils.logger import logger

ytdl_format_options = {
    'format': 'bestaudio/best'
}

ffmpeg_options = {
    'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class AudioPlayer(discord.PCMVolumeTransformer):
    """Audio playback using FFmpeg and yt-dlp."""

    def __init__(self, source, *, data, volume=0.3):
        """Initializes the AudioPlayer.

        Args:
            source: The audio source to be played.
            data: Metadata related to the audio.
            volume: The volume of the audio playback.

        Returns:
            None
        """
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def create_from_url(cls, url, *, loop=None, stream=True, start_time=0):
        """Creates an AudioPlayer instance from a YouTube URL.

        Args:
            url: The YouTube video URL.
            loop: The asyncio event loop (optional).
            stream: Whether to stream or download the video (default is True).
            start_time: The start time in seconds to seek to in the video (default is 0).

        Returns:
            AudioPlayer: An instance of AudioPlayer.
        """
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)

        ffmpeg_opts = ffmpeg_options.copy()
        if start_time > 0:
            ffmpeg_opts['options'] += f' -ss {start_time}'

        logger.info(f"Audio file created from URL: {url}, starting at {start_time} seconds.")
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_opts), data=data)
