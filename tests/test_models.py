from __future__ import annotations

from zapzapapi.models.instance import (
    ConfigureInstanceWebhookRequest,
    CreateInstanceRequest,
    InstanceWebhookEvent,
    InstanceWebhookExclude,
    TestInstanceWebhookRequest,
    UpdateInstanceRequest,
)
from zapzapapi.models.message import (
    Button,
    ButtonsMessage,
    CarouselCard,
    CarouselMessage,
    ContactMessage,
    FontType,
    ListMessage,
    MediaMessage,
    MediaType,
    PixButtonMessage,
    PixType,
    PollMessage,
    ReactionMessage,
    StatusBackgroundColor,
    StatusMessage,
    StatusType,
    TextMessage,
)


def test_create_instance_payload_uses_contract_aliases_and_metadata_json() -> None:
    request = CreateInstanceRequest(
        name="minha-instancia",
        system_name="Meu App",
        metadata={"plan": "pro", "clientId": "123"},
    )

    assert request.to_payload() == {
        "name": "minha-instancia",
        "systemName": "Meu App",
        "metadata": '{"clientId":"123","plan":"pro"}',
    }


def test_update_instance_payload_uses_webhook_url_and_metadata() -> None:
    request = UpdateInstanceRequest(
        webhook_url="https://example.com/webhook",
        metadata='{"clientId":"123"}',
    )

    assert request.to_payload() == {
        "webhook_url": "https://example.com/webhook",
        "metadata": '{"clientId":"123"}',
    }


def test_configure_instance_webhook_payload_serializes_event_and_exclude_enums() -> None:
    request = ConfigureInstanceWebhookRequest(
        webhook_url="https://example.com/webhook",
        events=[InstanceWebhookEvent.MESSAGES, InstanceWebhookEvent.MESSAGES_UPDATE],
        exclude_messages=[
            InstanceWebhookExclude.WAS_SENT_BY_API,
            InstanceWebhookExclude.IS_GROUP_YES,
        ],
    )

    assert request.to_payload() == {
        "webhook_url": "https://example.com/webhook",
        "events": "messages,messages_update",
        "excludeMessages": "wasSentByApi,isGroupYes",
    }


def test_configure_instance_webhook_payload_accepts_raw_strings() -> None:
    request = ConfigureInstanceWebhookRequest(
        webhook_url="https://example.com/webhook",
        events="messages,status",
        exclude_messages="fromMeYes,fromMeNo",
    )

    assert request.to_payload() == {
        "webhook_url": "https://example.com/webhook",
        "events": "messages,status",
        "excludeMessages": "fromMeYes,fromMeNo",
    }


def test_test_instance_webhook_payload_accepts_optional_url() -> None:
    request = TestInstanceWebhookRequest(url="https://example.com/test-webhook")

    assert request.to_payload() == {"url": "https://example.com/test-webhook"}


def test_text_message_payload_uses_api_aliases_and_default_delay() -> None:
    message = TextMessage(number="5511999999999", text="Ola", reply_id="msg_1")

    assert message.to_payload() == {
        "number": "5511999999999",
        "delay": 1000,
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


def test_contact_message_separates_recipient_number_from_contact_phone_number() -> None:
    message = ContactMessage(
        number="5511999999999",
        full_name="Joao Silva",
        phone_number="5511888888888",
    )

    assert message.to_payload() == {
        "number": "5511999999999",
        "delay": 1000,
        "fullName": "Joao Silva",
        "phoneNumber": "5511888888888",
    }


def test_pix_button_payload_preserves_reserved_async_alias_and_pix_enum() -> None:
    message = PixButtonMessage(
        number="5511999999999",
        pix_type=PixType.CPF,
        pix_key="12345678900",
        async_=True,
        track_id="externo-1",
    )

    assert message.to_payload() == {
        "number": "5511999999999",
        "delay": 1000,
        "pixType": "CPF",
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
        "delay": 1000,
        "type": "ptt",
        "file": "https://example.com/audio.ogg",
    }


def test_reaction_message_payload_uses_api_message_id_alias() -> None:
    message = ReactionMessage(
        number="5511999999999",
        message_id="5511991515364:2A6E2F02CE4125FDBA1B",
        emoji="\U0001f44d",
    )

    assert message.to_payload() == {
        "number": "5511999999999",
        "id": "5511991515364:2A6E2F02CE4125FDBA1B",
        "emoji": "\U0001f44d",
    }


def test_buttons_message_serializes_typed_buttons_to_json_string() -> None:
    message = ButtonsMessage(
        number="5511999999999",
        text="Como podemos ajudar?",
        buttons=[
            Button(text="Sim", id="yes"),
            Button(text="Site", url="https://example.com"),
            Button(text="Copiar", copy_code="ABC123"),
        ],
    )

    assert message.to_payload() == {
        "number": "5511999999999",
        "delay": 1000,
        "text": "Como podemos ajudar?",
        "buttons": (
            '[{"text":"Sim","id":"yes"},'
            '{"text":"Site","url":"https://example.com"},'
            '{"text":"Copiar","copy":"ABC123"}]'
        ),
    }


def test_list_and_poll_messages_serialize_choices_to_json_string() -> None:
    list_message = ListMessage(
        number="5511999999999",
        text="Escolha uma opcao:",
        choices=["[Produtos]", "Camiseta|p1|R$ 50"],
    )
    poll_message = PollMessage(
        number="5511999999999",
        text="Qual o melhor dia?",
        choices=["Segunda", "Terca"],
        selectable_count=1,
    )

    assert list_message.to_payload()["choices"] == '["[Produtos]","Camiseta|p1|R$ 50"]'
    assert poll_message.to_payload()["choices"] == '["Segunda","Terca"]'
    assert poll_message.to_payload()["selectableCount"] == "1"
    assert "delay" not in list_message.to_payload()
    assert "delay" not in poll_message.to_payload()


def test_carousel_message_serializes_cards_to_json_string() -> None:
    message = CarouselMessage(
        number="5511999999999",
        text="Confira nossas opcoes:",
        carousel=[
            CarouselCard(
                text="Produto 1",
                image="https://example.com/img.jpg",
                buttons=[Button(type="REPLY", text="Quero", id="quero")],
            )
        ],
    )

    assert message.to_payload()["carousel"] == (
        '[{"text":"Produto 1","image":"https://example.com/img.jpg",'
        '"buttons":[{"type":"REPLY","text":"Quero","id":"quero"}]}]'
    )


def test_status_message_accepts_documented_ptt_font_and_background_values() -> None:
    message = StatusMessage(
        type=StatusType.PTT,
        file="https://example.com/audio.ogg",
        font=FontType.SANS_SERIF,
        background_color=StatusBackgroundColor.CINZA_ESCURO,
    )

    assert message.to_payload() == {
        "type": "ptt",
        "file": "https://example.com/audio.ogg",
        "font": "0",
        "background_color": "19",
    }
