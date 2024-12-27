import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents
from bot_logs import log_bot_start, log_member_join

load_dotenv()
TOKEN = os.getenv('CLIENT_TOKEN')
CHANNEL_BOT_LOGS = int(os.getenv('CHANNEL_BOT_LOGS'))
CHANNEL_EVENT_ANALYTICS = int(os.getenv('CHANNEL_EVENT_ANALYTICS'))

intents = Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    await log_bot_start(bot, CHANNEL_BOT_LOGS)


@bot.event
async def on_member_join(member):
    await log_member_join(bot, CHANNEL_BOT_LOGS, member)


if __name__ == "__main__":
    bot.run(TOKEN)
