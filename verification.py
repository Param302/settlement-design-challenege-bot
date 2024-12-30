from utils import Embeds, refine_email, DBManager

db = DBManager()

def verify_user(message):
    email = refine_email(message.content)
    print(f"Verifying user with email {email}")
    status = db.verify_member(email, message.author.id)
    return status

class VerificationHandler:

    def verify_user(self, message):
        email = refine_email(message.content)
        print(f"Verifying user with email {email}")
        status = db.verify_member(email, message.author.id)
        return status

    async def __call__(self, message, channel):
        status = verify_user(message)
        match status:
            case -1:    # Email not found
                await message.channel.send(embed=Embeds.EMAIL_NOT_REGISTERED())
            case -2:    # Email already verified
                await message.channel.send(embed=Embeds.EMAIL_ALREADY_VERIFIED())
            case -3:    # User already verified
                print("User already verified")
                await message.channel.send(embed=Embeds.USER_ALREADY_VERIFIED())
                return
            case 0:     # Use email to verify
                await channel.send(embed=Embeds.LOG_EMAIL_VERIFIED(message.author, message.content))
                await message.channel.send(embed=Embeds.EMAIL_VERIFIED())
                # give user the role with the verified role: 1322142486369669140
                # give roles & handle category