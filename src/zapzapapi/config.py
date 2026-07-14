"""Configuração do client ZapZapApi."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ZapZapConfig:
    """Configuração imutável usada pelo client.

    Args:
        api_key: Chave pública da API.
        api_secret: Chave secreta da API.
        base_url: URL base da ZapZapApi.
        timeout: Timeout de cada requisição em segundos.
    """

    api_key: str
    api_secret: str
    base_url: str = "https://app.zapzapapi.com"
    timeout: float = 30.0

    def normalized_base_url(self) -> str:
        """Retorna a URL base sem barra final."""

        return self.base_url.rstrip("/")
