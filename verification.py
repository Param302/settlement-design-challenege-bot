from utils import Embeds, refine_email, DBManager

db = DBManager()

async def verify_user(message, channel):
    email = refine_email(message.content)
    print(f"Verifying user with email {email}")
    # ! add verification logic
    status = db.verify_member(email, message.author.id)
    match status:
        case -1:    # Email not found
            await message.channel.send(embed=Embeds.EMAIL_NOT_REGISTERED())
        case -2:   # User already verified
            await message.channel.send(embed=Embeds.EMAIL_ALREADY_VERIFIED())
        case 0:   # Use email to verify
            await message.channel.send(embed=Embeds.EMAIL_VERIFIED())
            await channel.send(embed=Embeds.LOG_EMAIL_VERIFIED(message.author, email))
