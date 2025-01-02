import re
from datetime import datetime
from discord import Color, Embed, Message
import discord
from discord import CategoryChannel, TextChannel, VoiceChannel, Role

data = {
    1: {
        "Team Name": "Dynamic Achievers",
        "Total Members": 4,
        "Members": [
            {"email": "22ds1195676@es.study.iitm.ac.in", "name": "Kavita Mehta", "verified": False, "discord_id": None},
            {"email": "27ds3369641@ds.study.iitm.ac.in", "name": "Neha Jain", "verified": False, "discord_id": None, "leader": True},
            {"email": "26ds3122880@ds.study.iitm.ac.in", "name": "Manish Patel", "verified": False, "discord_id": None},
            {"email": "29dp2169012@ds.study.iitm.ac.in", "name": "Priya Joshi", "verified": False, "discord_id": None},
        ],
    },
    2: {
        "Team Name": "Persistent Thinkers",
        "Total Members": 6,
        "Members": [
            {"email": "24dp2397095@es.study.iitm.ac.in", "name": "Ramesh Iyer", "verified": False, "discord_id": None},
            {"email": "27ds3116586@ds.study.iitm.ac.in", "name": "Ramesh Gupta", "verified": False, "discord_id": None},
            {"email": "21dp3104587@ds.study.iitm.ac.in", "name": "Kavita Patel", "verified": False, "discord_id": None},
            {"email": "29dp3112299@es.study.iitm.ac.in", "name": "Sanjay Jain", "verified": False, "discord_id": None},
            {"email": "29f1101297@es.study.iitm.ac.in", "name": "Vikram Joshi", "verified": False, "discord_id": None, "leader": True},
            {"email": "21dp2114529@es.study.iitm.ac.in", "name": "Ramesh Reddy", "verified": False, "discord_id": None},
        ],
    },
    3: {
        "Team Name": "Creative Explorers",
        "Total Members": 4,
        "Members": [
            {"email": "29ds2258290@ds.study.iitm.ac.in", "name": "Arjun Sharma", "verified": False, "discord_id": None, "leader": True},
            {"email": "21ds3116945@es.study.iitm.ac.in", "name": "Vikram Patel", "verified": False, "discord_id": None},
            {"email": "21dp3396612@ds.study.iitm.ac.in", "name": "Neha Joshi", "verified": False, "discord_id": None},
            {"email": "21ds2371392@ds.study.iitm.ac.in", "name": "Neha Joshi", "verified": False, "discord_id": None},
        ],
    },
    4: {
        "Team Name": "Intrepid Explorers",
        "Total Members": 4,
        "Members": [
            {"email": "21ds3150305@es.study.iitm.ac.in", "name": "Anjali Sharma", "verified": False, "discord_id": None},
            {"email": "29ds2144879@ds.study.iitm.ac.in", "name": "Manish Jain", "verified": False, "discord_id": None, "leader": True},
            {"email": "27ds1230945@ds.study.iitm.ac.in", "name": "Priya Joshi", "verified": False, "discord_id": None},
            {"email": "25dp1255001@ds.study.iitm.ac.in", "name": "Sanjay Mehta", "verified": False, "discord_id": None},
        ],
    },
    5: {
        "Team Name": "Persistent Pioneers",
        "Total Members": 5,
        "Members": [
            {"email": "23dp2163699@es.study.iitm.ac.in", "name": "Kavita Choudhary", "verified": False, "discord_id": None},
            {"email": "22ds339011@es.study.iitm.ac.in", "name": "Ramesh Joshi", "verified": False, "discord_id": None},
            {"email": "21f3333668@es.study.iitm.ac.in", "name": "Neha Patel", "verified": False, "discord_id": None, "leader": True},
            {"email": "21f3391640@ds.study.iitm.ac.in", "name": "Riya Joshi", "verified": False, "discord_id": None},
            {"email": "25dp3325396@ds.study.iitm.ac.in", "name": "Vikram Patel", "verified": False, "discord_id": None},
        ],
    },
}


def create_embed(title, description, color, **kwargs):
    return Embed(
        title=title,
        description=description,
        color=color,
        **kwargs
    ).set_footer(text="IITM Bot")


def refine_email(email):
    return email.strip().lower()


