from __future__ import annotations

from zapzapapi.models.groups import (
    CreateGroupRequest,
    GroupInfoRequest,
    GroupInviteInfoRequest,
    GroupParticipantAction,
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


def test_create_group_payload_preserves_participants_as_json_array() -> None:
    request = CreateGroupRequest(
        name="Meu Time",
        participants=["5511999990001", "5511999990002"],
    )

    assert request.to_payload() == {
        "name": "Meu Time",
        "participants": ["5511999990001", "5511999990002"],
    }


def test_create_group_payload_accepts_legacy_raw_participants_string() -> None:
    request = CreateGroupRequest(
        name="Meu Time",
        participants='["5511999990001","5511999990002"]',
    )

    assert request.to_payload() == {
        "name": "Meu Time",
        "participants": ["5511999990001", "5511999990002"],
    }


def test_group_lookup_payloads_use_api_aliases() -> None:
    info = GroupInfoRequest(group_jid="120363000000000000@g.us", get_invite_link=True)
    invite_info = GroupInviteInfoRequest(invite_code="ABC123")
    join = JoinGroupRequest(invite_code="https://chat.whatsapp.com/ABC123")
    leave = LeaveGroupRequest(group_jid="120363000000000000@g.us")
    reset = ResetGroupInviteCodeRequest(group_jid="120363000000000000@g.us")

    assert info.to_payload() == {
        "groupjid": "120363000000000000@g.us",
        "getInviteLink": "true",
    }
    assert invite_info.to_payload() == {"invitecode": "ABC123"}
    assert join.to_payload() == {"invitecode": "https://chat.whatsapp.com/ABC123"}
    assert leave.to_payload() == {"groupjid": "120363000000000000@g.us"}
    assert reset.to_payload() == {"groupjid": "120363000000000000@g.us"}


def test_list_groups_payload_serializes_get_participants_boolean() -> None:
    request = ListGroupsRequest(get_participants=False)

    assert request.to_payload() == {"getParticipants": "false"}


def test_group_update_payloads_preserve_aliases_and_boolean_strings() -> None:
    announce = UpdateGroupAnnounceRequest(
        group_jid="120363000000000000@g.us",
        announce=True,
    )
    description = UpdateGroupDescriptionRequest(
        group_jid="120363000000000000@g.us",
        description="Descricao do grupo",
    )
    image = UpdateGroupImageRequest(
        group_jid="120363000000000000@g.us",
        image="remove",
    )
    locked = UpdateGroupLockedRequest(group_jid="120363000000000000@g.us", locked=False)
    name = UpdateGroupNameRequest(group_jid="120363000000000000@g.us", name="Novo Nome")

    assert announce.to_payload() == {
        "groupjid": "120363000000000000@g.us",
        "announce": "true",
    }
    assert description.to_payload() == {
        "groupjid": "120363000000000000@g.us",
        "description": "Descricao do grupo",
    }
    assert image.to_payload() == {
        "groupjid": "120363000000000000@g.us",
        "image": "remove",
    }
    assert locked.to_payload() == {
        "groupjid": "120363000000000000@g.us",
        "locked": "false",
    }
    assert name.to_payload() == {
        "groupjid": "120363000000000000@g.us",
        "name": "Novo Nome",
    }


def test_update_group_participants_payload_uses_closed_action_enum() -> None:
    request = UpdateGroupParticipantsRequest(
        group_jid="120363000000000000@g.us",
        action=GroupParticipantAction.PROMOTE,
        participants=["5511999990003"],
    )

    assert request.to_payload() == {
        "groupjid": "120363000000000000@g.us",
        "action": "promote",
        "participants": ["5511999990003"],
    }
