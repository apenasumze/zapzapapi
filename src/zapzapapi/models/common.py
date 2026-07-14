"""Contratos compartilhados entre módulos."""

from __future__ import annotations

from pydantic import Field

from zapzapapi.models.base import BaseModel


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

