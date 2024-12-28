import os
from discord import Intents
from dotenv import load_dotenv
from discord.ext import commands
from verification import verify_user
from utils import Embeds, EmailHandler, MessageHandler
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

handle_email = EmailHandler()
handle_message = MessageHandler(bot, handle_email)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    await log_bot_start(bot, CHANNEL_INTERACTION_LOG)


@bot.event
async def on_member_join(member):
    await send_welcome_dm(member)
    await log_member_join(bot, CHANNEL_JOIN_LEAVE_LOG, member)


@bot.event
async def on_member_remove(member):
    await log_member_leave(bot, CHANNEL_JOIN_LEAVE_LOG, member)


@bot.event
async def on_message(message):
    msg_status = handle_message(message)
    match msg_status:
        case 2: # DM message (not email)
            await bot.get_channel(CHANNEL_INTERACTION_LOG).send(embed=Embeds.LOG_MEMBER_INTERACTION(message))
        case 1: # bot message
            return
        case 0: # guild message
            return
        case 40:   # valid email
            await verify_user(message, bot.get_channel(CHANNEL_VERIFICATION_LOG))
        case -41:   # invalid email format
            await message.channel.send(embed=Embeds.EMAIL_INVALID())
        case -42:   # email not in db
            await message.channel.send(embed=Embeds.EMAIL_NOT_REGISTERED())
        case -43:   # email already verified
            await message.channel.send(embed=Embeds.EMAIL_ALREADY_VERIFIED())


if __name__ == "__main__":
    bot.run(TOKEN)
