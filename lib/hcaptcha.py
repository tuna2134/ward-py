from aiohttp import ClientSession

class hCaptcha:
    def __init__(self, secret, loop):
        self.secret = secret
        self.session = ClientSession(loop=loop)
        
    async def siteverify(self, token):
        async with self.session.post("https://hcaptcha.com/siteverify",
                                     data={"secret": self.secret, "response": token}) as r:
            data = await r.json()
        return data["success"]
