from __future__ import annotations

import json

import httpx
import pytest

from zapzapapi import ZapZapAuthenticationError, ZapZapClient, ZapZapValidationError
from zapzapapi.models.account import AccountResponse
from zapzapapi.models.instance import (
    ConfigureInstanceWebhookRequest,
    ConfigureInstanceWebhookResponse,
    CreateInstanceRequest,
    CreateInstanceResponse,
    DeleteInstanceResponse,
    InstanceCreationCostResponse,
    InstanceQRCodeDetails,
    InstanceQRCodeResponse,
    InstanceResponse,
    InstanceWebhookEvent,
    InstanceWebhookExclude,
    InstanceWebhookResponse,
    TestInstanceWebhookRequest,
    TestInstanceWebhookResponse,
    UpdateInstanceRequest,
)
from zapzapapi.models.messages import (
    Button,
    ButtonsMessage,
    CarouselButton,
    CarouselCard,
    CarouselMessage,
    ListChoice,
    ListMessage,
    ReactionMessage,
    TextMessage,
)


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


def test_transport_sends_reaction_to_message_react_endpoint() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"messageType": "ReactionMessage", "status": "Pending"})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)

    response = client.messages.send_reaction(
        "instance-1",
        ReactionMessage(
            number="5511999999999",
            message_id="5511991515364:2A6E2F02CE4125FDBA1B",
            emoji="\U0001f44d",
        ),
    )

    assert response == {"messageType": "ReactionMessage", "status": "Pending"}
    assert len(calls) == 1
    assert calls[0].method == "POST"
    assert str(calls[0].url) == "https://app.zapzapapi.com/api/v1/instance-1/message/react"
    assert json.loads(calls[0].read()) == {
        "number": "5511999999999",
        "id": "5511991515364:2A6E2F02CE4125FDBA1B",
        "emoji": "\U0001f44d",
    }


def test_transport_sends_buttons_as_json_array() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"messageType": "NativeFlowMessage", "status": "Pending"})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)

    response = client.messages.send_buttons(
        "instance-1",
        ButtonsMessage(
            number="5511999999999",
            text="Escolha:",
            buttons=[
                Button.reply(text="Sim", id="yes"),
                Button.link(text="Site do Google", url="https://google.com"),
                Button.copy_text(text="Ligar", copy_code="+5511999999999"),
            ],
            image="https://picsum.photos/seed/zapzap-buttons/900/500",
        ),
    )

    assert response == {"messageType": "NativeFlowMessage", "status": "Pending"}
    assert len(calls) == 1
    assert calls[0].method == "POST"
    assert calls[0].url.path == "/api/v1/instance-1/send/buttons"
    assert json.loads(calls[0].read()) == {
        "number": "5511999999999",
        "delay": 1000,
        "text": "Escolha:",
        "buttons": [
            {"text": "Sim", "id": "yes"},
            {"text": "Site do Google", "url": "https://google.com"},
            {"text": "Ligar", "copy": "+5511999999999"},
        ],
        "image": "https://picsum.photos/seed/zapzap-buttons/900/500",
    }


def test_transport_sends_carousel_as_json_array() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"messageType": "InteractiveMessage", "status": "Pending"})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)

    response = client.messages.send_carousel(
        "instance-1",
        CarouselMessage(
            number="5511999999999",
            text="Confira nossas opcoes:",
            carousel=[
                CarouselCard(
                    text="Produto 1",
                    image="https://example.com/img.jpg",
                    buttons=[CarouselButton(text="Quero", id="produto_1")],
                )
            ],
        ),
    )

    assert response == {"messageType": "InteractiveMessage", "status": "Pending"}
    assert len(calls) == 1
    assert calls[0].method == "POST"
    assert calls[0].url.path == "/api/v1/instance-1/send/carousel"
    assert json.loads(calls[0].read()) == {
        "number": "5511999999999",
        "delay": 1000,
        "text": "Confira nossas opcoes:",
        "carousel": [
            {
                "text": "Produto 1",
                "image": "https://example.com/img.jpg",
                "buttons": [{"type": "REPLY", "text": "Quero", "id": "produto_1"}],
            }
        ],
    }


