from utils import Embeds, refine_email, DBManager

db = DBManager()

def verify_user(message, interaction=None):
    email = refine_email(message if isinstance(message, str) else message.content)
    print(f"Verifying user with email {email}")
    status = db.verify_member(email, interaction.author.id if interaction else message.author.id)
    return status

class VerificationHandler:

    def __init__(self, bot):
        self.bot = bot

    def verify_user(self, message, interaction=None):
        email = refine_email(message if isinstance(message, str) else message.content)
        print(f"Verifying user with email {email}")
        status = db.verify_member(email, interaction.user.id if interaction else message.author.id)
        return status

    async def send_embed(self, embed, message=None, interaction=None):
        if interaction:
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        await message.channel.send(embed=embed)

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
                return
            case 0:     # Use email to verify
                if interaction:
                    await self.verification_log_channel.send(embed=Embeds.LOG_EMAIL_VERIFIED(interaction.user, message))
                else:
                    await self.verification_log_channel.send(embed=Embeds.LOG_EMAIL_VERIFIED(message.author, message.content))

                await self.send_embed(Embeds.EMAIL_VERIFIED(), msg, interaction)
                await self.add_verified_role(interaction.user if interaction else self.guild.get_member(message.author.id))
                return db.get_team_details_by_email(refine_email(msg))
                # give roles & handle category
    
    async def add_verified_role(self, member):
        await member.add_roles(self.verified_role)
        print(f"Added verified role to {member}")
    
    def is_member_verified(self, member):
        return self.verified_role in member.roles
    
    def is_user_verified(self, user_id):
        member = self.guild.get_member(user_id)
        return self.verified_role.id in member.roles
    
    # async def manage_category(self, member):

        # if self.is_member_verified(member):
        #     await member.move_to(self.verified_category)
        # else:
        #     await member.move_to(self.unverified_category)
