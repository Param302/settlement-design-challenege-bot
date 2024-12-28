import re
from discord import Embed

data = {
    "21f1234567@ds.study.iitm.ac.in": "Param",
}


def refine_email(email):
    return email.strip().lower()

def valid_format(email):
    email_pattern = re.compile(r"^(2[1-9])(f|ds|dp)[1-3]\d{6}@(ds|es)\.study\.iitm\.ac\.in$")
    return email_pattern.match(email)

def email_in_db(email):
    return email in data

def email_already_verified(email):
    return False


def create_embed(title, description, color, **kwargs):
    return Embed(
        title=title,
        description=description,
        color=color,
        **kwargs
    ).set_footer(text="IITM Bot")