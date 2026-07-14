"""Contratos de instâncias."""

from __future__ import annotations

from pydantic import Field

from zapzapapi.models.base import BaseModel


class CreateInstanceRequest(BaseModel):
    """Dados para criação de uma instância.

    Args:
        name: Nome da instância.
        phone: Número associado, quando exigido pela API.
    """

    name: str
    phone: str | None = None


class UpdateInstanceRequest(BaseModel):
    """Dados para atualização de uma instância."""

    name: str | None = None
    phone: str | None = None


class ConfigureInstanceWebhookRequest(BaseModel):
    """Dados para configurar o webhook administrativo de uma instância."""

    url: str
    enabled: bool = True
    events: list[str] = Field(default_factory=list)

