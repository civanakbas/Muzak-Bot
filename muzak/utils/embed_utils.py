import discord


def get_avatar_url(author: discord.User) -> str:
    """Helper function to get the avatar URL or a default if not available.

    Args:
        author: The user object to get the avatar URL from.

    Returns:
        str: The avatar URL or a default image URL.
    """
    return author.avatar.url if author.avatar else str(author.default_avatar.url)


def song_added_embed(
    url: str,
    author_name: str,
    author_avatar_url: str
) -> discord.Embed:
    """Function to create an embed for when a song is added to the queue.

    Args:
        url: The URL of the song.
        author_name: The name of the user who requested the song.
        author_avatar_url: The URL of the user's avatar.

    Returns:
        discord.Embed: The embed object for the song added message.
    """
    embed = discord.Embed(
        title="🎶 Song Added to Queue",
        description=f"[Click here to view the video]({url})",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Requested by {author_name}", icon_url=author_avatar_url)
    return embed

def now_playing_embed(
    song_title: str,
    author_name: str,
    author_avatar_url: str
) -> discord.Embed:
    """Function to create an embed for the currently playing song.

    Args:
        song_title: The title of the currently playing song.
        author_name: The name of the user who requested the song.
        author_avatar_url: The URL of the user's avatar.

    Returns:
        discord.Embed: The embed object for the now playing message.
    """
    embed = discord.Embed(
        title="🎶 Now Playing",
        description=song_title,
        color=discord.Color.purple()
    )
    embed.set_footer(text=f"Requested by {author_name}", icon_url=author_avatar_url)
    return embed

def song_skipped_embed(
    author_name: str,
    author_avatar_url: str
) -> discord.Embed:
    """Function to create an embed for when a song is skipped.

    Args:
        author_name: The name of the user who skipped the song.
        author_avatar_url: The URL of the user's avatar.

    Returns:
        discord.Embed: The embed object for the song skipped message.
    """
    embed = discord.Embed(
        title="⏭️ Song Skipped",
        description="The current song has been skipped.",
        color=discord.Color.orange()
    )
    embed.set_footer(text=f"Skipped by {author_name}", icon_url=author_avatar_url)
    return embed

def queue_display_embed(
    queue_list: str,
    author_name: str,
    author_avatar_url: str
) -> discord.Embed:
    """Function to create an embed for displaying the current song queue.

    Args:
        queue_list: A string representation of the current song queue.
        author_name: The name of the user who requested to view the queue.
        author_avatar_url: The URL of the user's avatar.

    Returns:
        discord.Embed: The embed object for displaying the queue.
    """
    embed = discord.Embed(
        title="🎵 Current Queue",
        description=queue_list,
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Requested by {author_name}", icon_url=author_avatar_url)
    return embed

def empty_queue_embed(
    author_name: str,
    author_avatar_url: str
) -> discord.Embed:
    """Function to create an embed for when the queue is empty.

    Args:
        author_name: The name of the user who requested to view the queue.
        author_avatar_url: The URL of the user's avatar.

    Returns:
        discord.Embed: The embed object indicating that the queue is empty.
    """
    embed = discord.Embed(
        title="🎵 Current Queue",
        description="The queue is empty!",
        color=discord.Color.red()
    )
    embed.set_footer(text=f"Requested by {author_name}", icon_url=author_avatar_url)
    return embed

def ping_embed(
    latency: int,
    author_name: str,
    author_avatar_url: str
) -> discord.Embed:
    """Function to create an embed for the ping command.

    Args:
        latency: The latency of the bot in milliseconds.
        author_name: The name of the user who invoked the command.
        author_avatar_url: The URL of the user's avatar.

    Returns:
        discord.Embed: The embed object for the ping command.
    """
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: {latency}ms",
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Requested by {author_name}", icon_url=author_avatar_url)
    return embed

def join_channel_embed(
    channel_name: str,
    author_name: str,
    author_avatar_url: str
) -> discord.Embed:
    """Function to create an embed for joining a voice channel.

    Args:
        channel_name: The name of the channel the bot joined.
        author_name: The name of the user who invoked the command.
        author_avatar_url: The URL of the user's avatar.

    Returns:
        discord.Embed: The embed object for joining a voice channel.
    """
    embed = discord.Embed(
        title="🔊 Joined Voice Channel",
        description=f"Connected to {channel_name}",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Requested by {author_name}", icon_url=author_avatar_url)
    return embed

def leave_channel_embed(
    channel_name: str,
    author_name: str,
    author_avatar_url: str
) -> discord.Embed:
    """Function to create an embed for leaving a voice channel.

    Args:
        channel_name: The name of the channel the bot left.
        author_name: The name of the user who invoked the command.
        author_avatar_url: The URL of the user's avatar.

    Returns:
        discord.Embed: The embed object for leaving a voice channel.
    """
    embed = discord.Embed(
        title="👋 Left Voice Channel",
        description=f"Disconnected from {channel_name}",
        color=discord.Color.red()
    )
    embed.set_footer(text=f"Requested by {author_name}", icon_url=author_avatar_url)
    return embed
