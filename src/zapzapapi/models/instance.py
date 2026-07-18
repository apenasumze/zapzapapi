"""Contratos de instâncias."""

from __future__ import annotations

import json
from collections.abc import Sequence
from decimal import Decimal
from enum import Enum
from typing import ClassVar

from pydantic import ConfigDict, Field, field_serializer

from zapzapapi.models.base import BaseModel, JsonObject


class ResponseModel(BaseModel):
    """Modelo de resposta que preserva campos extras retornados pela API."""

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        use_enum_values=True,
    )


class InstanceWebhookEvent(str, Enum):
    """Eventos configuraveis para o webhook administrativo da instancia."""

    MESSAGES = "messages"
    CONNECTION = "connection"
    MESSAGES_UPDATE = "messages_update"
    GROUPS = "groups"
    CHATS = "chats"
    LEADS = "leads"
    CONTACTS = "contacts"
    HISTORY = "history"
    QRCODE = "qrcode"
    LABELS = "labels"
    PRESENCE = "presence"
    CHAT_LABELS = "chat_labels"
    BLOCKS = "blocks"
    CALL = "call"


class InstanceWebhookExclude(str, Enum):
    """Filtros de mensagens que podem ser ignorados pelo webhook."""

    WAS_SENT_BY_API = "wasSentByApi"
    WAS_NOT_SENT_BY_API = "wasNotSentByApi"
    FROM_ME_YES = "fromMeYes"
    FROM_ME_NO = "fromMeNo"
    IS_GROUP_NO = "isGroupNo"
    IS_GROUP_YES = "isGroupYes"


WebhookEventValue = str | InstanceWebhookEvent
WebhookExcludeValue = str | InstanceWebhookExclude


class CreateInstanceRequest(BaseModel):
    """Dados para criação de uma instância.

    Args:
        name: Nome da instância.
        system_name: Nome do sistema exibido no WhatsApp.
        metadata: Dados livres vinculados ao sistema consumidor.
    """

    name: str
    system_name: str | None = Field(default=None, alias="systemName")
    metadata: str | JsonObject | None = None

    @field_serializer("metadata")
    def _serialize_metadata(self, metadata: str | JsonObject | None) -> str | None:
        if metadata is None:
            return None
        if isinstance(metadata, str):
            return metadata
        return json.dumps(metadata, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


class UpdateInstanceRequest(BaseModel):
    """Dados para atualização de uma instância."""

    webhook_url: str | None = None
    metadata: str | JsonObject | None = None

    @field_serializer("metadata")
    def _serialize_metadata(self, metadata: str | JsonObject | None) -> str | None:
        if metadata is None:
            return None
        if isinstance(metadata, str):
            return metadata
        return json.dumps(metadata, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


class ConfigureInstanceWebhookRequest(BaseModel):
    """Dados para configurar o webhook administrativo de uma instância."""

    webhook_url: str
    events: WebhookEventValue | list[WebhookEventValue] | None = None
    exclude_messages: WebhookExcludeValue | list[WebhookExcludeValue] | None = Field(
        default=None,
        alias="excludeMessages",
    )

    @field_serializer("events")
    def _serialize_events(
        self,
        events: WebhookEventValue | list[WebhookEventValue] | None,
    ) -> str | None:
        if events is None:
            return None
        return serialize_csv(events)

    @field_serializer("exclude_messages")
    def _serialize_exclude_messages(
        self,
        exclude_messages: WebhookExcludeValue | list[WebhookExcludeValue] | None,
    ) -> str | None:
        if exclude_messages is None:
            return None
        return serialize_csv(exclude_messages)


class TestInstanceWebhookRequest(BaseModel):
    """Dados opcionais para testar o webhook administrativo."""

    __test__: ClassVar[bool] = False

    url: str | None = None


class InstanceResponse(ResponseModel):
    """Dados principais de uma instância."""

    id: str
    name: str | None = None
    status: str | None = None
    phone_number: str | None = None
    system_name: str | None = Field(default=None, alias="systemName")
    webhook_url: str | None = None
    webhook_enabled: bool | None = None
    webhook_events: list[WebhookEventValue] = Field(default_factory=list)
    webhook_exclude: list[WebhookExcludeValue] = Field(default_factory=list)
    metadata: str | JsonObject | None = None


class InstanceBillingResponse(ResponseModel):
    """Dados de cobrança gerados na criação da instância."""

    charged: Decimal | float | int | None = None


class CreateInstanceResponse(ResponseModel):
    """Resposta da criação de uma instância."""

    instance: InstanceResponse | JsonObject
    billing: InstanceBillingResponse | JsonObject | None = None


class InstanceCreationCostResponse(ResponseModel):
    """Custo calculado para criação de uma instância."""

    activation_fee: Decimal | float | int | None = Field(default=None, alias="activationFee")
    prorate: Decimal | float | int | None = None
    total: Decimal | float | int | None = None
    instance_price: Decimal | float | int | None = Field(default=None, alias="instancePrice")
    current_balance: Decimal | float | int | None = Field(default=None, alias="currentBalance")


class DeleteInstanceResponse(ResponseModel):
    """Resposta da remoção de uma instância."""

    message: str | None = None


class InstanceQRCodeDetails(ResponseModel):
    """Dados resumidos da instância retornados junto ao QR Code."""

    id: str | None = None
    token: str | None = None
    status: str | None = None
    paircode: str | None = None
    qrcode: str | None = None
    name: str | None = None
    profile_name: str | None = Field(default=None, alias="profileName")
    profile_pic_url: str | None = Field(default=None, alias="profilePicUrl")
    is_business: bool | None = Field(default=None, alias="isBusiness")
    platform: str | None = Field(default=None, alias="plataform")
    system_name: str | None = Field(default=None, alias="systemName")
    owner: str | None = None
    current_presence: str | None = None
    created: str | None = None
    updated: str | None = None
    current_time: str | None = Field(default=None, alias="currentTime")


class InstanceQRCodeResponse(ResponseModel):
    """Resposta da consulta de QR Code."""

    connected: bool | None = None
    logged_in: bool | None = Field(default=None, alias="loggedIn")
    instance: InstanceQRCodeDetails | JsonObject | None = None
    qrcode: str | None = None
    base64: str | None = None
    code: str | None = None


class InstanceWebhookResponse(ResponseModel):
    """Configuração atual de webhook administrativo."""

    webhook_url: str | None = None
    configured: bool | None = None
    events: WebhookEventValue | list[WebhookEventValue] | None = None
    exclude_messages: WebhookExcludeValue | list[WebhookExcludeValue] | None = Field(
        default=None,
        alias="excludeMessages",
    )


class ConfigureInstanceWebhookResponse(ResponseModel):
    """Resposta da configuração de webhook administrativo."""

    ok: bool | None = None
    webhook_url: str | None = None
    message: str | None = None


class TestInstanceWebhookResponse(ResponseModel):
    """Resposta do teste de webhook administrativo."""

    __test__: ClassVar[bool] = False

    ok: bool | None = None
    status_code: int | None = Field(default=None, alias="statusCode")
    response_time: int | float | None = Field(default=None, alias="responseTime")
    message: str | None = None


def serialize_csv(value: str | Enum | Sequence[str | Enum]) -> str:
    if isinstance(value, Enum):
        return str(value.value)
    if isinstance(value, str):
        return value
    return ",".join(str(item.value) if isinstance(item, Enum) else item for item in value)
