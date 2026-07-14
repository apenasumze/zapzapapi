"""Exceções próprias da ZapZapApi Python Client."""

from __future__ import annotations

from typing import Any


class ZapZapAPIError(Exception):
    """Erro base para falhas retornadas pela ZapZapApi.

    Args:
        message: Mensagem resumida do erro.
        status_code: Código HTTP retornado pela API, quando disponível.
        method: Método HTTP usado na requisição.
        url: URL chamada.
        response_body: Corpo retornado pela API, quando disponível.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        method: str | None = None,
        url: str | None = None,
        response_body: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.method = method
        self.url = url
        self.response_body = response_body


class ZapZapAuthenticationError(ZapZapAPIError):
    """Erro de autenticação ou autorização."""


class ZapZapNotFoundError(ZapZapAPIError):
    """Erro para recurso não encontrado."""


class ZapZapValidationError(ZapZapAPIError):
    """Erro de validação de dados enviados à API."""


class ZapZapRateLimitError(ZapZapAPIError):
    """Erro para limite de requisições excedido."""