class MessageHandler:
    # if the message is from the bot, ignore it
    # if the message is in DM channel
    # - if the author has sent the email
    # - - if the author is already verified (has verified role), say already verified
    # - - if the author is not verified, verify the author - Email Handler
    # - if the author has sent normal message, send it to member interaction channel
    # if the message is in guild channel, <under construction hehe>

    def __init__(self, bot, handle_email):
        self.bot = bot
        self._handle_email = handle_email

    def _is_DM(self, message):
        return message.guild is None
    
    def _is_bot_message(self, message: Message):
        return message.author.id == self.bot.user.id
    
    def _is_email(self, message: Message):
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        return email_pattern.match(message.content)


    def __call__(self, message: Message) -> int:
        if self._is_bot_message(message):
            return 1
        if self._is_DM(message):
            if self._is_email(message):
                return self._handle_email(message)
            return 2
        return 0



class EmailHandler:

    def _refine_email(self, message):
        return refine_email(message.content)
    
    def _is_valid_format(self, email):
        email_pattern = re.compile(r"^(2[1-9])(f|ds|dp)[1-3]\d{6}@(ds|es)\.study\.iitm\.ac\.in$")
        return email_pattern.match(email)

    def __call__(self, email) -> int:
        email = self._refine_email(email)
        if not self._is_valid_format(email):
            return -41
        return 40


# ! Update the sheet, create new sheet, verified column and discord id for each email 
# currently, use a dictionary to store the data

class DBManager:
    """
    DataBase Manager
    """
    def __init__(self):
        self.db = data
    
    def get_team(self, team_id):
        return self.db.get(team_id)
    
    def get_team_details_by_email(self, email):
        team_id, member = self.find_record_by("email", email)
        if team_id == -1:
            return -1
        return self.get_team(team_id)

    def find_record_by(self, key, value):
        print("Finding record by", key, value, type(key), type(value))
        for team_id, team in self.db.items():
            for member in team["Members"]:
                if member[key] == value:
                    return team_id, member
        return -1, -1
    
    def is_member_verified(self, discord_id):
        team_id, member = self.find_record_by("discord_id", discord_id)
        if team_id == -1:
            return -1, -1
        return member.get("verified"), member

    def is_email_verified(self, member_email):
        team_id, member = self.find_record_by("email", member_email)
        if team_id == -1:
            return -1, -1
        return member.get("verified"), member

    def verify_member(self, email, discord_id):
        member_status, _ = self.is_member_verified(discord_id)

        if member_status != -1 and member_status:
            print("Verified hai bhyiiii!!!", self.is_member_verified(discord_id))
            return -3
        
        status, member = self.is_email_verified(email)
        if status==-1:
            return -1
        
        if status:
            return -2

        member["verified"] = True
        member["discord_id"] = discord_id
        return 0
    
    def unverify_member(self, email):
        status, member = self.is_email_verified(email)

        if status==-1:
            return -1

        if not status:
            return -2
    
        member["verified"] = False
        member["discord_id"] = None
        return 0


class TeamManager:
    """
    if only one member is verified, 
    - create respective team category
    - create respective team channels
    - create respective team role
    - connect roles with category
    - assign roles to that member
    - rename member nickname to registered name

    if more than one member is verified, then 
    - assign roles to all respective team members

    if member is leader, then
    - assign team leader role to that member
    """
    """
    Each team will have a category,
    in a category, there will be following channels:
    - structure
    - operations
    - human factor
    - automation
    - team vc
    - general chat

    Each team will have a role, (team name) with following perms:
    - read messages
    - send messages
    - connect to voice
    - view channel
    - send tts messages
    - embed links
    - attach files
    - read message history
    - share screen
    - add reactions
    - send voice messages
    """

    def __init__(self, bot):
        self.bot = bot

    async def create_category(self, team_name):
        overwrites = {
            self.guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel=False),
            self.verified_role: discord.PermissionOverwrite(read_messages=False, view_channel=False)
        }
        return await self.guild.create_category(team_name, overwrites=overwrites)

    async def create_channels(self, category: CategoryChannel):
        channels = ["structure", "operations", "human factor", "automation", "team vc", "general chat"]
        for channel in channels:
            if "vc" in channel:
                await category.create_voice_channel(channel)
            else:
                await category.create_text_channel(channel)

    async def create_role(self, team_name):
        permissions = discord.Permissions(
            read_messages=True,
            send_messages=True,
            connect=True,
            view_channel=True,
            send_tts_messages=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            stream=True,
            add_reactions=True,
            send_voice_messages=True
        )
        role = await self.guild.create_role(name=team_name, permissions=permissions)
        return await role.edit(position=1)

    async def connect_role_with_category(self, role: Role, category: CategoryChannel):
        overwrite_perms = discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                connect=True,
                view_channel=True,
                send_tts_messages=True,
                embed_links=True,
                attach_files=True,
                read_message_history=True,
                stream=True,
                add_reactions=True,
                send_voice_messages=True
            )
        await category.set_permissions(role, overwrite=overwrite_perms)
        for channel in category.channels:
            await channel.set_permissions(role, overwrite=overwrite_perms)

    async def assign_roles_to_member(self, member, role: Role, is_leader=False):
        await member.add_roles(role)
        if is_leader:
            leader_role = discord.utils.get(self.guild.roles, id=1322141544299630612)
            await member.add_roles(leader_role)
        await member.edit(nick=member.display_name)

    async def is_new_team(self, team_details):
        role = discord.utils.get(self.guild.roles, name=team_details["Team Name"])
        return role is None

    async def __call__(self, team_details, member, is_leader=False):
        if await self.is_new_team(team_details):
            category = await self.create_category(team_details["Team Name"])
            await self.create_channels(category, team_details["Team Name"])
            role = await self.create_role(team_details["Team Name"])
            await self.connect_role_with_category(role, category)
            await self.assign_roles_to_member(member, role, is_leader)
        else:
            role = discord.utils.get(self.guild.roles, name=team_details["Team Name"])
            await self.assign_roles_to_member(member, role, is_leader)



