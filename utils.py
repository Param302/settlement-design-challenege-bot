import re
import discord
from gsheets import GSheets
from datetime import datetime
from discord import Color, Embed, Message
from discord import CategoryChannel, Role


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

def get_color():
    team_colors = [
    "#3357FF",  # Royal Blue
    "#FF8C33",  # Dark Orange
    "#8C33FF",  # Purple
    "#daa520",  # Goldenrod
]
    team_colors.append(team_colors.pop(0))
    return team_colors[-1]

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


class DBManager:
    """
    DataBase Manager
    """
    def __init__(self, sheet_name, worksheet):
        self.sheet = GSheets(sheet_name, worksheet)
    
    def get_team(self, team_id):
        return self.sheet.get_record_by_team_id(team_id)

    
    def get_team_details_by_email(self, email):
        team = self.sheet.get_team_by_email(email)
        return team, [member for member in team["Members"] if member["email"]==email][0]

    def verify_member(self, email, discord_id):
        return self.sheet.verify_member(email, discord_id)
    
    def unverify_member(self, email):
        return self.sheet.unverify_member(email)


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
    permissions = {
        "read_messages": True,
        "send_messages": True,
        "connect": True,
        "view_channel": True,
        "send_tts_messages": True,
        "embed_links": True,
        "attach_files": True,
        "read_message_history": True,
        "stream": True,
        "add_reactions": True,
        "send_voice_messages": True
    }

    def __init__(self, bot):
        self.bot = bot

    def permission_handler(self, handler):
        return handler(**self.permissions)

    async def create_category(self, team_name):
        overwrites = {
            self.guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel=False),
            self.verified_role: discord.PermissionOverwrite(read_messages=False, view_channel=False),
            self.core_team_role: discord.PermissionOverwrite(read_messages=True, view_channel=True),
            self.event_head_role: discord.PermissionOverwrite(read_messages=True, view_channel=True),
            self.volunteer_role: discord.PermissionOverwrite(read_messages=True, view_channel=True)
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
        role = await self.guild.create_role(
            name=team_name, 
            permissions=self.permission_handler(discord.Permissions), 
            color=discord.Color.from_str(get_color())
            )
        return await role.edit(position=1)

    async def connect_role_with_category(self, role: Role, category: CategoryChannel):
        overwrite_perms = self.permission_handler(discord.PermissionOverwrite)
        await category.set_permissions(role, overwrite=overwrite_perms)
        for channel in category.channels:
            await channel.set_permissions(role, overwrite=overwrite_perms)

    async def assign_roles_to_member(self, member, role: Role, is_leader=False):
        await member.add_roles(role)
        await member.add_roles(self.team_leader_role if is_leader else self.team_member_role)
    
    async def set_member_nickname(self, member, nickname):
        await member.edit(nick=nickname)

    async def is_new_team(self, team_name):
        role = discord.utils.get(self.guild.roles, name=team_name)
        category = discord.utils.get(self.guild.categories, name=team_name)
        return role is None and category is None


    async def __call__(self, user, team_details, member):
        await self.set_member_nickname(user, member["name"])
        team_name = team_details["Team Name"]
        if await self.is_new_team(team_name):
            category = await self.create_category(team_name)
            await self.create_channels(category)
            role = await self.create_role(team_name)
            await self.connect_role_with_category(role, category)
        else:
            role = discord.utils.get(self.guild.roles, name=team_name)

        await self.assign_roles_to_member(user, role, is_leader=member.get("leader", False))



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
    def LOG_EMAIL_VERIFIED(user, email, details):
        team, member = details
        # ! Add team details and member details
        embed = create_embed(
            title="User Verified",
            description=f"{user.mention} has been verified.",
            color=Color.green(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Username", value=member["name"], inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Team Name", value=team["Team Name"], inline=True)
        embed.add_field(name="Email", value=email, inline=True)
        if member.get("is_leader", False):
            embed.add_field(name="Team Leader", value="Yes", inline=True)
        embed.add_field(name="Total Members", value=team["Total Members"], inline=True)
        return embed

    
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
    
    @staticmethod
    def INTERACTION_ERROR():
        return create_embed(
            title="Error",
            description="There was an error processing your request. Please use the command again.",
            timestamp=datetime.now(),
            color=Color.orange()
        )
