from discord import Embed

def create_embed(title, description, color, **kwargs):
    return Embed(
        title=title,
        description=description,
        color=color,
        **kwargs
    )
