"""Cliente Python para integração com a ZapZapApi."""

from zapzapapi.client import ZapZapClient
from zapzapapi.exceptions import (
    ZapZapAPIError,
    ZapZapAuthenticationError,
    ZapZapNotFoundError,
    ZapZapRateLimitError,
    ZapZapValidationError,
)

__all__ = [
    "ZapZapAPIError",
    "ZapZapAuthenticationError",
    "ZapZapClient",
    "ZapZapNotFoundError",
    "ZapZapRateLimitError",
    "ZapZapValidationError",
]

