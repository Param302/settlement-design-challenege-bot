import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents
from bot_logs import log_bot_start, log_member_join, log_member_leave, send_welcome_dm

load_dotenv()
TOKEN = os.getenv('CLIENT_TOKEN')
CHANNEL_EVENT_ANALYTICS = int(os.getenv('CHANNEL_EVENT_ANALYTICS'))
CHANNEL_INTERACTION_LOG = int(os.getenv('CHANNEL_INTERACTION_LOG'))
CHANNEL_JOIN_LEAVE_LOG = int(os.getenv('CHANNEL_JOIN_LEAVE_LOG'))
CHANNEL_VERIFICATION_LOG = int(os.getenv('CHANNEL_VERIFICATION_LOG'))

intents = Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    await log_bot_start(bot, CHANNEL_INTERACTION_LOG)


@bot.event
async def on_member_join(member):
    await log_member_join(bot, CHANNEL_JOIN_LEAVE_LOG, member)
    await send_welcome_dm(member)


@bot.event
async def on_member_remove(member):
    await log_member_leave(bot, CHANNEL_JOIN_LEAVE_LOG, member)


if __name__ == "__main__":
    bot.run(TOKEN)
