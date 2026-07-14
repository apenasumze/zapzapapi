"""Base dos contratos da ZapZapApi."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict

JsonObject = dict[str, Any]
JsonValue = dict[str, Any] | list[Any] | str | int | float | bool | None


class BaseModel(PydanticBaseModel):
    """Modelo base dos contratos públicos da biblioteca."""

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        use_enum_values=True,
    )

    def to_payload(self) -> JsonObject:
        """Converte o contrato para o payload esperado pela API.

        Returns:
            Dicionário pronto para envio como JSON.
        """

        return self.model_dump(by_alias=True, exclude_none=True)
