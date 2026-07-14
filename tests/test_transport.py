from __future__ import annotations

import json

import httpx
import pytest

from zapzapapi import ZapZapAuthenticationError, ZapZapClient, ZapZapValidationError
from zapzapapi.models.message import TextMessage


def test_transport_sends_single_request_with_auth_headers() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"status": "sent", "id": "msg_1"})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)

    response = client.messages.send_text(
        "instance-1",
        TextMessage(number="5511999999999", text="Olá", reply_id="msg_0"),
    )

    assert response == {"status": "sent", "id": "msg_1"}
    assert len(calls) == 1
    assert calls[0].method == "POST"
    assert str(calls[0].url) == "https://app.zapzapapi.com/api/v1/instance-1/send/text"
    assert calls[0].headers["x-api-key"] == "key"
    assert calls[0].headers["x-api-secret"] == "secret"
    assert json.loads(calls[0].read()) == {
        "number": "5511999999999",
        "delay": 1000,
        "replyid": "msg_0",
        "text": "Olá",
    }


def test_transport_raises_typed_authentication_error_without_retry() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(401, json={"message": "invalid credentials"})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)

    with pytest.raises(ZapZapAuthenticationError) as exc_info:
        client.account.get()

    assert calls == 1
    assert exc_info.value.status_code == 401
    assert exc_info.value.response_body == {"message": "invalid credentials"}


def test_transport_raises_validation_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(422, json={"message": "number is required"})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)

    with pytest.raises(ZapZapValidationError):
        client.messages.send_text("instance-1", TextMessage(number="5511999999999", text="Olá"))
