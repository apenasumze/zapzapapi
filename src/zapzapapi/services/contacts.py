"""Servico de contatos e verificacao de numeros."""

from __future__ import annotations

from zapzapapi.models.base import JsonValue
from zapzapapi.models.contacts import (
    AddContactRequest,
    CheckNumbersRequest,
    ContactDetailsRequest,
    ListContactsRequest,
    RemoveContactRequest,
)
from zapzapapi.services.base import BaseService


class ContactsService(BaseService):
    """Operacoes de contatos, agenda e detalhes publicos."""

    def check_numbers(self, instance_id: str, data: CheckNumbersRequest) -> JsonValue:
        """Verifica se numeros existem no WhatsApp."""

        return self._transport.post(f"/api/v1/{instance_id}/chat/check", data)

    def details(self, instance_id: str, data: ContactDetailsRequest) -> JsonValue:
        """Consulta detalhes publicos de um contato ou grupo."""

        return self._transport.post(f"/api/v1/{instance_id}/chat/details", data)

    def add(self, instance_id: str, data: AddContactRequest) -> JsonValue:
        """Adiciona um contato a agenda da instancia."""

        return self._transport.post(f"/api/v1/{instance_id}/contact/add", data)

    def remove(self, instance_id: str, data: RemoveContactRequest) -> JsonValue:
        """Remove um contato da agenda da instancia."""

        return self._transport.post(f"/api/v1/{instance_id}/contact/remove", data)

    def list_fast(self, instance_id: str) -> JsonValue:
        """Lista contatos rapidamente."""

        return self._transport.get(f"/api/v1/{instance_id}/contacts")

    def list(self, instance_id: str, filters: ListContactsRequest | None = None) -> JsonValue:
        """Lista contatos com paginacao."""

        return self._transport.post(f"/api/v1/{instance_id}/contacts/list", filters)
