from datetime import datetime
import os
from dotenv import load_dotenv
from discord.ext import commands
from verification import verify_user
from discord import Color, Intents
from utils import create_embed, email_in_db, email_already_verified, refine_email, valid_format
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


# call verify_user when a user DMs the bot
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.guild is not None:
        return
    print(f"Received DM from {message.author}")
    print("Message content:", message.content)
    channel = bot.get_channel(CHANNEL_VERIFICATION_LOG)
    
    email = refine_email(message.content)
    if not valid_format(email):
        embed = create_embed(
            title="Invalid Email Format",
            description="Please provide a valid IITM student email ID.",
            timestamp=datetime.now(),
            color=Color.orange()
        )
        await message.channel.send(embed=embed)
        return
    
    if not email_in_db(email):
        embed = create_embed(
            title="Email Not Registered",
            description="Make sure you have registered your email",
            timestamp=datetime.now(),
            color=Color.red()
        )
        await message.channel.send(embed=embed)
        return

    if email_already_verified(email):
        embed = create_embed(
            title="Email Already Verified",
            description="This email has already been verified.",
            timestamp=datetime.now(),
            color=Color.red()
        )
        await message.channel.send(embed=embed)
        return

    await verify_user(message, channel)




if __name__ == "__main__":
    bot.run(TOKEN)
