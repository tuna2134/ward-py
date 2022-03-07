from lib.client import Client
import config
from discord import app_commands
from sanic import text

client = Client()

@client.event
async def on_ready():
    print("Ready!")
    
@client.route("/")
async def main(request):
    return text("404 error")

client.run(config.token, config.ip, config.port)