class Embeds:

    @staticmethod
    def LOG_BOT_START():
        return create_embed(
            title="Bot Status",
            description="The bot is now online and ready to serve!",
            color=Color.green(),
            timestamp=datetime.now()
        )
    

    @staticmethod
    def LOG_NEW_MEMBER(member):
        embed = create_embed(
            title=f"New Member Joined",
            description=f"{member.mention} has joined the server.",
            color=Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        return embed
    
    @staticmethod
    def LOG_MEMBER_LEAVE(member):
        embed = create_embed(
            title=f"Member Left",
            description=f"{member.mention} has left the server.",
            color=Color.red(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        return embed

    @staticmethod
    def LOG_EMAIL_VERIFIED(user, email):
        # ! Add team details and member details
        return create_embed(
            title="User Verified",
            description=f"{user.mention} has been verified with email `{email}`.",
            color=Color.green(),
            timestamp=datetime.now()
        )
    
    @staticmethod
    def LOG_MEMBER_INTERACTION(message):
        embed = create_embed(
            title=f"{message.author.display_name} has sent a message!",
            description="This message was sent in DM. <ping @volunteers>",
            color=Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar.url if message.author.avatar else None)
        embed.add_field(name="Message", value=message.content, inline=False)
        embed.add_field(name="Username", value=message.author.name, inline=True)
        embed.add_field(name="User ID", value=message.author.id, inline=True)
        return embed

    
    @staticmethod
    def SEND_WELCOME_DM(member, server_image_url):
        embed = create_embed(
            title=f"Welcome to {member.guild.name.title()}!",
            description="We're glad to have you here.",
            color=Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=server_image_url)
        embed.add_field(
            name="Get Started",
            value="Please share your IITM student email ID to join your team.",
            inline=False
        )
        return embed


    @staticmethod
    def EMAIL_INVALID():
        return create_embed(
            title="Invalid Email Format",
            description="Please provide a valid IITM student email ID.",
            timestamp=datetime.now(),
            color=Color.orange()
        )
    
    @staticmethod
    def EMAIL_NOT_REGISTERED():
        return create_embed(
            title="Email Not Registered",
            description="Make sure you have registered in the challenge.",
            timestamp=datetime.now(),
            color=Color.red()
        )
    
    @staticmethod
    def EMAIL_ALREADY_VERIFIED():
        return create_embed(
            title="Email Already Verified",
            description="This email has already been verified.",
            timestamp=datetime.now(),
            color=Color.red()
        )
    
    @staticmethod
    def EMAIL_VERIFIED():
        return create_embed(
            title="Verification Successful",
            description="You have been successfully verified.",
            timestamp=datetime.now(),
            color=Color.green()
        )
    
    @staticmethod
    def USER_ALREADY_VERIFIED():
        return create_embed(
            title="Already Verified",
            description="You have already been verified.",
            timestamp=datetime.now(),
            color=Color.blue()
        )
