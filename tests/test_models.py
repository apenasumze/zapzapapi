from __future__ import annotations

import pytest

from zapzapapi.models.instance import (
    ConfigureInstanceWebhookRequest,
    CreateInstanceRequest,
    InstanceWebhookEvent,
    InstanceWebhookExclude,
    TestInstanceWebhookRequest,
    UpdateInstanceRequest,
)
from zapzapapi.models.messages import (
    Button,
    ButtonsMessage,
    CarouselButton,
    CarouselButtonType,
    CarouselCard,
    CarouselMessage,
    ContactMessage,
    FontType,
    ListChoice,
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


def test_buttons_message_preserves_buttons_as_json_array() -> None:
    message = ButtonsMessage(
        number="5511999999999",
        text="Como podemos ajudar?",
        buttons=[
            Button.reply(text="Sim", id="yes"),
            Button.link(text="Site", url="https://example.com"),
            Button.copy_text(text="Copiar", copy_code="ABC123"),
        ],
    )

    assert message.to_payload() == {
        "number": "5511999999999",
        "delay": 1000,
        "text": "Como podemos ajudar?",
        "buttons": [
            {"text": "Sim", "id": "yes"},
            {"text": "Site", "url": "https://example.com"},
            {"text": "Copiar", "copy": "ABC123"},
        ],
    }


def test_buttons_message_accepts_legacy_raw_string() -> None:
    message = ButtonsMessage(
        number="5511999999999",
        text="Como podemos ajudar?",
        buttons=(
            '[{"text":"Sim","id":"yes"},'
            '{"text":"Site","url":"https://example.com"},'
            '{"text":"Copiar","copy":"ABC123"}]'
        ),
    )

    assert message.to_payload()["buttons"] == [
        {"text": "Sim", "id": "yes"},
        {"text": "Site", "url": "https://example.com"},
        {"text": "Copiar", "copy": "ABC123"},
    ]


def test_button_factories_create_confirmed_button_payloads() -> None:
    assert Button.reply(text="Sim", id="yes").to_payload() == {
        "text": "Sim",
        "id": "yes",
    }
    assert Button.link(text="Site", url="https://example.com").to_payload() == {
        "text": "Site",
        "url": "https://example.com",
    }
    assert Button.call(text="Ligar", phone="+5511999999999").to_payload() == {
        "text": "Ligar",
        "phone": "+5511999999999",
    }
    assert Button.copy_text(text="Copiar", copy_code="ABC123").to_payload() == {
        "text": "Copiar",
        "copy": "ABC123",
    }


def test_button_requires_exactly_one_action() -> None:
    with pytest.raises(ValueError, match="exactly one action"):
        Button(text="Sem acao")

    with pytest.raises(ValueError, match="exactly one action"):
        Button(text="Misturado", id="yes", url="https://example.com")


def test_buttons_message_accepts_up_to_three_buttons() -> None:
    with pytest.raises(ValueError, match="up to 3 buttons"):
        ButtonsMessage(
            number="5511999999999",
            text="Como podemos ajudar?",
            buttons=[
                Button.reply(text="Opcao 1", id="1"),
                Button.reply(text="Opcao 2", id="2"),
                Button.reply(text="Opcao 3", id="3"),
                Button.reply(text="Opcao 4", id="4"),
            ],
        )


def test_list_message_serializes_category_and_list_choices_as_json_array() -> None:
    list_message = ListMessage(
        number="5511999999999",
        text="Escolha uma opcao:",
        category="Produtos",
        choices=[
            ListChoice(item="Camiseta", id="p1", description="R$ 50"),
            ListChoice(item="Calca", id="p2", description="R$ 120"),
        ],
        list_button="Opcoes",
        footer_text="Gostou?",
    )

    assert list_message.to_payload() == {
        "number": "5511999999999",
        "text": "Escolha uma opcao:",
        "choices": ["[Produtos]", "Camiseta|p1|R$ 50", "Calca|p2|R$ 120"],
        "listButton": "Opcoes",
        "footerText": "Gostou?",
    }


def test_list_choice_accepts_only_required_item() -> None:
    message = ListMessage(
        number="5511999999999",
        text="Escolha uma opcao:",
        category="Produtos",
        choices=[
            ListChoice(item="Camiseta"),
            ListChoice(item="Calca", description="R$ 120"),
            ListChoice(item="Tenis", id="p3"),
        ],
    )

    assert message.to_payload()["choices"] == [
        "[Produtos]",
        "Camiseta",
        "Calca||R$ 120",
        "Tenis|p3",
    ]


def test_list_message_accepts_legacy_string_choices() -> None:
    message = ListMessage(
        number="5511999999999",
        text="Escolha uma opcao:",
        choices='["[Produtos]","Camiseta|p1|R$ 50"]',
    )

    assert message.to_payload()["choices"] == ["[Produtos]", "Camiseta|p1|R$ 50"]


def test_poll_message_serializes_choices_to_json_string() -> None:
    poll_message = PollMessage(
        number="5511999999999",
        text="Qual o melhor dia?",
        choices=["Segunda", "Terca"],
        selectable_count=1,
    )

    assert poll_message.to_payload()["choices"] == '["Segunda","Terca"]'
    assert poll_message.to_payload()["selectableCount"] == "1"
    assert "delay" not in poll_message.to_payload()


def test_carousel_message_preserves_cards_as_json_array() -> None:
    message = CarouselMessage(
        number="5511999999999",
        text="Confira nossas opcoes:",
        carousel=[
            CarouselCard(
                text="Produto 1",
                image="https://example.com/img.jpg",
                buttons=[CarouselButton(text="Quero", id="quero")],
            )
        ],
    )

    assert message.to_payload()["carousel"] == [
        {
            "text": "Produto 1",
            "image": "https://example.com/img.jpg",
            "buttons": [{"type": "REPLY", "text": "Quero", "id": "quero"}],
        }
    ]


def test_carousel_button_uses_confirmed_reply_type() -> None:
    button = CarouselButton(text="Quero", id="quero", type=CarouselButtonType.REPLY)

    assert button.to_payload() == {
        "text": "Quero",
        "id": "quero",
        "type": "REPLY",
    }


def test_carousel_message_accepts_legacy_raw_string() -> None:
    message = CarouselMessage(
        number="5511999999999",
        text="Confira nossas opcoes:",
        carousel=(
            '[{"text":"Produto 1","image":"https://example.com/img.jpg",'
            '"buttons":[{"type":"REPLY","text":"Quero","id":"quero"}]}]'
        ),
    )

    assert message.to_payload()["carousel"] == [
        {
            "text": "Produto 1",
            "image": "https://example.com/img.jpg",
            "buttons": [{"type": "REPLY", "text": "Quero", "id": "quero"}],
        }
    ]


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
