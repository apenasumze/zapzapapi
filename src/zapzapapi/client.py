"""Client principal da ZapZapApi."""

from __future__ import annotations

import httpx

from zapzapapi.config import ZapZapConfig
from zapzapapi.services.account import AccountService
from zapzapapi.services.chats import ChatsService
from zapzapapi.services.contacts import ContactsService
from zapzapapi.services.groups import GroupsService
from zapzapapi.services.instances import InstancesService
from zapzapapi.services.messages import MessagesService
from zapzapapi.services.profile import ProfileService
from zapzapapi.transport import ZapZapTransport


class ZapZapClient:
    """Fachada principal para consumir a ZapZapApi.

    Args:
        api_key: Chave pública da API.
        api_secret: Chave secreta da API.
        base_url: URL base da ZapZapApi.
        timeout: Timeout de cada requisição em segundos.
        http_client: Client HTTP opcional, usado principalmente em testes.
    """

    def __init__(
        self,
        *,
        api_key: str,
        api_secret: str,
        base_url: str = "https://app.zapzapapi.com",
        timeout: float = 15.0,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.config = ZapZapConfig(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
            timeout=timeout,
        )
        self._transport = ZapZapTransport(self.config, http_client=http_client)
        self.account = AccountService(self._transport)
        self.instances = InstancesService(self._transport)
        self.messages = MessagesService(self._transport)
        self.chats = ChatsService(self._transport)
        self.contacts = ContactsService(self._transport)
        self.profile = ProfileService(self._transport)
        self.groups = GroupsService(self._transport)

    def close(self) -> None:
        """Fecha recursos HTTP mantidos pelo client."""

        self._transport.close()

    def __enter__(self) -> ZapZapClient:
        """Entra no contexto gerenciado."""

        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        """Fecha o transporte ao sair do contexto gerenciado."""

        self.close()
