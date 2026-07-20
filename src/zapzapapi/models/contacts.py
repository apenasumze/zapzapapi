"""Contratos de contatos e verificacao de numeros."""

from __future__ import annotations

from pydantic import field_serializer, field_validator

from zapzapapi.models.base import BaseModel
from zapzapapi.models.common import (
    ApiBoolean,
    normalize_string_list,
    serialize_api_boolean,
)


class CheckNumbersRequest(BaseModel):
    """Dados para verificar se numeros existem no WhatsApp."""

    numbers: list[str]

    @field_validator("numbers", mode="before")
    @classmethod
    def _normalize_numbers(cls, numbers: object) -> object:
        return normalize_string_list(numbers)


class ContactDetailsRequest(BaseModel):
    """Dados para consultar detalhes publicos de um contato ou grupo."""

    number: str
    preview: ApiBoolean | None = None

    @field_serializer("preview")
    def _serialize_preview(self, preview: ApiBoolean | None) -> str | None:
        return serialize_api_boolean(preview)


class AddContactRequest(BaseModel):
    """Dados para adicionar um contato a agenda da instancia."""

    phone: str
    name: str


class RemoveContactRequest(BaseModel):
    """Dados para remover um contato da agenda da instancia."""

    number: str


class ListContactsRequest(BaseModel):
    """Filtros de paginacao para listar contatos."""

    limit: int | float | None = None
    offset: int | float | None = None
