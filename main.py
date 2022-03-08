from lib.client import Client
from lib.hcaptcha import hCaptcha
from discord import app_commands, Role
import discord
import config
from aiosqlite import connect
from jinja2 import Environment, FileSystemLoader
from discord import app_commands
from sanic import text
import random, string

client = Client()
hcaptcha = hCaptcha(config.secretkey)
env = Environment(
    loader=FileSystemLoader("./html"),
    enable_async=True
)

async def template(filename, *args, **kwargs):
    content = await env.get_template(filename).render_async(kwargs)
    return html(content)

@client.event
async def on_ready():
    print("Ready!")
    
def randomname(self, n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)
    
@client.event
async def on_interaction(interaction):
    if interaction.type != discord.InteractionType.component:
        return
    data = interaction.data
    if data["custom_id"] == "captcha_start_button":
        async with connect("main.db") as db:
            name = randomname(10)
            await db.execute("INSERT INTO url VALUES(?, ?)", (name, interaction.user.id))
            await interaction.response.send_message(f"{config.url}/verify/{name}", ephemeral=True)
    
class hcaptchaGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="ward", description="")
        
    @app_commands.command(description="setting a bot")
    @app_commands.describe(role="Roles to be granted when authentication is successful.")
    async def setting(self, interaction, role: Role):
        async with connect("main.db") as db:
            cursor = await db.execute("SELECT * FROM role")
            if (await cursor.fetchone()) is not None:
                await db.execute("INSERT INTO role VALUES(?)", (role.id,))
            else:
                await db.execute("DELETE FROM role")
                await db.execute("INSERT INTO role VALUES(?)", (role.id,))
        await interaction.response.send_message("setting it!")
        
    @app_commands.command(description="Send the panel necessary for authentication.")
    @app_commands.describe(channel="Please specify the channel you want to send the panel.")
    async def send(self, interaction, channel: discord.TextChannel):
        embed = discord.Embed(title="Captcha Panel", description="please click a button")
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="click!", custom_id="captcha_start_button"))
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message("send a panel!")
    
@client.route("/")
async def main(request):
    return text("404 error")

@client.web.get("/verify/<name>")
async def verify(request, name):
    async with connect("main.db") as db:
        cursor = await db.execute("SELECT * FROM url WHERE name=?", (name,))
        if (await cursor.fetchone()):
            return await template("verify.html", sitekey=config.sitekey)
        else:
            return text("invalid url")

@client.web.post("/verify/<name>")
async def verify_check(request):
    async with connect("main.db") as db:
        cursor = await db.execute("SELECT * FROM url WHERE name=?", (name,))
        if (await cursor.fetchone()):
            check = await hcaptcha.siteverify(request.form["h-captcha-response"])
            if check:
                pass
            else:
                return await template("verify.html", sitekey=config.sitekey)
        else:
            return text("invalid url")

client.run(config.token, config.ip, config.port)
