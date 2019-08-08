from bocadillo import App, configure

app = App()
configure(app)


@app.websocket_route("/echo")
async def echo(ws):
    async for message in ws:
        await ws.send(message)
