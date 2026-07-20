"""Servico de conversas e mensagens existentes."""

from __future__ import annotations

from zapzapapi.models.base import JsonValue
from zapzapapi.models.chat import (
    ArchiveChatRequest,
    BlockChatRequest,
    ChatNotesRequest,
    DeleteChatRequest,
    DeleteMessageRequest,
    DownloadMessageRequest,
    EditChatNotesRequest,
    EditMessageRequest,
    FindChatsRequest,
    FindMessagesRequest,
    HistorySyncRequest,
    MarkMessagesReadRequest,
    MuteChatRequest,
    PinChatRequest,
    PresenceRequest,
    ReactionMessage,
    ReadChatRequest,
    RefreshChatNotesRequest,
)
from zapzapapi.services.base import BaseService


class ChatsService(BaseService):
    """Operacoes sobre conversas e mensagens existentes."""

    def find(self, instance_id: str, filters: FindChatsRequest | None = None) -> JsonValue:
        """Busca conversas da instancia."""

        return self._transport.post(f"/api/v1/{instance_id}/chat/find", filters)

    def read(self, instance_id: str, data: ReadChatRequest) -> JsonValue:
        """Marca uma conversa como lida."""

        return self._transport.post(f"/api/v1/{instance_id}/chat/read", data)

    def archive(self, instance_id: str, data: ArchiveChatRequest) -> JsonValue:
        """Arquiva ou desarquiva uma conversa."""

        return self._transport.post(f"/api/v1/{instance_id}/chat/archive", data)

    def pin(self, instance_id: str, data: PinChatRequest) -> JsonValue:
        """Fixa ou desafixa uma conversa."""

        return self._transport.post(f"/api/v1/{instance_id}/chat/pin", data)

    def mute(self, instance_id: str, data: MuteChatRequest) -> JsonValue:
        """Silencia uma conversa."""

        return self._transport.post(f"/api/v1/{instance_id}/chat/mute", data)

    def block(self, instance_id: str, data: BlockChatRequest) -> JsonValue:
        """Bloqueia ou desbloqueia um contato.

        Nao utilizar para desbloquear contatos por bug conhecido da API.
        """

        return self._transport.post(f"/api/v1/{instance_id}/chat/block", data)

    def blocklist(self, instance_id: str) -> JsonValue:
        """Lista contatos bloqueados."""

        return self._transport.get(f"/api/v1/{instance_id}/chat/blocklist")

    def delete(self, instance_id: str, data: DeleteChatRequest) -> JsonValue:
        """Deleta ou limpa uma conversa."""

        return self._transport.post(f"/api/v1/{instance_id}/chat/delete", data)

    def notes(self, instance_id: str, data: ChatNotesRequest | None = None) -> JsonValue:
        """Consulta notas de uma conversa."""

        return self._transport.post(f"/api/v1/{instance_id}/chat/notes", data)

    def edit_notes(self, instance_id: str, data: EditChatNotesRequest) -> JsonValue:
        """Edita notas de uma conversa."""

        return self._transport.post(f"/api/v1/{instance_id}/chat/notes/edit", data)

    def refresh_notes(
        self,
        instance_id: str,
        data: RefreshChatNotesRequest | None = None,
    ) -> JsonValue:
        """Recarrega notas de uma conversa."""

        return self._transport.post(f"/api/v1/{instance_id}/chat/notes/refresh", data)

    def find_messages(
        self,
        instance_id: str,
        filters: FindMessagesRequest | None = None,
    ) -> JsonValue:
        """Busca historico de mensagens."""

        return self._transport.post(f"/api/v1/{instance_id}/message/find", filters)

    def edit_message(self, instance_id: str, data: EditMessageRequest) -> JsonValue:
        """Edita uma mensagem existente."""

        return self._transport.post(f"/api/v1/{instance_id}/message/edit", data)

    def delete_message(self, instance_id: str, data: DeleteMessageRequest) -> JsonValue:
        """Deleta uma mensagem existente."""

        return self._transport.post(f"/api/v1/{instance_id}/message/delete", data)

    def download_message(self, instance_id: str, data: DownloadMessageRequest) -> JsonValue:
        """Baixa a midia de uma mensagem."""

        return self._transport.post(f"/api/v1/{instance_id}/message/download", data)

    def mark_messages_read(self, instance_id: str, data: MarkMessagesReadRequest) -> JsonValue:
        """Marca mensagens como lidas."""

        return self._transport.post(f"/api/v1/{instance_id}/message/markread", data)

    def presence(self, instance_id: str, data: PresenceRequest) -> JsonValue:
        """Envia indicador de digitacao ou gravacao."""

        return self._transport.post(f"/api/v1/{instance_id}/message/presence", data)

    def history_sync(self, instance_id: str, data: HistorySyncRequest | None = None) -> JsonValue:
        """Sincroniza mensagens antigas de uma conversa."""

        return self._transport.post(f"/api/v1/{instance_id}/message/history-sync", data)

    def react_message(self, instance_id: str, data: ReactionMessage) -> JsonValue:
        """Reage com emoji a uma mensagem existente."""

        return self._transport.post(f"/api/v1/{instance_id}/message/react", data)
