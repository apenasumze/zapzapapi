"""Serviço de instâncias."""

from __future__ import annotations

from zapzapapi.models.base import JsonValue
from zapzapapi.models.instance import (
    ConfigureInstanceWebhookRequest,
    CreateInstanceRequest,
    UpdateInstanceRequest,
)
from zapzapapi.services.base import BaseService


class InstancesService(BaseService):
    """Operações administrativas de instâncias."""

    def list(self) -> JsonValue:
        """Lista as instâncias da conta."""

        return self._transport.get("/api/v1/instances")

    def create(self, data: CreateInstanceRequest) -> JsonValue:
        """Cria uma nova instância.

        Args:
            data: Dados de criação da instância.
        """

        return self._transport.post("/api/v1/instances", data)

    def cost(self) -> JsonValue:
        """Retorna o custo de criação de uma instância."""

        return self._transport.get("/api/v1/instances/cost")

    def get(self, instance_id: str) -> JsonValue:
        """Retorna detalhes de uma instância."""

        return self._transport.get(f"/api/v1/instances/{instance_id}")

    def update(self, instance_id: str, data: UpdateInstanceRequest) -> JsonValue:
        """Atualiza uma instância."""

        return self._transport.put(f"/api/v1/instances/{instance_id}", data)

    def delete(self, instance_id: str) -> JsonValue:
        """Remove uma instância."""

        return self._transport.delete(f"/api/v1/instances/{instance_id}")

    def qrcode(self, instance_id: str) -> JsonValue:
        """Retorna o QR Code de uma instância."""

        return self._transport.get(f"/api/v1/instances/{instance_id}/qrcode")

    def get_webhook(self, instance_id: str) -> JsonValue:
        """Retorna a configuração de webhook administrativo da instância."""

        return self._transport.get(f"/api/v1/instances/{instance_id}/webhook")

    def configure_webhook(
        self,
        instance_id: str,
        data: ConfigureInstanceWebhookRequest,
    ) -> JsonValue:
        """Configura o webhook administrativo da instância."""

        return self._transport.put(f"/api/v1/instances/{instance_id}/webhook", data)

    def test_webhook(self, instance_id: str) -> JsonValue:
        """Testa o webhook administrativo da instância."""

        return self._transport.post(f"/api/v1/instances/{instance_id}/webhook/test")
