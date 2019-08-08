from bocadillo import App, configure, Templates

app = App()
templates = Templates()
configure(app)


@app.route("/")
async def home(req, res):
    res.html = await templates.render("index.html")


@app.websocket_route("/echo")
async def echo(ws):
    async for message in ws:
        await ws.send(message)
