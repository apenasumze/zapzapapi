from __future__ import annotations

from zapzapapi.models.profile import UpdateProfileImageRequest, UpdateProfileNameRequest


def test_profile_payloads_preserve_documented_fields() -> None:
    image = UpdateProfileImageRequest(image="https://example.com/logo.jpg")
    name = UpdateProfileNameRequest(name="Minha Empresa")

    assert image.to_payload() == {"image": "https://example.com/logo.jpg"}
    assert name.to_payload() == {"name": "Minha Empresa"}
