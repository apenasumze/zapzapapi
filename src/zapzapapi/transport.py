"""Transporte HTTP central da ZapZapApi."""

from __future__ import annotations

from typing import cast

import httpx

from zapzapapi.config import ZapZapConfig
from zapzapapi.exceptions import (
    ZapZapAPIError,
    ZapZapAuthenticationError,
    ZapZapNotFoundError,
    ZapZapRateLimitError,
    ZapZapValidationError,
)
from zapzapapi.models.base import BaseModel, JsonObject, JsonValue


class ZapZapTransport:
    """Executa requisições HTTP contra a ZapZapApi.

    Cada chamada de método público executa uma única requisição HTTP e devolve a resposta ou lança
    uma exceção tipada.

    Args:
        config: Configuração imutável do client.
        http_client: Client HTTP opcional, útil para testes.
    """

    def __init__(
        self,
        config: ZapZapConfig,
        *,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._config = config
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(timeout=config.timeout)

    def close(self) -> None:
        """Fecha o client HTTP quando ele foi criado pela própria biblioteca."""

        if self._owns_client:
            self._client.close()

    def get(self, endpoint: str) -> JsonValue:
        """Executa uma requisição GET sem retry."""

        return self.request("GET", endpoint)

    def post(self, endpoint: str, payload: BaseModel | JsonObject | None = None) -> JsonValue:
        """Executa uma requisição POST sem retry."""

        return self.request("POST", endpoint, payload=payload)

    def put(self, endpoint: str, payload: BaseModel | JsonObject | None = None) -> JsonValue:
        """Executa uma requisição PUT sem retry."""

        return self.request("PUT", endpoint, payload=payload)

    def delete(self, endpoint: str) -> JsonValue:
        """Executa uma requisição DELETE sem retry."""

        return self.request("DELETE", endpoint)

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        payload: BaseModel | JsonObject | None = None,
    ) -> JsonValue:
        """Executa uma única requisição HTTP.

        Args:
            method: Método HTTP.
            endpoint: Caminho relativo da API.
            payload: Contrato ou dicionário a ser enviado como JSON.

        Returns:
            Corpo da resposta convertido de JSON quando possível.

        Raises:
            ZapZapAPIError: Quando a API retorna erro HTTP.
        """

        url = self._build_url(endpoint)
        response = self._client.request(
            method=method,
            url=url,
            headers=self._headers(),
            json=self._payload_to_json(payload),
        )
        return self._handle_response(response, method=method, url=url)

    def _build_url(self, endpoint: str) -> str:
        normalized_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        return f"{self._config.normalized_base_url()}{normalized_endpoint}"

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key": self._config.api_key,
            "x-api-secret": self._config.api_secret,
        }

    def _payload_to_json(self, payload: BaseModel | JsonObject | None) -> JsonObject | None:
        if payload is None:
            return None
        if isinstance(payload, BaseModel):
            return payload.to_payload()
        return payload

    def _handle_response(self, response: httpx.Response, *, method: str, url: str) -> JsonValue:
        body = self._response_body(response)
        if response.is_success:
            return body

        error_cls: type[ZapZapAPIError]
        if response.status_code in {401, 403}:
            error_cls = ZapZapAuthenticationError
        elif response.status_code == 404:
            error_cls = ZapZapNotFoundError
        elif response.status_code in {400, 422}:
            error_cls = ZapZapValidationError
        elif response.status_code == 429:
            error_cls = ZapZapRateLimitError
        else:
            error_cls = ZapZapAPIError

        raise error_cls(
            f"Erro na requisição ZapZapApi: HTTP {response.status_code}.",
            status_code=response.status_code,
            method=method,
            url=url,
            response_body=body,
        )

    def _response_body(self, response: httpx.Response) -> JsonValue:
        if not response.content:
            return None
        try:
            return cast(JsonValue, response.json())
        except ValueError:
            return response.text
