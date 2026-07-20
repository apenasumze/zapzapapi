"""Contratos de conversas e mensagens existentes."""

from __future__ import annotations

from enum import Enum

from pydantic import Field, field_serializer, field_validator

from zapzapapi.models.base import BaseModel
from zapzapapi.models.common import (
    ApiBoolean,
    normalize_string_list,
    serialize_api_boolean,
    serialize_required_api_boolean,
)


class ChatSearchOperator(str, Enum):
    """Operadores logicos aceitos na busca de chats."""

    AND = "AND"
    OR = "OR"


class PresenceType(str, Enum):
    """Tipos aceitos pelo indicador de presenca."""

    COMPOSING = "composing"  # Digitando
    RECORDING = "recording"  # Gravando
    PAUSED = "paused"  # Pausado


class ReactionMessage(BaseModel):
    """Reacao enviada para uma mensagem existente."""

    number: str
    message_id: str = Field(alias="id")
    emoji: str


class FindChatsRequest(BaseModel):
    """Filtros para buscar conversas."""

    operator: ChatSearchOperator | None = None
    sort: str | None = None
    limit: int | float | None = None
    offset: int | float | None = None
    wa_fastid: str | None = None
    wa_chatid: str | None = None
    wa_archived: ApiBoolean | None = None
    wa_contact_name: str | None = Field(default=None, alias="wa_contactName")
    wa_name: str | None = None
    name: str | None = None
    wa_is_blocked: ApiBoolean | None = Field(default=None, alias="wa_isBlocked")
    wa_is_group: ApiBoolean | None = Field(default=None, alias="wa_isGroup")
    wa_is_group_admin: ApiBoolean | None = Field(default=None, alias="wa_isGroup_admin")
    wa_is_group_announce: ApiBoolean | None = Field(default=None, alias="wa_isGroup_announce")
    wa_is_group_member: ApiBoolean | None = Field(default=None, alias="wa_isGroup_member")
    wa_is_pinned: ApiBoolean | None = Field(default=None, alias="wa_isPinned")
    wa_label: str | None = None
    wa_notes: str | None = None
    lead_tags: str | None = None
    lead_is_ticket_open: ApiBoolean | None = Field(default=None, alias="lead_isTicketOpen")
    lead_assigned_attendant_id: str | None = Field(
        default=None,
        alias="lead_assignedAttendant_id",
    )
    lead_status: str | None = None

    @field_serializer(
        "wa_archived",
        "wa_is_blocked",
        "wa_is_group",
        "wa_is_group_admin",
        "wa_is_group_announce",
        "wa_is_group_member",
        "wa_is_pinned",
        "lead_is_ticket_open",
    )
    def _serialize_api_boolean(self, value: ApiBoolean | None) -> str | None:
        return serialize_api_boolean(value)


class ReadChatRequest(BaseModel):
    """Dados para marcar uma conversa como lida."""

    number: str


class ArchiveChatRequest(BaseModel):
    """Dados para arquivar ou desarquivar uma conversa."""

    number: str
    archive: ApiBoolean

    @field_serializer("archive")
    def _serialize_archive(self, archive: ApiBoolean) -> str:
        return serialize_required_api_boolean(archive)


class PinChatRequest(BaseModel):
    """Dados para fixar ou desafixar uma conversa."""

    number: str
    pin: ApiBoolean

    @field_serializer("pin")
    def _serialize_pin(self, pin: ApiBoolean) -> str:
        return serialize_required_api_boolean(pin)


class MuteChatRequest(BaseModel):
    """Dados para silenciar uma conversa."""

    number: str
    duration: int | float | None = None


class BlockChatRequest(BaseModel):
    """Dados para bloquear ou desbloquear um contato."""

    number: str
    block: ApiBoolean

    @field_serializer("block")
    def _serialize_block(self, block: ApiBoolean) -> str:
        return serialize_required_api_boolean(block)


class DeleteChatRequest(BaseModel):
    """Dados para deletar ou limpar uma conversa."""

    number: str
    delete_chat_db: ApiBoolean | None = Field(default=None, alias="deleteChatDB")
    delete_messages_db: ApiBoolean | None = Field(default=None, alias="deleteMessagesDB")
    delete_chat_whatsapp: ApiBoolean | None = Field(default=None, alias="deleteChatWhatsApp")
    clear_chat_whatsapp: ApiBoolean | None = Field(default=None, alias="clearChatWhatsApp")

    @field_serializer(
        "delete_chat_db",
        "delete_messages_db",
        "delete_chat_whatsapp",
        "clear_chat_whatsapp",
    )
    def _serialize_api_boolean(self, value: ApiBoolean | None) -> str | None:
        return serialize_api_boolean(value)


class ChatNotesRequest(BaseModel):
    """Dados para consultar notas de uma conversa."""

    number: str | None = None


class EditChatNotesRequest(BaseModel):
    """Dados para editar notas de uma conversa."""

    number: str | None = None
    notes: str | None = None


class RefreshChatNotesRequest(BaseModel):
    """Dados para recarregar notas de uma conversa."""

    number: str | None = None
    force: ApiBoolean | None = None

    @field_serializer("force")
    def _serialize_force(self, force: ApiBoolean | None) -> str | None:
        return serialize_api_boolean(force)


class FindMessagesRequest(BaseModel):
    """Filtros para buscar historico de mensagens."""

    chat_id: str | None = Field(default=None, alias="chatid")
    message_id: str | None = Field(default=None, alias="id")
    limit: int | float | None = None
    offset: int | float | None = None


class EditMessageRequest(BaseModel):
    """Dados para editar uma mensagem existente."""

    message_id: str = Field(alias="id")
    number: str
    text: str


class DeleteMessageRequest(BaseModel):
    """Dados para deletar uma mensagem existente."""

    message_id: str = Field(alias="id")
    number: str | None = None


class DownloadMessageRequest(BaseModel):
    """Dados para baixar midia de uma mensagem."""

    message_id: str = Field(alias="id")
    return_link: ApiBoolean | None = None
    return_base64: ApiBoolean | None = None
    generate_mp3: ApiBoolean | None = None
    transcribe: ApiBoolean | None = None

    @field_serializer("return_link", "return_base64", "generate_mp3", "transcribe")
    def _serialize_api_boolean(self, value: ApiBoolean | None) -> str | None:
        return serialize_api_boolean(value)


class MarkMessagesReadRequest(BaseModel):
    """Dados para marcar mensagens como lidas."""

    message_ids: list[str] = Field(alias="id")

    @field_validator("message_ids", mode="before")
    @classmethod
    def _normalize_message_ids(cls, message_ids: object) -> object:
        return normalize_string_list(message_ids)


class PresenceRequest(BaseModel):
    """Dados para enviar indicador de digitacao ou gravacao."""

    number: str
    presence: PresenceType
    delay: int | float | None = None


class HistorySyncRequest(BaseModel):
    """Dados para sincronizar mensagens antigas de uma conversa."""

    message_id: str | None = Field(default=None, alias="messageid")
    number: str | None = None
    count: int | float | None = None
