"""Serviço de instâncias."""

from __future__ import annotations

from zapzapapi.models.base import JsonValue
from zapzapapi.models.instance import (
    ConfigureInstanceWebhookRequest,
    ConfigureInstanceWebhookResponse,
    CreateInstanceRequest,
    CreateInstanceResponse,
    DeleteInstanceResponse,
    InstanceCreationCostResponse,
    InstanceQRCodeResponse,
    InstanceResponse,
    InstanceWebhookResponse,
    TestInstanceWebhookRequest,
    TestInstanceWebhookResponse,
    UpdateInstanceRequest,
)
from zapzapapi.services.base import BaseService


class InstancesService(BaseService):
    """Operações administrativas de instâncias."""

    def list(self) -> list[InstanceResponse] | JsonValue:
        """Lista as instâncias da conta."""

        response = self._transport.get("/api/v1/instances")
        if isinstance(response, list):
            return [InstanceResponse.model_validate(item) for item in response]
        return response

    def create(self, data: CreateInstanceRequest) -> CreateInstanceResponse | JsonValue:
        """Cria uma nova instância.

        Args:
            data: Dados de criação da instância.
        """

        response = self._transport.post("/api/v1/instances", data)
        if isinstance(response, dict):
            return CreateInstanceResponse.model_validate(response)
        return response

    def cost(self) -> InstanceCreationCostResponse | JsonValue:
        """Retorna o custo de criação de uma instância."""

        response = self._transport.get("/api/v1/instances/cost")
        if isinstance(response, dict):
            return InstanceCreationCostResponse.model_validate(response)
        return response

    def get(self, instance_id: str) -> InstanceResponse | JsonValue:
        """Retorna detalhes de uma instância."""

        response = self._transport.get(f"/api/v1/instances/{instance_id}")
        if isinstance(response, dict):
            return InstanceResponse.model_validate(response)
        return response

    def update(self, instance_id: str, data: UpdateInstanceRequest) -> InstanceResponse | JsonValue:
        """Atualiza uma instância."""

        response = self._transport.put(f"/api/v1/instances/{instance_id}", data)
        if isinstance(response, dict):
            return InstanceResponse.model_validate(response)
        return response

    def delete(self, instance_id: str) -> DeleteInstanceResponse | JsonValue:
        """Remove uma instância."""

        response = self._transport.delete(f"/api/v1/instances/{instance_id}")
        if isinstance(response, dict):
            return DeleteInstanceResponse.model_validate(response)
        return response

    def qrcode(self, instance_id: str) -> InstanceQRCodeResponse | JsonValue:
        """Retorna o QR Code de uma instância."""

        response = self._transport.get(f"/api/v1/instances/{instance_id}/qrcode")
        if isinstance(response, dict):
            return InstanceQRCodeResponse.model_validate(response)
        return response

    def get_webhook(self, instance_id: str) -> InstanceWebhookResponse | JsonValue:
        """Retorna a configuração de webhook administrativo da instância."""

        response = self._transport.get(f"/api/v1/instances/{instance_id}/webhook")
        if isinstance(response, dict):
            return InstanceWebhookResponse.model_validate(response)
        return response

    def configure_webhook(
        self,
        instance_id: str,
        data: ConfigureInstanceWebhookRequest,
    ) -> ConfigureInstanceWebhookResponse | JsonValue:
        """Configura o webhook administrativo da instância."""

        response = self._transport.put(f"/api/v1/instances/{instance_id}/webhook", data)
        if isinstance(response, dict):
            return ConfigureInstanceWebhookResponse.model_validate(response)
        return response

    def test_webhook(
        self,
        instance_id: str,
        data: TestInstanceWebhookRequest | None = None,
    ) -> TestInstanceWebhookResponse | JsonValue:
        """Testa o webhook administrativo da instância."""

        response = self._transport.post(f"/api/v1/instances/{instance_id}/webhook/test", data)
        if isinstance(response, dict):
            return TestInstanceWebhookResponse.model_validate(response)
        return response
