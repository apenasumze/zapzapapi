"""Servico do perfil da instancia conectada."""

from __future__ import annotations

from zapzapapi.models.base import JsonValue
from zapzapapi.models.profile import UpdateProfileImageRequest, UpdateProfileNameRequest
from zapzapapi.services.base import BaseService


class ProfileService(BaseService):
    """Operacoes sobre o perfil publico da instancia conectada."""

    def update_image(self, instance_id: str, data: UpdateProfileImageRequest) -> JsonValue:
        """Altera a foto do perfil da instancia conectada."""

        return self._transport.post(f"/api/v1/{instance_id}/profile/image", data)

    def update_name(self, instance_id: str, data: UpdateProfileNameRequest) -> JsonValue:
        """Altera o nome do perfil da instancia conectada."""

        return self._transport.post(f"/api/v1/{instance_id}/profile/name", data)
