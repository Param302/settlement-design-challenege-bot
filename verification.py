from discord import Color
from datetime import datetime
from utils import create_embed, refine_email

async def verify_user(message, channel):
    email = refine_email(message.content)
    embed = create_embed(
        title="Verification Successful",
        description="You have been successfully verified.",
        timestamp=datetime.now(),
        color=Color.green()
    )
    await message.channel.send(embed=embed)


    embed = create_embed(
        title="User Verified",
        description=f"{message.user.mention} has been verified with email {email}.",
        color=Color.green(),
        timestamp=datetime.now()
    )
    await channel.send(embed=embed)
