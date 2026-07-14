"""Contratos de envio de mensagens."""

from __future__ import annotations

from enum import Enum

from pydantic import Field

from zapzapapi.models.base import BaseModel


class MediaType(str, Enum):
    """Tipos de mídia aceitos pelo endpoint de envio de mídia."""

    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"


class StatusType(str, Enum):
    """Tipos aceitos pelo endpoint de status/story."""

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    
    
class FontType(Enum):
    SERIF = 1
    NORICAN_REGULAR = 2
    BRYNDAN_WRITE = 3
    BEBASNEUE_REGULAR = 4
    OSWALD_HEAVY = 5


class BaseMessage(BaseModel):
    """Campos comuns de mensagens destinadas a um número.

    Args:
        number: Número do destinatário em formato aceito pela ZapZapApi.
        delay: Atraso opcional em milissegundos.
        reply_id: Identificador da mensagem respondida.
    """

    number: str
    delay: int = 1000
    reply_id: str | None = Field(default=None, alias="replyid")


class MentionableMessage(BaseMessage):
    """Mensagem que pode mencionar contatos."""

    mentions: list[str] | None = None


class TextMessage(BaseMessage):
    """Mensagem de texto simples."""

    text: str


class MediaMessage(MentionableMessage):
    """Mensagem com mídia.

    Args:
        number: Número do destinatário.
        type: Tipo de mídia.
        file: URL ou conteúdo aceito pela API.
        text: Legenda opcional.
        doc_name: Nome do documento, quando aplicável.
    """

    type: MediaType
    file: str
    text: str | None = None
    doc_name: str | None = Field(default=None, alias="docName")


class ContactMessage(BaseMessage):
    """Mensagem de contato em formato vCard."""

    full_name: str = Field(alias="fullName")
    phone_number: str = Field(alias="phoneNumber")
    organization: str | None = None
    email: str | None = None


class LocationMessage(BaseMessage):
    """Mensagem de localização."""

    latitude: float
    longitude: float
    name: str | None = None
    address: str | None = None


class LocationButtonMessage(BaseModel):
    """Mensagem que solicita o envio de localização pelo destinatário."""

    number: str
    text: str


class Button(BaseModel):
    """Botão de resposta."""

    id: str
    text: str


class ButtonsMessage(BaseMessage):
    """Mensagem com botões de resposta."""

    text: str
    buttons: list[Button]
    image: str | None = None
    footer: str | None = None


class ListChoice(BaseModel):
    """Opção exibida em mensagem de lista."""

    id: str
    title: str
    description: str | None = None


class ListMessage(BaseModel):
    """Mensagem com lista de opções."""

    number: str
    text: str
    choices: list[ListChoice]
    list_button: str | None = Field(default=None, alias="listButton")
    footer_text: str | None = Field(default=None, alias="footerText")


class PollMessage(BaseModel):
    """Mensagem de enquete."""

    number: str
    text: str
    choices: list[str]
    selectable_count: int | None = Field(default=None, alias="selectableCount")


class CarouselCard(BaseModel):
    """Card de carrossel."""

    title: str
    text: str | None = None
    image: str | None = None
    buttons: list[Button] | None = None


class CarouselMessage(BaseModel):
    """Mensagem de carrossel."""

    number: str
    text: str
    carousel: list[CarouselCard]
    delay: int | None = None


class PixButtonMessage(BaseMessage):
    """Mensagem com botão PIX."""

    pix_type: str = Field(alias="pixType")
    pix_key: str = Field(alias="pixKey")
    pix_name: str | None = Field(default=None, alias="pixName")
    async_: bool | None = Field(default=None, alias="async")
    read_chat: bool | None = Field(default=None, alias="readchat")
    read_messages: bool | None = Field(default=None, alias="readmessages")
    mentions: list[str] | None = None
    track_source: str | None = None
    track_id: str | None = None


class RequestPaymentMessage(BaseModel):
    """Mensagem de solicitação de pagamento."""

    number: str
    amount: float
    pix_key: str | None = Field(default=None, alias="pixKey")
    pix_type: str | None = Field(default=None, alias="pixType")
    item_name: str | None = Field(default=None, alias="itemName")
    invoice_number: str | None = Field(default=None, alias="invoiceNumber")
    title: str | None = None
    footer: str | None = None
    pix_name: str | None = Field(default=None, alias="pixName")
    text: str | None = None
    payment_link: str | None = Field(default=None, alias="paymentLink")
    file_url: str | None = Field(default=None, alias="fileUrl")
    file_name: str | None = Field(default=None, alias="fileName")
    boleto_code: str | None = Field(default=None, alias="boletoCode")
    allow_cards: bool | None = Field(default=None, alias="allowCards")
    currency: str | None = None
    note: str | None = None


class StatusMessage(BaseModel):
    """Mensagem de status/story."""

    type: StatusType
    text: str | None = None
    background_color: str | None = None
    font: str | None = None
    file: str | None = None
