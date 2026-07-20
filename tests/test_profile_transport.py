from __future__ import annotations

import json

import httpx

from zapzapapi import ZapZapClient
from zapzapapi.models.profile import UpdateProfileImageRequest, UpdateProfileNameRequest


def test_profile_service_covers_connected_instance_profile_routes() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"ok": True})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)

    assert client.profile.update_image(
        "instance-1",
        UpdateProfileImageRequest(image="https://example.com/logo.jpg"),
    ) == {"ok": True}
    assert client.profile.update_name(
        "instance-1",
        UpdateProfileNameRequest(name="Minha Empresa"),
    ) == {"ok": True}

    assert [(call.method, call.url.path) for call in calls] == [
        ("POST", "/api/v1/instance-1/profile/image"),
        ("POST", "/api/v1/instance-1/profile/name"),
    ]
    assert json.loads(calls[0].read()) == {"image": "https://example.com/logo.jpg"}
    assert json.loads(calls[1].read()) == {"name": "Minha Empresa"}
