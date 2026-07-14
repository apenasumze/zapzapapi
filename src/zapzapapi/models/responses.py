"""Contratos genéricos de resposta."""

from __future__ import annotations

from typing import Any

from zapzapapi.models.base import BaseModel


class GenericResponse(BaseModel):
    """Resposta genérica para endpoints ainda sem contrato específico consolidado."""

    status: str | None = None
    message: str | None = None
    id: str | None = None
    data: dict[str, Any] | list[Any] | None = None

