import discord
from datetime import datetime
from utils import create_embed

async def log_bot_start(bot, channel_id):
    channel = bot.get_channel(channel_id)

    embed = create_embed(
        title="Bot Status",
        description="The bot is now online and ready to serve!",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )
    await channel.send(embed=embed)


async def log_member_join(bot, channel_id, member):
    channel = bot.get_channel(channel_id)
    
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


async def log_member_leave(bot, channel_id, member):
    channel = bot.get_channel(channel_id)
    
    embed = create_embed(
        title=f"Member Left",
        description=f"{member.mention} has left the server.",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="User ID", value=member.id, inline=True)
    await channel.send(embed=embed)


async def send_welcome_dm(member):
    try:
        server_image_url = "https://avatars.githubusercontent.com/u/181232261?s=200&v=4"  # Replace with your server image URL
        embed = create_embed(
            title=f"Welcome to {member.guild.name.title()}!",
            description="We're glad to have you here.",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=server_image_url)
        embed.add_field(
            name="Get Started",
            value="Please share your IITM student email ID to join your team.",
            inline=False
        )
        embed.add_field(
            name="Need Help?",
            value="If you have any questions, feel free to reply here.",
            inline=False
        )
        await member.send(embed=embed)
    except discord.Forbidden:
        print(f"Could not send DM to {member.name}")


