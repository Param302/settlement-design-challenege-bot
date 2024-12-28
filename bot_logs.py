from utils import Embeds
from discord import Forbidden

async def log_bot_start(bot, channel_id):
    channel = bot.get_channel(channel_id)
    await channel.send(embed=Embeds.LOG_BOT_START())


async def log_member_join(bot, channel_id, member):
    channel = bot.get_channel(channel_id)
    await channel.send(embed=Embeds.LOG_NEW_MEMBER(member))


async def log_member_leave(bot, channel_id, member):
    channel = bot.get_channel(channel_id)
    await channel.send(embed=Embeds.LOG_MEMBER_LEAVE(member))


async def send_welcome_dm(member):
    try:
        server_image_url = "https://avatars.githubusercontent.com/u/181232261?s=200&v=4"
        await member.send(embed=Embeds.SEND_WELCOME_DM(member, server_image_url))
    except Forbidden:
        print(f"Could not send DM to {member.name}")


