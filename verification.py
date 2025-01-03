import asyncio
import email
from utils import Embeds, refine_email, DBManager
from discord.app_commands.errors import CommandInvokeError


class VerificationHandler:

    def __init__(self, bot, sheet_name, worksheet):
        self.bot = bot
        self.db = DBManager(sheet_name, worksheet)

    def verify_user(self, message, interaction=None):
        email = refine_email(message if isinstance(message, str) else message.content)
        print(f"Verifying user with email {email}")
        status = self.db.verify_member(email, interaction.user.id if interaction else message.author.id)
        return status

    async def send_embed(self, embed, message=None, interaction=None):
        if interaction is None:
            await message.channel.send(embed=embed)
            return 0

        try:
            await interaction.response.defer(ephemeral=True, thinking=True)
            await asyncio.sleep(7)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return 0
        except Exception as e:
            print(e)
            return -1
        

    async def __call__(self, message, interaction=None):
        msg = message if isinstance(message, str) else message
        
        status = self.verify_user(message, interaction)
        match status:
            case -1:    # Email not found
                await self.send_embed(Embeds.EMAIL_NOT_REGISTERED(), msg, interaction)
            case -2:    # Email already verified
                await self.send_embed(Embeds.EMAIL_ALREADY_VERIFIED(), msg, interaction)
            case -3:    # User already verified
                print("User already verified")
                await self.send_embed(Embeds.USER_ALREADY_VERIFIED(), msg, interaction)
            case 0:     # Use email to verify
                if interaction:
                    details = self.db.get_team_details_by_email(message)
                    await self.verification_log_channel.send(embed=Embeds.LOG_EMAIL_VERIFIED(interaction.user, message, details))
                else:
                    details = self.db.get_team_details_by_email(message.content)
                    await self.verification_log_channel.send(embed=Embeds.LOG_EMAIL_VERIFIED(message.author, message.content, details))

                response = await self.send_embed(Embeds.EMAIL_VERIFIED(), msg, interaction)
                if response == -1:
                    self.db.unverify_member(message)
                    # self.bot.send_message()
                    return -1, -1

                await self.add_verified_role(interaction.user if interaction else self.guild.get_member(message.author.id))
                return details
    
        return -1, -1
    
    async def add_verified_role(self, member):
        await member.add_roles(self.verified_role)
        print(f"Added verified role to {member}")
    
    def is_member_verified(self, member):
        return self.verified_role in member.roles
    
    def is_user_verified(self, user_id):
        member = self.guild.get_member(user_id)
        return self.verified_role.id in member.roles
