from __future__ import annotations

from zapzapapi.models.message import PixButtonMessage, TextMessage


def test_text_message_payload_uses_api_aliases() -> None:
    message = TextMessage(number="5511999999999", text="Olá", reply_id="msg_1")

    assert message.to_payload() == {
        "number": "5511999999999",
        "delay": 1000,
        "text": "Olá",
        "replyid": "msg_1",
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
        "delay": 1000,
        "pixType": "cpf",
        "pixKey": "12345678900",
        "async": True,
        "track_id": "externo-1",
    }
