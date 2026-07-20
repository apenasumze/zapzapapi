from __future__ import annotations

import json

import httpx

from zapzapapi import ZapZapClient
from zapzapapi.models.chat import (
    ArchiveChatRequest,
    BlockChatRequest,
    ChatNotesRequest,
    DeleteChatRequest,
    DeleteMessageRequest,
    DownloadMessageRequest,
    EditChatNotesRequest,
    EditMessageRequest,
    FindChatsRequest,
    FindMessagesRequest,
    HistorySyncRequest,
    MarkMessagesReadRequest,
    MuteChatRequest,
    PinChatRequest,
    PresenceRequest,
    PresenceType,
    ReactionMessage,
    ReadChatRequest,
    RefreshChatNotesRequest,
)


def test_chats_service_covers_conversation_routes() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"ok": True})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)

    assert client.chats.find("instance-1", FindChatsRequest(limit=10)) == {"ok": True}
    assert client.chats.read("instance-1", ReadChatRequest(number="5511999999999")) == {"ok": True}
    assert client.chats.archive(
        "instance-1",
        ArchiveChatRequest(number="5511999999999@s.whatsapp.net", archive=True),
    ) == {"ok": True}
    assert client.chats.pin(
        "instance-1",
        PinChatRequest(number="5511999999999@s.whatsapp.net", pin=False),
    ) == {"ok": True}
    assert client.chats.mute(
        "instance-1",
        MuteChatRequest(number="5511999999999@s.whatsapp.net", duration=86400000),
    ) == {"ok": True}
    assert client.chats.block(
        "instance-1",
        BlockChatRequest(number="5511999999999", block=True),
    ) == {"ok": True}
    assert client.chats.blocklist("instance-1") == {"ok": True}
    assert client.chats.delete(
        "instance-1",
        DeleteChatRequest(number="5511999999999", delete_chat_db=True),
    ) == {"ok": True}
    assert client.chats.notes(
        "instance-1",
        ChatNotesRequest(number="5511999999999@s.whatsapp.net"),
    ) == {"ok": True}
    assert client.chats.edit_notes(
        "instance-1",
        EditChatNotesRequest(
            number="5511999999999@s.whatsapp.net",
            notes="Cliente prefere contato a tarde",
        ),
    ) == {"ok": True}
    assert client.chats.refresh_notes(
        "instance-1",
        RefreshChatNotesRequest(number="5511999999999@s.whatsapp.net", force=False),
    ) == {"ok": True}

    assert len(calls) == 11
    assert [(call.method, call.url.path) for call in calls] == [
        ("POST", "/api/v1/instance-1/chat/find"),
        ("POST", "/api/v1/instance-1/chat/read"),
        ("POST", "/api/v1/instance-1/chat/archive"),
        ("POST", "/api/v1/instance-1/chat/pin"),
        ("POST", "/api/v1/instance-1/chat/mute"),
        ("POST", "/api/v1/instance-1/chat/block"),
        ("GET", "/api/v1/instance-1/chat/blocklist"),
        ("POST", "/api/v1/instance-1/chat/delete"),
        ("POST", "/api/v1/instance-1/chat/notes"),
        ("POST", "/api/v1/instance-1/chat/notes/edit"),
        ("POST", "/api/v1/instance-1/chat/notes/refresh"),
    ]
    assert json.loads(calls[2].read()) == {
        "number": "5511999999999@s.whatsapp.net",
        "archive": "true",
    }
    assert json.loads(calls[7].read()) == {
        "number": "5511999999999",
        "deleteChatDB": "true",
    }


def test_chats_service_covers_existing_message_routes() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"ok": True})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)

    assert client.chats.find_messages(
        "instance-1",
        FindMessagesRequest(chat_id="5511999999999@s.whatsapp.net", limit=100),
    ) == {"ok": True}
    assert client.chats.edit_message(
        "instance-1",
        EditMessageRequest(message_id="ABCDEF123456", number="5511999999999", text="Corrigido"),
    ) == {"ok": True}
    assert client.chats.delete_message(
        "instance-1",
        DeleteMessageRequest(message_id="ABCDEF123456", number="5511999999999"),
    ) == {"ok": True}
    assert client.chats.download_message(
        "instance-1",
        DownloadMessageRequest(message_id="7EB0F01D7244B421048F0706368376E0", return_link=True),
    ) == {"ok": True}
    assert client.chats.mark_messages_read(
        "instance-1",
        MarkMessagesReadRequest(message_ids=["3EB0538DA65A59F6D8A251"]),
    ) == {"ok": True}
    assert client.chats.presence(
        "instance-1",
        PresenceRequest(number="5511999999999", presence=PresenceType.COMPOSING, delay=3000),
    ) == {"ok": True}
    assert client.chats.history_sync(
        "instance-1",
        HistorySyncRequest(message_id="3EB01234567890ABCDEF", count=20),
    ) == {"ok": True}
    assert client.chats.react_message(
        "instance-1",
        ReactionMessage(
            number="5511999999999",
            message_id="5511991515364:2A6E2F02CE4125FDBA1B",
            emoji="ok",
        ),
    ) == {"ok": True}

    assert len(calls) == 8
    assert [(call.method, call.url.path) for call in calls] == [
        ("POST", "/api/v1/instance-1/message/find"),
        ("POST", "/api/v1/instance-1/message/edit"),
        ("POST", "/api/v1/instance-1/message/delete"),
        ("POST", "/api/v1/instance-1/message/download"),
        ("POST", "/api/v1/instance-1/message/markread"),
        ("POST", "/api/v1/instance-1/message/presence"),
        ("POST", "/api/v1/instance-1/message/history-sync"),
        ("POST", "/api/v1/instance-1/message/react"),
    ]
    assert json.loads(calls[0].read()) == {
        "chatid": "5511999999999@s.whatsapp.net",
        "limit": 100,
    }
    assert json.loads(calls[4].read()) == {"id": ["3EB0538DA65A59F6D8A251"]}
    assert json.loads(calls[7].read()) == {
        "number": "5511999999999",
        "id": "5511991515364:2A6E2F02CE4125FDBA1B",
        "emoji": "ok",
    }
