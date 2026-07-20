from __future__ import annotations

import json

import httpx

from zapzapapi import ZapZapClient
from zapzapapi.models.contacts import (
    AddContactRequest,
    CheckNumbersRequest,
    ContactDetailsRequest,
    ListContactsRequest,
    RemoveContactRequest,
)


def test_contacts_service_covers_contact_and_lookup_routes() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"ok": True})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)

    assert client.contacts.check_numbers(
        "instance-1",
        CheckNumbersRequest(numbers=["5511999999999", "5521888888888"]),
    ) == {"ok": True}
    assert client.contacts.details(
        "instance-1",
        ContactDetailsRequest(number="5511999999999", preview=False),
    ) == {"ok": True}
    assert client.contacts.add(
        "instance-1",
        AddContactRequest(phone="5511999999999", name="Joao Silva"),
    ) == {"ok": True}
    assert client.contacts.remove(
        "instance-1",
        RemoveContactRequest(number="5511999999999"),
    ) == {"ok": True}
    assert client.contacts.list_fast("instance-1") == {"ok": True}
    assert client.contacts.list(
        "instance-1",
        ListContactsRequest(limit=50, offset=0),
    ) == {"ok": True}

    assert [(call.method, call.url.path) for call in calls] == [
        ("POST", "/api/v1/instance-1/chat/check"),
        ("POST", "/api/v1/instance-1/chat/details"),
        ("POST", "/api/v1/instance-1/contact/add"),
        ("POST", "/api/v1/instance-1/contact/remove"),
        ("GET", "/api/v1/instance-1/contacts"),
        ("POST", "/api/v1/instance-1/contacts/list"),
    ]
    assert json.loads(calls[0].read()) == {
        "numbers": ["5511999999999", "5521888888888"],
    }
    assert json.loads(calls[1].read()) == {
        "number": "5511999999999",
        "preview": "false",
    }
    assert json.loads(calls[5].read()) == {"limit": 50, "offset": 0}
