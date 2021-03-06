from redbot.core import commands, checks, Config
import discord
import json

def json_to_embed(data):
        embed = discord.Embed()
        embed.type = "rich"

        if "title" in data.keys():
            embed.title = data["title"]

        if "url" in data.keys():
            embed.url = data["url"]

        if "description" in data.keys():
            embed.description = data["description"]

        if "color" in data.keys():
            embed.colour = data["color"]

        if "author" in data.keys():
            name = "None"
            url = discord.Embed.Empty
            icon_url = discord.Embed.Empty

            if "name" in data["author"].keys():
                name = data["author"]["name"]

            if "url" in data["author"].keys():
                url = data["author"]["url"]

            if "icon_url" in data["author"].keys():
                icon_url = data["author"]["icon_url"]

            embed.set_author(name=name, url=url, icon_url=icon_url)

        if "footer" in data.keys():
            text = discord.Embed.Empty
            icon_url = discord.Embed.Empty

            if "text" in data["footer"].keys():
                text = data["footer"]["text"]

            if "icon_url" in data["footer"].keys():
                icon_url = data["footer"]["icon_url"]

            embed.set_footer(text=text, icon_url=icon_url)

        if "image" in data.keys():
            embed.set_image(url=data["image"])

        if "thumbnail" in data.keys():
            embed.set_image(url=data["thumbnail"])

        if "fields" in data.keys():
            for field in data["fields"]:
                name = "None"
                value = "None"
                inline = True

                if "name" in field:
                    name = field["name"]

                if "value" in field:
                    value = field["value"]

                if "inline" in field:
                    inline = field["inline"]

                embed.add_field(name=name, value=value, inline=inline)

        return embed


class CustomReactions(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, identifier=(3322665 + 3))

        default_guild = {
            "custom_reactions": []
        }

        self.config.register_guild(**default_guild)


    @commands.command()
    @checks.admin_or_permissions(Manage_server=True)
    async def acr(self, ctx, cr_name: str=None, *, cr_value: str=None):
        group = self.config.guild(ctx.guild)
        json_obj = json.loads(cr_value)

        async with group.custom_reactions() as custom_reactions:
            sent = False
            item = None

            try:
                name = cr_name
                embed = json_to_embed(json_obj)

                item = {
                    "name": name,
                    "value": cr_value
                }

                await ctx.send(f"Created reaction {name}, response:", embed=embed)

                sent = True
            except:
                item = None
                await ctx.send("Failed to create the embed, make sure your JSON is valid as well as any URLs.")

            if sent:
                custom_reactions.append(item)
