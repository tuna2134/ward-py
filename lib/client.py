from discord import Client, app_commands
from sanic import Sanic

class Client(Client):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self.web = Sanic("web")
        self.route = self.web.route
        self.web.register_listener(self.process_start, "main_process_start")
        
    async def process_start(self, app, loop):
        super().__init__(*self._args, **self._kwargs)
        loop.create_task(self.run(self.token))
        await self.wait_until_ready()
    
    def run(self, token, *args, **kwargs):
        self.token = token
        self.web.run(*args, **kwargs)
