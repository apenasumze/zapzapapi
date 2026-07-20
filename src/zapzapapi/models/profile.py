"""Contratos do perfil da instancia conectada."""

from __future__ import annotations

from zapzapapi.models.base import BaseModel


class UpdateProfileImageRequest(BaseModel):
    """Dados para alterar a foto do perfil da instancia conectada."""

    image: str


class UpdateProfileNameRequest(BaseModel):
    """Dados para alterar o nome do perfil da instancia conectada."""

    name: str
