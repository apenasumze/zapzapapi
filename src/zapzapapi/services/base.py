"""Base dos serviços da ZapZapApi."""

from __future__ import annotations

from zapzapapi.transport import ZapZapTransport


class BaseService:
    """Classe base para serviços HTTP."""

    def __init__(self, transport: ZapZapTransport) -> None:
        self._transport = transport

