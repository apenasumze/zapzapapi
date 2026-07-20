"""Serviço de envio de mensagens."""

from __future__ import annotations

from zapzapapi.models.base import JsonValue
from zapzapapi.models.chat import ReactionMessage
from zapzapapi.models.messages import (
    ButtonsMessage,
    CarouselMessage,
    ContactMessage,
    ListMessage,
    LocationButtonMessage,
    LocationMessage,
    MediaMessage,
    PixButtonMessage,
    PollMessage,
    RequestPaymentMessage,
    StatusMessage,
    TextMessage,
)
from zapzapapi.services.base import BaseService


class MessagesService(BaseService):
    """Operações de envio de mensagens."""

    def send_text(self, instance_id: str, message: TextMessage) -> JsonValue:
        """Envia uma mensagem de texto.

        Args:
            instance_id: Identificador da instância.
            message: Contrato da mensagem de texto.
        """

        return self._transport.post(f"/api/v1/{instance_id}/send/text", message)

    def send_media(self, instance_id: str, message: MediaMessage) -> JsonValue:
        """Envia uma mensagem de mídia."""

        return self._transport.post(f"/api/v1/{instance_id}/send/media", message)

    def send_contact(self, instance_id: str, message: ContactMessage) -> JsonValue:
        """Envia um contato em formato vCard."""

        return self._transport.post(f"/api/v1/{instance_id}/send/contact", message)

    def send_location(self, instance_id: str, message: LocationMessage) -> JsonValue:
        """Envia uma localização."""

        return self._transport.post(f"/api/v1/{instance_id}/send/location", message)

    def request_location(self, instance_id: str, message: LocationButtonMessage) -> JsonValue:
        """Solicita a localização do destinatário."""

        return self._transport.post(f"/api/v1/{instance_id}/send/location-button", message)

    def send_buttons(self, instance_id: str, message: ButtonsMessage) -> JsonValue:
        """Envia uma mensagem com botões de resposta."""

        return self._transport.post(f"/api/v1/{instance_id}/send/buttons", message)

    def send_list(self, instance_id: str, message: ListMessage) -> JsonValue:
        """Envia uma lista de opções."""

        return self._transport.post(f"/api/v1/{instance_id}/send/list", message)

    def send_poll(self, instance_id: str, message: PollMessage) -> JsonValue:
        """Envia uma enquete."""

        return self._transport.post(f"/api/v1/{instance_id}/send/poll", message)

    def send_carousel(self, instance_id: str, message: CarouselMessage) -> JsonValue:
        """Envia um carrossel."""

        return self._transport.post(f"/api/v1/{instance_id}/send/carousel", message)

    def send_pix_button(self, instance_id: str, message: PixButtonMessage) -> JsonValue:
        """Envia um botão PIX."""

        return self._transport.post(f"/api/v1/{instance_id}/send/pix-button", message)

    def request_payment(self, instance_id: str, message: RequestPaymentMessage) -> JsonValue:
        """Solicita um pagamento."""

        return self._transport.post(f"/api/v1/{instance_id}/send/request-payment", message)

    def send_reaction(self, instance_id: str, message: ReactionMessage) -> JsonValue:
        """Envia uma reacao com emoji para uma mensagem existente."""

        return self._transport.post(f"/api/v1/{instance_id}/message/react", message)

    def send_status(self, instance_id: str, message: StatusMessage) -> JsonValue:
        """Envia um status/story."""

        return self._transport.post(f"/api/v1/{instance_id}/send/status", message)
