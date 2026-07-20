from __future__ import annotations

from zapzapapi.models.chat import (
    ArchiveChatRequest,
    BlockChatRequest,
    ChatSearchOperator,
    DeleteChatRequest,
    DownloadMessageRequest,
    EditMessageRequest,
    FindChatsRequest,
    FindMessagesRequest,
    HistorySyncRequest,
    MarkMessagesReadRequest,
    PresenceRequest,
    PresenceType,
    ReactionMessage,
    RefreshChatNotesRequest,
)
from zapzapapi.models.messages import ReactionMessage as LegacyReactionMessage


def test_chat_action_payload_serializes_booleans_as_api_strings() -> None:
    archive = ArchiveChatRequest(number="5511999999999@s.whatsapp.net", archive=True)
    block = BlockChatRequest(number="5511999999999", block=False)

    assert archive.to_payload() == {
        "number": "5511999999999@s.whatsapp.net",
        "archive": "true",
    }
    assert block.to_payload() == {
        "number": "5511999999999",
        "block": "false",
    }


def test_delete_chat_payload_uses_api_aliases() -> None:
    request = DeleteChatRequest(
        number="5511999999999",
        delete_chat_db=True,
        delete_messages_db=False,
        clear_chat_whatsapp=True,
    )

    assert request.to_payload() == {
        "number": "5511999999999",
        "deleteChatDB": "true",
        "deleteMessagesDB": "false",
        "clearChatWhatsApp": "true",
    }


def test_find_chats_payload_preserves_filter_aliases() -> None:
    request = FindChatsRequest(
        operator=ChatSearchOperator.AND,
        sort="-wa_lastMsgTimestamp",
        limit=25,
        wa_contact_name="Maria",
        wa_is_blocked=False,
        wa_is_group=True,
        lead_is_ticket_open="true",
        lead_assigned_attendant_id="attendant-1",
    )

    assert request.to_payload() == {
        "operator": "AND",
        "sort": "-wa_lastMsgTimestamp",
        "limit": 25,
        "wa_contactName": "Maria",
        "wa_isBlocked": "false",
        "wa_isGroup": "true",
        "lead_isTicketOpen": "true",
        "lead_assignedAttendant_id": "attendant-1",
    }


def test_message_operation_payloads_use_api_aliases() -> None:
    edit = EditMessageRequest(
        message_id="ABCDEF123456",
        number="5511999999999",
        text="Texto corrigido",
    )
    find = FindMessagesRequest(
        chat_id="5511999999999@s.whatsapp.net",
        message_id="ABCDEF123456",
        limit=100,
    )
    history = HistorySyncRequest(
        message_id="3EB01234567890ABCDEF",
        number="5511999999999@s.whatsapp.net",
        count=20,
    )

    assert edit.to_payload() == {
        "id": "ABCDEF123456",
        "number": "5511999999999",
        "text": "Texto corrigido",
    }
    assert find.to_payload() == {
        "chatid": "5511999999999@s.whatsapp.net",
        "id": "ABCDEF123456",
        "limit": 100,
    }
    assert history.to_payload() == {
        "messageid": "3EB01234567890ABCDEF",
        "number": "5511999999999@s.whatsapp.net",
        "count": 20,
    }


def test_download_and_refresh_payloads_serialize_optional_booleans() -> None:
    download = DownloadMessageRequest(
        message_id="7EB0F01D7244B421048F0706368376E0",
        return_link=True,
        return_base64=False,
        generate_mp3=True,
        transcribe=False,
    )
    refresh = RefreshChatNotesRequest(
        number="5511999999999@s.whatsapp.net",
        force=True,
    )

    assert download.to_payload() == {
        "id": "7EB0F01D7244B421048F0706368376E0",
        "return_link": "true",
        "return_base64": "false",
        "generate_mp3": "true",
        "transcribe": "false",
    }
    assert refresh.to_payload() == {
        "number": "5511999999999@s.whatsapp.net",
        "force": "true",
    }


def test_mark_messages_read_payload_preserves_ids_as_json_array() -> None:
    request = MarkMessagesReadRequest(message_ids=["3EB0538DA65A59F6D8A251", "ABCDEF123456"])

    assert request.to_payload() == {"id": ["3EB0538DA65A59F6D8A251", "ABCDEF123456"]}


def test_mark_messages_read_payload_accepts_legacy_raw_string() -> None:
    request = MarkMessagesReadRequest(message_ids='["3EB0538DA65A59F6D8A251"]')

    assert request.to_payload() == {"id": ["3EB0538DA65A59F6D8A251"]}


def test_presence_and_reaction_payloads_use_documented_values() -> None:
    presence = PresenceRequest(
        number="5511999999999",
        presence=PresenceType.COMPOSING,
        delay=3000,
    )
    reaction = ReactionMessage(
        number="5511999999999",
        message_id="5511991515364:2A6E2F02CE4125FDBA1B",
        emoji="ok",
    )

    assert presence.to_payload() == {
        "number": "5511999999999",
        "presence": "composing",
        "delay": 3000,
    }
    assert reaction.to_payload() == {
        "number": "5511999999999",
        "id": "5511991515364:2A6E2F02CE4125FDBA1B",
        "emoji": "ok",
    }


def test_legacy_message_reaction_import_points_to_chat_contract() -> None:
    assert LegacyReactionMessage is ReactionMessage
