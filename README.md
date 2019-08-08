# ws-test

Example application to debug `1006` connection closure issues when running the code from the [Bocadillo tutorial](https://bocadilloproject.github.io/guide/tutorial.html#trying-out-the-websocket-endpoint).

## Usage

Start the server:

```bash
uvicorn app:app --log-level=debug
# OR, if you have Heroku CLI:
heroku local
```

Two clients are available:

- `asyncio` + `websockets`:

  - Start the client:

  ```
  python -m clients.asyncio ws://localhost:8000/echo
  ```

  - To send messages, type them in the REPL and hit `Enter`. **Note**: the blocking call to `input()` is what is causing the connection to shutdown after the server's ping timeout expires (because the client rarely gets a chance to manage connection keep alive, i.e. pings and pongs).

- `trio` + `trio-websocket`:

  - Create a `messages` file: `touch messages`.
  - Start the client:

  ```
  python -m clients.trio ws://localhost:8000/echo
  ```

  - To send messages:

  ```bash
  echo "Hello" >> messages
  ```

  - Messages are read _asynchronously_ from the file, so the WebSocket client can send and receive pings and pongs as designed, and the connection stays open.
