import os
from dotenv import load_dotenv
from discord.ext.commands import Bot
from verification import VerificationHandler
from utils import Embeds, EmailHandler, MessageHandler, TeamManager
from discord import app_commands, Intents, Interaction, Object, Guild
from bot_logs import log_bot_start, log_member_join, log_member_leave, send_welcome_dm

load_dotenv()
TOKEN = os.getenv('CLIENT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL_EVENT_ANALYTICS = int(os.getenv('CHANNEL_EVENT_ANALYTICS'))
CHANNEL_INTERACTION_LOG = int(os.getenv('CHANNEL_INTERACTION_LOG'))
CHANNEL_JOIN_LEAVE_LOG = int(os.getenv('CHANNEL_JOIN_LEAVE_LOG'))
CHANNEL_VERIFICATION_LOG = int(os.getenv('CHANNEL_VERIFICATION_LOG'))
ROLE_EVERYONE = int(os.getenv('ROLE_EVERYONE'))
ROLE_VERIFIED = int(os.getenv('ROLE_VERIFIED'))
ROLE_TEAM_LEADER = int(os.getenv('ROLE_TEAM_LEADER'))
ROLE_TEAM_MEMBER = int(os.getenv('ROLE_TEAM_MEMBER'))
SHEET_NAME = os.getenv('SHEET_NAME')
WORKSHEET = os.getenv('WORKSHEET')

intents = Intents.all()
intents.members = True
bot = Bot(command_prefix="!", intents=intents)
server = Object(id=GUILD_ID)
print(GUILD_ID)
print(server)
handle_email = EmailHandler()
handle_message = MessageHandler(bot, handle_email)
handle_verification = VerificationHandler(bot, SHEET_NAME, WORKSHEET)
manage_team = TeamManager(bot)


@bot.event
async def on_ready():
    global handle_verification
    print(f"Bot is online as {bot.user}")
    await bot.tree.sync(guild=server)
    await log_bot_start(bot, CHANNEL_INTERACTION_LOG)
    handle_verification.guild = manage_team.guild = bot.get_guild(GUILD_ID)
    handle_verification.verified_role = manage_team.verified_role = handle_verification.guild.get_role(ROLE_VERIFIED)
    handle_verification.verification_log_channel = handle_verification.guild.get_channel(CHANNEL_VERIFICATION_LOG)
    manage_team.team_leader_role = handle_verification.guild.get_role(ROLE_TEAM_LEADER)
    manage_team.team_member_role = handle_verification.guild.get_role(ROLE_TEAM_MEMBER)
    print("I am ready")



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
            if handle_verification.is_user_verified(message.author.id):
                await message.channel.send(embed=Embeds.USER_ALREADY_VERIFIED())
                return
            team_details, member = await handle_verification(message)
            if team_details != -1 and member != -1: # team details found
                user = bot.get_guild(GUILD_ID).get_member(message.author.id)
                await manage_team(user, team_details, member)
            # await team_category_manager.handle_team_creation(team_details, message.author)
        case -41:   # invalid email format
            await message.channel.send(embed=Embeds.EMAIL_INVALID())

#! Removing command for now - as DMs are working & discord interaction error
# @bot.tree.command(name="jointeam", description="Join your team with your student email ID.", guild=server)
# @app_commands.describe(student_mail_id="Your Student email ID.")
# async def jointeam(interaction: Interaction, student_mail_id: str):
#     team_details, member = await handle_verification(student_mail_id, interaction)
#     if team_details != -1 and member != -1: # team details found
#         await manage_team(interaction.user, team_details, member)

if __name__ == "__main__":
    bot.run(TOKEN)
