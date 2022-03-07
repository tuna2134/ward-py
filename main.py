from lib.client import Client
from lib.hcaptcha import hCaptcha
import config
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
