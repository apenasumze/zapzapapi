"""Serviço de conta."""

from __future__ import annotations

from zapzapapi.models.account import AccountResponse
from zapzapapi.models.base import JsonValue
from zapzapapi.services.base import BaseService


class AccountService(BaseService):
    """Operações relacionadas à conta ZapZapApi."""

    def get(self) -> AccountResponse | JsonValue:
        """Retorna os dados da conta autenticada.

        Returns:
            Dados da conta quando a resposta segue o contrato conhecido.
        """

        response = self._transport.get("/api/v1/account")
        if isinstance(response, dict):
            return AccountResponse.model_validate(response)
        return response
