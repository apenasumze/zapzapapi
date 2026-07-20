"""Contratos compartilhados entre módulos."""

from __future__ import annotations

import json
from typing import Literal

from pydantic import Field

from zapzapapi.models.base import BaseModel

ApiBoolean = bool | Literal["true", "false"]


class MessageReference(BaseModel):
    """Referência a uma mensagem existente.

    Args:
        message_id: Identificador da mensagem.
    """

    message_id: str = Field(alias="id")


class TrackingFields(BaseModel):
    """Campos opcionais para rastreamento de requisições.

    Args:
        track_source: Origem de rastreamento.
        track_id: Identificador externo de rastreamento.
    """

    track_source: str | None = None
    track_id: str | None = None


def serialize_api_boolean(value: ApiBoolean | None) -> str | None:
    """Serializa booleanos no formato string usado pela API."""

    if value is None:
        return None
    return serialize_required_api_boolean(value)


def serialize_required_api_boolean(value: ApiBoolean) -> str:
    """Serializa um booleano obrigatorio no formato externo da API."""

    if isinstance(value, bool):
        return "true" if value else "false"
    return value


def normalize_string_list(value: object) -> object:
    """Normaliza string JSON/CSV para lista de strings."""

    if isinstance(value, list):
        return value
    if not isinstance(value, str):
        return value

    raw_value = value.strip()
    if not raw_value:
        return []

    if raw_value.startswith("["):
        parsed = json.loads(raw_value)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
        return parsed

    return [item.strip() for item in raw_value.split(",") if item.strip()]
