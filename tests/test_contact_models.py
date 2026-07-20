from __future__ import annotations

from zapzapapi.models.contacts import (
    AddContactRequest,
    CheckNumbersRequest,
    ContactDetailsRequest,
    ListContactsRequest,
    RemoveContactRequest,
)


def test_check_numbers_payload_preserves_numbers_as_json_array() -> None:
    request = CheckNumbersRequest(numbers=["5511999999999", "5521888888888"])

    assert request.to_payload() == {"numbers": ["5511999999999", "5521888888888"]}


def test_check_numbers_payload_accepts_legacy_raw_string() -> None:
    request = CheckNumbersRequest(numbers='["5511999999999"]')

    assert request.to_payload() == {"numbers": ["5511999999999"]}


def test_contact_details_payload_serializes_preview_boolean() -> None:
    request = ContactDetailsRequest(number="5511999999999", preview=True)

    assert request.to_payload() == {
        "number": "5511999999999",
        "preview": "true",
    }


def test_contact_agenda_payloads_preserve_documented_fields() -> None:
    add = AddContactRequest(phone="5511999999999", name="Joao Silva")
    remove = RemoveContactRequest(number="5511999999999")
    list_contacts = ListContactsRequest(limit=50, offset=0)

    assert add.to_payload() == {"phone": "5511999999999", "name": "Joao Silva"}
    assert remove.to_payload() == {"number": "5511999999999"}
    assert list_contacts.to_payload() == {"limit": 50, "offset": 0}
