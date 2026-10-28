"""Small ASGI security middleware for bounded request bodies."""

import json
import threading
import time
from collections import deque
from typing import Any


class RequestBodyLimitMiddleware:
    """Reject oversized HTTP request bodies before handing them to FastAPI."""

    def __init__(self, app: Any, max_body_bytes: int = 65_536) -> None:
        self.app = app
        self.max_body_bytes = max_body_bytes

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        content_length = headers.get(b"content-length")
        if content_length is not None:
            try:
                declared_length = int(content_length)
            except ValueError:
                declared_length = -1
            if declared_length > self.max_body_bytes:
                await self._reject(send)
                return

        body = bytearray()
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            if message["type"] != "http.request":
                continue
            body.extend(message.get("body", b""))
            if len(body) > self.max_body_bytes:
                await self._reject(send)
                return
            if not message.get("more_body", False):
                break

        body_bytes = bytes(body)
        replayed = False

        async def replay_receive() -> dict[str, Any]:
            nonlocal replayed
            if not replayed:
                replayed = True
                return {
                    "type": "http.request",
                    "body": body_bytes,
                    "more_body": False,
                }
            return await receive()

        await self.app(scope, replay_receive, send)

    async def _reject(self, send: Any) -> None:
        payload = json.dumps({"detail": "Request body too large"}).encode("utf-8")
        await send({
            "type": "http.response.start",
            "status": 413,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(payload)).encode("ascii")),
                (b"cache-control", b"no-store"),
            ],
        })
        await send({
            "type": "http.response.body",
            "body": payload,
            "more_body": False,
        })



class InMemoryRateLimiter:
    """Process-local sliding-window limiter; use an edge proxy for public deployments."""

    def __init__(self, window_seconds: int = 60, max_clients: int = 10_000) -> None:
        self.window_seconds = window_seconds
        self.max_clients = max_clients
        self._events: dict[str, deque[float]] = {}
        self._lock = threading.Lock()

    def check(self, client_key: str, limit: int) -> int | None:
        """Return retry-after seconds when blocked, otherwise None."""
        now = time.monotonic()
        cutoff = now - self.window_seconds
        with self._lock:
            for key in list(self._events):
                events = self._events[key]
                while events and events[0] <= cutoff:
                    events.popleft()
                if not events:
                    del self._events[key]

            events = self._events.get(client_key)
            if events is None:
                if len(self._events) >= self.max_clients:
                    return self.window_seconds
                events = deque()
                self._events[client_key] = events

            if len(events) >= limit:
                return max(1, int(events[0] + self.window_seconds - now + 0.999))

            events.append(now)
            return None

    def reset(self) -> None:
        """Clear limiter state; intended for deterministic tests and controlled restarts."""
        with self._lock:
            self._events.clear()