def test_transport_sends_list_choices_as_json_array() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"messageType": "ListMessage", "status": "Pending"})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)

    response = client.messages.send_list(
        "instance-1",
        ListMessage(
            number="5511999999999",
            text="Escolha uma opcao:",
            category="Produtos",
            choices=[
                ListChoice(item="Camiseta", id="p1", description="R$ 50"),
                ListChoice(item="Calca", id="p2", description="R$ 120"),
            ],
            list_button="Opcoes",
            footer_text="Gostou?",
        ),
    )

    assert response == {"messageType": "ListMessage", "status": "Pending"}
    assert len(calls) == 1
    assert calls[0].method == "POST"
    assert calls[0].url.path == "/api/v1/instance-1/send/list"
    assert json.loads(calls[0].read()) == {
        "number": "5511999999999",
        "text": "Escolha uma opcao:",
        "choices": ["[Produtos]", "Camiseta|p1|R$ 50", "Calca|p2|R$ 120"],
        "listButton": "Opcoes",
        "footerText": "Gostou?",
    }


def test_account_and_instances_services_cover_documented_group_routes() -> None:
    calls: list[httpx.Request] = []
    responses = {
        ("GET", "/api/v1/account"): {
            "id": "account-1",
            "name": "Joao",
            "email": "joao@example.com",
            "balance": "150.00",
            "billing_day": 10,
            "status": "ACTIVE",
        },
        ("GET", "/api/v1/instances"): [
            {
                "id": "instance-1",
                "name": "minha-instancia",
                "status": "CONNECTED",
                "phone_number": "5511999999999",
                "webhook_events": ["messages", "connection"],
                "webhook_exclude": ["wasSentByApi", "isGroupYes"],
            }
        ],
        ("POST", "/api/v1/instances"): {
            "instance": {"id": "instance-2", "name": "nova", "status": "PENDING"},
            "billing": {"charged": 25.5},
        },
        ("GET", "/api/v1/instances/cost"): {
            "activationFee": 10,
            "prorate": 15.5,
            "total": 25.5,
            "instancePrice": 49.9,
            "currentBalance": 150,
        },
        ("DELETE", "/api/v1/instances/instance-1"): {"message": "Instancia deletada com sucesso"},
        ("GET", "/api/v1/instances/instance-1"): {
            "id": "instance-1",
            "name": "minha-instancia",
            "status": "CONNECTED",
            "phone_number": "5511999999999",
        },
        ("PUT", "/api/v1/instances/instance-1"): {
            "id": "instance-1",
            "name": "minha-instancia",
            "webhook_url": "https://example.com/webhook",
            "metadata": {"clientId": "123"},
        },
        ("GET", "/api/v1/instances/instance-1/qrcode"): {
            "connected": True,
            "loggedIn": True,
            "instance": {
                "id": "instance-1",
                "token": "secret-token",
                "paircode": "",
                "qrcode": "",
                "status": "connected",
                "profileName": "Nome",
                "profilePicUrl": "https://example.com/profile.jpg",
                "isBusiness": True,
                "plataform": "smba",
                "systemName": "ZapZap API",
                "owner": "5511999999999",
                "current_presence": "unavailable",
                "currentTime": "2026-07-18 14:51:59.530Z",
            },
        },
        ("GET", "/api/v1/instances/instance-1/webhook"): {
            "webhook_url": "https://example.com/webhook",
            "configured": True,
        },
        ("PUT", "/api/v1/instances/instance-1/webhook"): {
            "ok": True,
            "webhook_url": "https://example.com/webhook",
        },
        ("POST", "/api/v1/instances/instance-1/webhook/test"): {
            "ok": True,
            "statusCode": 200,
            "responseTime": 150,
        },
    }

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json=responses[(request.method, request.url.path)])

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)

    account = client.account.get()
    instances = client.instances.list()
    created = client.instances.create(
        CreateInstanceRequest(
            name="nova",
            system_name="Meu App",
            metadata={"clientId": "123"},
        )
    )
    cost = client.instances.cost()
    details = client.instances.get("instance-1")
    updated = client.instances.update(
        "instance-1",
        UpdateInstanceRequest(
            webhook_url="https://example.com/webhook",
            metadata={"clientId": "123"},
        ),
    )
    deleted = client.instances.delete("instance-1")
    qrcode = client.instances.qrcode("instance-1")
    webhook = client.instances.get_webhook("instance-1")
    configured = client.instances.configure_webhook(
        "instance-1",
        ConfigureInstanceWebhookRequest(
            webhook_url="https://example.com/webhook",
            events=[InstanceWebhookEvent.MESSAGES, InstanceWebhookEvent.MESSAGES_UPDATE],
            exclude_messages=[
                InstanceWebhookExclude.WAS_SENT_BY_API,
                InstanceWebhookExclude.IS_GROUP_YES,
            ],
        ),
    )
    tested = client.instances.test_webhook(
        "instance-1",
        TestInstanceWebhookRequest(url="https://example.com/webhook-test"),
    )

    assert isinstance(account, AccountResponse)
    assert isinstance(instances, list)
    assert isinstance(instances[0], InstanceResponse)
    assert instances[0].webhook_events == ["messages", "connection"]
    assert instances[0].webhook_exclude == ["wasSentByApi", "isGroupYes"]
    assert isinstance(created, CreateInstanceResponse)
    assert isinstance(cost, InstanceCreationCostResponse)
    assert isinstance(details, InstanceResponse)
    assert isinstance(updated, InstanceResponse)
    assert isinstance(deleted, DeleteInstanceResponse)
    assert isinstance(qrcode, InstanceQRCodeResponse)
    assert qrcode.logged_in is True
    assert isinstance(qrcode.instance, InstanceQRCodeDetails)
    assert qrcode.instance.token == "secret-token"
    assert qrcode.instance.profile_pic_url == "https://example.com/profile.jpg"
    assert qrcode.instance.platform == "smba"
    assert isinstance(webhook, InstanceWebhookResponse)
    assert isinstance(configured, ConfigureInstanceWebhookResponse)
    assert isinstance(tested, TestInstanceWebhookResponse)
    assert [(call.method, call.url.path) for call in calls] == [
        ("GET", "/api/v1/account"),
        ("GET", "/api/v1/instances"),
        ("POST", "/api/v1/instances"),
        ("GET", "/api/v1/instances/cost"),
        ("GET", "/api/v1/instances/instance-1"),
        ("PUT", "/api/v1/instances/instance-1"),
        ("DELETE", "/api/v1/instances/instance-1"),
        ("GET", "/api/v1/instances/instance-1/qrcode"),
        ("GET", "/api/v1/instances/instance-1/webhook"),
        ("PUT", "/api/v1/instances/instance-1/webhook"),
        ("POST", "/api/v1/instances/instance-1/webhook/test"),
    ]
    assert json.loads(calls[2].read()) == {
        "name": "nova",
        "systemName": "Meu App",
        "metadata": '{"clientId":"123"}',
    }
    assert json.loads(calls[5].read()) == {
        "webhook_url": "https://example.com/webhook",
        "metadata": '{"clientId":"123"}',
    }
    assert json.loads(calls[9].read()) == {
        "webhook_url": "https://example.com/webhook",
        "events": "messages,messages_update",
        "excludeMessages": "wasSentByApi,isGroupYes",
    }
    assert json.loads(calls[10].read()) == {"url": "https://example.com/webhook-test"}


def test_transport_raises_validation_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(422, json={"message": "number is required"})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)

    with pytest.raises(ZapZapValidationError):
        client.messages.send_text("instance-1", TextMessage(number="5511999999999", text="Olá"))
