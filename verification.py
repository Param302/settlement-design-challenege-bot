from utils import Embeds, refine_email

async def verify_user(message, channel):
    email = refine_email(message.content)
    print(f"Verifying user with email {email}")
    # ! add verification logic
    await message.channel.send(embed=Embeds.EMAIL_VERIFIED())
    await channel.send(embed=Embeds.LOG_EMAIL_VERIFIED(message.author, email))
