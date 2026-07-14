"""Contratos de conta."""

from __future__ import annotations

from decimal import Decimal

from zapzapapi.models.base import BaseModel


class AccountResponse(BaseModel):
    """Dados principais da conta ZapZapApi."""

    id: str
    name: str | None = None
    email: str | None = None
    balance: Decimal | str | None = None
    billing_day: int | None = None
    status: str | None = None

