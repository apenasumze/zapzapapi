"""Contratos de grupos e comunidades."""

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


class GroupParticipantAction(str, Enum):
    """Acoes aceitas para gerenciamento de participantes."""

    ADD = "add"
    REMOVE = "remove"
    PROMOTE = "promote"
    DEMOTE = "demote"
    APPROVE = "approve"
    REJECT = "reject"


class CreateGroupRequest(BaseModel):
    """Dados para criar um grupo."""

    name: str  # Nome do grupo.
    participants: list[str]  # Lista de participantes iniciais.

    @field_validator("participants", mode="before")
    @classmethod
    def _normalize_participants(cls, participants: object) -> object:
        return normalize_string_list(participants)


class GroupInfoRequest(BaseModel):
    """Dados para consultar informacoes de um grupo."""

    group_jid: str = Field(alias="groupjid")
    get_invite_link: ApiBoolean | None = Field(default=None, alias="getInviteLink")

    @field_serializer("get_invite_link")
    def _serialize_get_invite_link(self, value: ApiBoolean | None) -> str | None:
        return serialize_api_boolean(value)


class GroupInviteInfoRequest(BaseModel):
    """Dados para consultar informacoes pelo convite do grupo."""

    invite_code: str = Field(alias="invitecode")


class JoinGroupRequest(BaseModel):
    """Dados para entrar em um grupo via convite."""

    invite_code: str = Field(alias="invitecode")


class LeaveGroupRequest(BaseModel):
    """Dados para sair de um grupo."""

    group_jid: str = Field(alias="groupjid")


class ListGroupsRequest(BaseModel):
    """Filtros para buscar grupos."""

    get_participants: ApiBoolean | None = Field(default=None, alias="getParticipants")

    @field_serializer("get_participants")
    def _serialize_get_participants(self, value: ApiBoolean | None) -> str | None:
        return serialize_api_boolean(value)


class ResetGroupInviteCodeRequest(BaseModel):
    """Dados para resetar o codigo de convite de um grupo."""

    group_jid: str = Field(alias="groupjid")


class UpdateGroupAnnounceRequest(BaseModel):
    """Dados para alterar o modo somente admins de um grupo."""

    group_jid: str = Field(alias="groupjid")
    announce: ApiBoolean

    @field_serializer("announce")
    def _serialize_announce(self, announce: ApiBoolean) -> str:
        return serialize_required_api_boolean(announce)


class UpdateGroupDescriptionRequest(BaseModel):
    """Dados para alterar a descricao de um grupo."""

    group_jid: str = Field(alias="groupjid")
    description: str


class UpdateGroupImageRequest(BaseModel):
    """Dados para alterar a foto de um grupo."""

    group_jid: str = Field(alias="groupjid")
    image: str


class UpdateGroupLockedRequest(BaseModel):
    """Dados para bloquear ou liberar a edicao de um grupo."""

    group_jid: str = Field(alias="groupjid")
    locked: ApiBoolean

    @field_serializer("locked")
    def _serialize_locked(self, locked: ApiBoolean) -> str:
        return serialize_required_api_boolean(locked)


class UpdateGroupNameRequest(BaseModel):
    """Dados para renomear um grupo."""

    group_jid: str = Field(alias="groupjid")
    name: str


class UpdateGroupParticipantsRequest(BaseModel):
    """Dados para gerenciar participantes de um grupo."""

    group_jid: str = Field(alias="groupjid")
    action: GroupParticipantAction
    participants: list[str]

    @field_validator("participants", mode="before")
    @classmethod
    def _normalize_participants(cls, participants: object) -> object:
        return normalize_string_list(participants)
