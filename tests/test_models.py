from __future__ import annotations

from zapzapapi.models.message import (
    FontType,
    MediaMessage,
    MediaType,
    PixButtonMessage,
    StatusMessage,
    StatusType,
    TextMessage,
)


def test_text_message_payload_uses_api_aliases() -> None:
    message = TextMessage(number="5511999999999", text="Ola", reply_id="msg_1")

    assert message.to_payload() == {
        "number": "5511999999999",
        "text": "Ola",
        "replyid": "msg_1",
    }


def test_text_message_payload_preserves_explicit_delay() -> None:
    message = TextMessage(number="5511999999999", text="Ola", delay=1200)

    assert message.to_payload() == {
        "number": "5511999999999",
        "delay": 1200,
        "text": "Ola",
    }


def test_pix_button_payload_preserves_reserved_async_alias() -> None:
    message = PixButtonMessage(
        number="5511999999999",
        pix_type="cpf",
        pix_key="12345678900",
        async_=True,
        track_id="externo-1",
    )

    assert message.to_payload() == {
        "number": "5511999999999",
        "pixType": "cpf",
        "pixKey": "12345678900",
        "async": True,
        "track_id": "externo-1",
    }


def test_media_message_accepts_documented_media_type_values() -> None:
    message = MediaMessage(
        number="5511999999999",
        type=MediaType.PTT,
        file="https://example.com/audio.ogg",
    )

    assert message.to_payload() == {
        "number": "5511999999999",
        "type": "ptt",
        "file": "https://example.com/audio.ogg",
    }


def test_status_message_accepts_documented_ptt_and_font_values() -> None:
    message = StatusMessage(
        type=StatusType.PTT,
        file="https://example.com/audio.ogg",
        font=FontType.FONT_8,
    )

    assert message.to_payload() == {
        "type": "ptt",
        "file": "https://example.com/audio.ogg",
        "font": "8",
    }
