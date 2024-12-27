import discord
from datetime import datetime
from utils import create_embed

async def log_bot_start(bot, channel_id):
    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"Could not find channel with ID {channel_id}")
        return

    embed = create_embed(
        title="Bot Status",
        description="The bot is now online and ready to serve!",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )
    await channel.send(embed=embed)


async def log_member_join(bot, channel_id, member):
    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"Could not find channel with ID {channel_id}")
        return
    
    embed = create_embed(
        title=f"New Member Joined",
        description=f"{member.mention} has joined the server.",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="User ID", value=member.id, inline=True)
    await channel.send(embed=embed)



