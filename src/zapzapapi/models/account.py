"""Contratos de conta."""

from __future__ import annotations

from zapzapapi.models.base import BaseModel


class AccountResponse(BaseModel):
    """Dados principais da conta ZapZapApi."""

    id: str # Identificador único da conta
    name: str # Nome da conta
    email: str # Email da conta
    balance: str # Saldo da conta.
    billing_day: int # Dia do mês em que  é feito a cobrança da fatura
    status: str # Status da conta

