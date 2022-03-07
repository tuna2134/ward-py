from lib.client import Client
from lib.hcaptcha import hCaptcha
import config
from discord import app_commands
from sanic import text

client = Client()
hcaptcha = hCaptcha()

@client.event
async def on_ready():
    print("Ready!")
    
@client.route("/")
async def main(request):
    return text("404 error")

@client.web.get("/verify")
async def verify(request):
    pass

@client.web.post("/verify")
async def verify_check(request):
    check = await hcaptcha.verify(request.form["h-captcha-response"])
    if check:
        pass
    else:
        pass

client.run(config.token, config.ip, config.port)
