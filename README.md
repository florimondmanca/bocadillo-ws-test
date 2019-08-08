# ws-test

Example application to debug unexpected connection closures when running the code from the [Bocadillo tutorial](https://bocadilloproject.github.io/guide/tutorial.html#trying-out-the-websocket-endpoint).

## Usage

Start the server:

```bash
uvicorn app:app --log-level=debug
# OR, if you have Heroku CLI:
heroku local
```

Three clients are available:

- `asyncio` + `websockets`:

  - Start the client:

  ```
  python -m clients.asyncio ws://localhost:8000/echo
  ```

  - To send messages, type them in the REPL and hit `Enter`.

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

- A browser-based JavaScript client: open your browser at http://localhost:8000.

## Rationale

The client code in the `asyncio` + `websockets` client is using `input()` to get user input. This is a **blocking** call, which results in other tasks running on the event loop from running. In particular, this prevents the client from exchanging `ping` and `pong` messages with the server. After a while, either the server or the client time out waiting for a `pong`, and the connection is shut down.

Key learning point here: **don't block the event loop**. Make sure all I/O is asynchronous. This isn't always easy, especially when reading from files or stdin. Alternatives to `asyncio` such as `trio` have more tools built-in to help you achieve full-async I/O handling.
