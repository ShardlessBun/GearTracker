from discord import Embed, Color


class ErrorEmbed(Embed):

    def __init__(self, *args, **kwargs):
        kwargs['title'] = f"Error: {kwargs.get('title')}"
        kwargs['color'] = Color.brand_red()
        super().__init__(**kwargs)
