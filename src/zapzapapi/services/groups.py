"""Servico de grupos e comunidades."""

from __future__ import annotations

from zapzapapi.models.base import JsonValue
from zapzapapi.models.groups import (
    CreateGroupRequest,
    GroupInfoRequest,
    GroupInviteInfoRequest,
    JoinGroupRequest,
    LeaveGroupRequest,
    ListGroupsRequest,
    ResetGroupInviteCodeRequest,
    UpdateGroupAnnounceRequest,
    UpdateGroupDescriptionRequest,
    UpdateGroupImageRequest,
    UpdateGroupLockedRequest,
    UpdateGroupNameRequest,
    UpdateGroupParticipantsRequest,
)
from zapzapapi.services.base import BaseService


class GroupsService(BaseService):
    """Operacoes sobre grupos e comunidades."""

    def create(self, instance_id: str, data: CreateGroupRequest) -> JsonValue:
        """Cria um grupo."""

        return self._transport.post(f"/api/v1/{instance_id}/group/create", data)

    def info(self, instance_id: str, data: GroupInfoRequest) -> JsonValue:
        """Consulta informacoes de um grupo."""

        return self._transport.post(f"/api/v1/{instance_id}/group/info", data)

    def invite_info(self, instance_id: str, data: GroupInviteInfoRequest) -> JsonValue:
        """Consulta informacoes de grupo por convite."""

        return self._transport.post(f"/api/v1/{instance_id}/group/inviteInfo", data)

    def join(self, instance_id: str, data: JoinGroupRequest) -> JsonValue:
        """Entra em um grupo via convite."""

        return self._transport.post(f"/api/v1/{instance_id}/group/join", data)

    def leave(self, instance_id: str, data: LeaveGroupRequest) -> JsonValue:
        """Sai de um grupo."""

        return self._transport.post(f"/api/v1/{instance_id}/group/leave", data)

    def list(self, instance_id: str) -> JsonValue:
        """Lista grupos rapidamente."""

        return self._transport.get(f"/api/v1/{instance_id}/group/list")

    def search(self, instance_id: str, filters: ListGroupsRequest | None = None) -> JsonValue:
        """Busca grupos com opcoes adicionais."""

        return self._transport.post(f"/api/v1/{instance_id}/group/list", filters)

    def reset_invite_code(
        self,
        instance_id: str,
        data: ResetGroupInviteCodeRequest,
    ) -> JsonValue:
        """Reseta o codigo de convite de um grupo."""

        return self._transport.post(f"/api/v1/{instance_id}/group/resetInviteCode", data)

    def update_announce(self, instance_id: str, data: UpdateGroupAnnounceRequest) -> JsonValue:
        """Altera o modo somente admins de um grupo."""

        return self._transport.post(f"/api/v1/{instance_id}/group/updateAnnounce", data)

    def update_description(
        self,
        instance_id: str,
        data: UpdateGroupDescriptionRequest,
    ) -> JsonValue:
        """Altera a descricao de um grupo."""

        return self._transport.post(f"/api/v1/{instance_id}/group/updateDescription", data)

    def update_image(self, instance_id: str, data: UpdateGroupImageRequest) -> JsonValue:
        """Altera a foto de um grupo."""

        return self._transport.post(f"/api/v1/{instance_id}/group/updateImage", data)

    def update_locked(self, instance_id: str, data: UpdateGroupLockedRequest) -> JsonValue:
        """Bloqueia ou libera a edicao de um grupo."""

        return self._transport.post(f"/api/v1/{instance_id}/group/updateLocked", data)

    def update_name(self, instance_id: str, data: UpdateGroupNameRequest) -> JsonValue:
        """Renomeia um grupo."""

        return self._transport.post(f"/api/v1/{instance_id}/group/updateName", data)

    def update_participants(
        self,
        instance_id: str,
        data: UpdateGroupParticipantsRequest,
    ) -> JsonValue:
        """Gerencia participantes de um grupo."""

        return self._transport.post(f"/api/v1/{instance_id}/group/updateParticipants", data)
