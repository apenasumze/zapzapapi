from __future__ import annotations

import json

import httpx

from zapzapapi import ZapZapClient
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


def test_groups_service_covers_group_routes() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"ok": True})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = ZapZapClient(api_key="key", api_secret="secret", http_client=http_client)
    group_jid = "120363000000000000@g.us"

    assert client.groups.create(
        "instance-1",
        CreateGroupRequest(name="Meu Time", participants=["5511999990001"]),
    ) == {"ok": True}
    assert client.groups.info(
        "instance-1",
        GroupInfoRequest(group_jid=group_jid, get_invite_link=True),
    ) == {"ok": True}
    assert client.groups.invite_info(
        "instance-1",
        GroupInviteInfoRequest(invite_code="ABC123"),
    ) == {"ok": True}
    assert client.groups.join(
        "instance-1",
        JoinGroupRequest(invite_code="https://chat.whatsapp.com/ABC123"),
    ) == {"ok": True}
    assert client.groups.leave("instance-1", LeaveGroupRequest(group_jid=group_jid)) == {
        "ok": True,
    }
    assert client.groups.list("instance-1") == {"ok": True}
    assert client.groups.search("instance-1", ListGroupsRequest(get_participants=False)) == {
        "ok": True,
    }
    assert client.groups.reset_invite_code(
        "instance-1",
        ResetGroupInviteCodeRequest(group_jid=group_jid),
    ) == {"ok": True}
    assert client.groups.update_announce(
        "instance-1",
        UpdateGroupAnnounceRequest(group_jid=group_jid, announce=True),
    ) == {"ok": True}
    assert client.groups.update_description(
        "instance-1",
        UpdateGroupDescriptionRequest(group_jid=group_jid, description="Descricao"),
    ) == {"ok": True}
    assert client.groups.update_image(
        "instance-1",
        UpdateGroupImageRequest(group_jid=group_jid, image="remove"),
    ) == {"ok": True}
    assert client.groups.update_locked(
        "instance-1",
        UpdateGroupLockedRequest(group_jid=group_jid, locked=False),
    ) == {"ok": True}
    assert client.groups.update_name(
        "instance-1",
        UpdateGroupNameRequest(group_jid=group_jid, name="Novo Nome"),
    ) == {"ok": True}
    assert client.groups.update_participants(
        "instance-1",
        UpdateGroupParticipantsRequest(
            group_jid=group_jid,
            action=GroupParticipantAction.ADD,
            participants=["5511999990002"],
        ),
    ) == {"ok": True}

    assert [(call.method, call.url.path) for call in calls] == [
        ("POST", "/api/v1/instance-1/group/create"),
        ("POST", "/api/v1/instance-1/group/info"),
        ("POST", "/api/v1/instance-1/group/inviteInfo"),
        ("POST", "/api/v1/instance-1/group/join"),
        ("POST", "/api/v1/instance-1/group/leave"),
        ("GET", "/api/v1/instance-1/group/list"),
        ("POST", "/api/v1/instance-1/group/list"),
        ("POST", "/api/v1/instance-1/group/resetInviteCode"),
        ("POST", "/api/v1/instance-1/group/updateAnnounce"),
        ("POST", "/api/v1/instance-1/group/updateDescription"),
        ("POST", "/api/v1/instance-1/group/updateImage"),
        ("POST", "/api/v1/instance-1/group/updateLocked"),
        ("POST", "/api/v1/instance-1/group/updateName"),
        ("POST", "/api/v1/instance-1/group/updateParticipants"),
    ]
    assert json.loads(calls[0].read()) == {
        "name": "Meu Time",
        "participants": ["5511999990001"],
    }
    assert json.loads(calls[1].read()) == {
        "groupjid": group_jid,
        "getInviteLink": "true",
    }
    assert json.loads(calls[6].read()) == {"getParticipants": "false"}
    assert json.loads(calls[13].read()) == {
        "groupjid": group_jid,
        "action": "add",
        "participants": ["5511999990002"],
    }
