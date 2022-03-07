from lib.client import Client
from lib.hcaptcha import hCaptcha
from discord import app_commands, Role
import config
from aiosqlite import connect
from jinja2 import Environment, FileSystemLoader
from discord import app_commands
from sanic import text

client = Client()
hcaptcha = hCaptcha()
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
    
class hcaptchaGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="ward", description="")
        
    @app_commands.command(description="setting")
    @app_commands.descripe(role="Roles to be granted when authentication is successful.")
    async def setup(self, interaction, role: Role):
        async with connect("main.db") as db:
            cursor = await db.execute("SELECT * FROM role")
            if (await cursor.fetchone()) is not None:
                await db.execute("INSERT INTO role VALUES(?)", (role.id,))
            else:
                await db.execute("DELETE FROM role")
                await db.execute("INSERT INTO role VALUES(?)", (role.id,))
        await interaction.response.send_message("setting it!")
    
@client.route("/")
async def main(request):
    return text("404 error")

@client.web.get("/verify")
async def verify(request):
    return await template("verify.html")

@client.web.post("/verify")
async def verify_check(request):
    check = await hcaptcha.siteverify(request.form["h-captcha-response"])
    if check:
        pass
    else:
        pass

client.run(config.token, config.ip, config.port)
