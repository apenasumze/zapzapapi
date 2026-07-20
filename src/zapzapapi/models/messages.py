"""Contratos de envio de mensagens."""

from __future__ import annotations

import json
from enum import Enum
from typing import Any

from pydantic import Field, field_serializer, field_validator, model_validator

from zapzapapi.models.base import BaseModel
from zapzapapi.models.chat import ReactionMessage as ReactionMessage


class MediaType(str, Enum):
    """Tipos de midia aceitos pelo endpoint de envio de midia."""

    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    PTT = "ptt"
    MYAUDIO = "myaudio"
    PTV = "ptv"
    DOCUMENT = "document"
    STICKER = "sticker"


class StatusType(str, Enum):
    """Tipos aceitos pelo endpoint de status/story."""

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    PTT = "ptt"


class FontType(str, Enum):
    """Fontes aceitas pelo endpoint de status/story."""

    SANS_SERIF = "0"
    SERIF = "1"
    NORICAN = "2"
    BRYNDAN = "3"
    BEBAS_NEUE = "4"
    FUTURA_PT = "5"
    ESTILO_6 = "6"
    ESTILO_7 = "7"
    ESTILO_8 = "8"


class StatusBackgroundColor(str, Enum):
    """Cores de fundo aceitas pelo endpoint de status/story."""

    AMARELO = "1"
    AMARELO_MEDIO = "2"
    AMARELO_ESCURO = "3"
    VERDE_CLARO = "4"
    VERDE = "5"
    VERDE_ESCURO = "6"
    AZUL_CLARO = "7"
    AZUL = "8"
    AZUL_ESCURO = "9"
    LILAS_CLARO = "10"
    LILAS = "11"
    LILAS_ESCURO = "12"
    MAGENTA = "13"
    ROSA_CLARO = "14"
    ROSA = "15"
    MARROM_CLARO = "16"
    CINZA_CLARO = "17"
    CINZA = "18"
    CINZA_ESCURO = "19"


class PixType(str, Enum):
    """Tipos de chave PIX aceitos pela API."""

    EMAIL = "EMAIL"
    CPF = "CPF"
    CNPJ = "CNPJ"
    PHONE = "PHONE"
    EVP = "EVP"


class QuotedMessage(BaseModel):
    """Mensagem citada/respondida em payloads que aceitam objeto quoted."""

    key: dict[str, Any]
    message: dict[str, Any] | None = None


class BaseMessage(BaseModel):
    """Campos comuns de mensagens destinadas a um numero."""

    number: str
    delay: int | None = 1000
    reply_id: str | None = Field(default=None, alias="replyid")
    quoted: QuotedMessage | None = None


class TextMessage(BaseMessage):
    """Mensagem de texto simples."""

    text: str
    link_preview: bool | None = Field(default=None, alias="linkPreview")
    mentions_every_one: bool | None = Field(default=None, alias="mentionsEveryOne")
    mentioned: list[str] | None = None


class MediaMessage(BaseMessage):
    """Mensagem com midia."""

    type: MediaType
    file: str  # URL ou caminho do arquivo
    caption: str | None = Field(default=None, alias="text")  # Legenda do arquivo
    # Nome do arquivo, obrigatorio para documentos.
    file_name: str | None = Field(default=None, alias="docName")
    mentions: list[str] | None = None


class ContactMessage(BaseMessage):
    """Mensagem de contato em formato vCard."""

    full_name: str = Field(alias="fullName")
    phone_number: str = Field(alias="phoneNumber")
    organization: str | None = None
    email: str | None = None


class LocationMessage(BaseMessage):
    """Mensagem de localizacao."""

    latitude: float
    longitude: float
    name: str | None = None
    address: str | None = None


class LocationButtonMessage(BaseMessage):
    """Mensagem que solicita o envio de localizacao pelo destinatario."""

    text: str


class Button(BaseModel):
    """Botao usado no endpoint de envio de botoes."""

    text: str = Field(min_length=1)
    id: str | None = Field(default=None, min_length=1)
    url: str | None = Field(default=None, min_length=1)
    phone: str | None = Field(default=None, min_length=1)
    copy_code: str | None = Field(default=None, alias="copy", min_length=1)

    @classmethod
    def reply(cls, *, text: str, id: str) -> Button:
        """Cria um botao de resposta automatica."""

        return cls(text=text, id=id)

    @classmethod
    def link(cls, *, text: str, url: str) -> Button:
        """Cria um botao de reposta para um link externo."""

        return cls(text=text, url=url)

    @classmethod
    def call(cls, *, text: str, phone: str) -> Button:
        """Cria um botao de ligacao."""

        return cls(text=text, phone=phone)

    @classmethod
    def copy_text(cls, *, text: str, copy_code: str) -> Button:
        """Cria um botao para copiar texto/codigo."""

        return cls(text=text, copy=copy_code)

    @model_validator(mode="after")
    def _validate_single_action(self) -> Button:
        actions = {
            "id": self.id,
            "url": self.url,
            "phone": self.phone,
            "copy": self.copy_code,
        }
        configured_actions = [
            action for action, value in actions.items() if value is not None
        ]
        if len(configured_actions) != 1:
            raise ValueError("Button must define exactly one action: id, url, phone or copy")
        return self


def _button_payload(button: Button) -> dict[str, Any]:
    raw_payload = button.to_payload()
    ordered_keys = ("text", "id", "url", "phone", "copy")
    return {key: raw_payload[key] for key in ordered_keys if key in raw_payload}


class ButtonsMessage(BaseMessage):
    """Mensagem com botoes de resposta."""

    text: str
    buttons: list[Button]
    image: str | None = None # Opcional, se definido envia uma imagem junto com os botoes.
    footer: str | None = None # Opcional, se definido envia um rodape junto com os botoes.

    @field_validator("buttons", mode="before")
    @classmethod
    def _normalize_buttons(cls, buttons: object) -> object:
        if isinstance(buttons, str):
            return json.loads(buttons)
        return buttons

    @field_validator("buttons")
    @classmethod
    def _validate_buttons_count(cls, buttons: list[Button]) -> list[Button]:
        if not buttons:
            raise ValueError("ButtonsMessage must define at least one button")
        if len(buttons) > 3: # Limitação da API ZapZap.
            raise ValueError("ButtonsMessage accepts up to 3 buttons")
        return buttons

    @field_serializer("buttons")
    def _serialize_buttons(self, buttons: list[Button]) -> list[dict[str, Any]]:
        return [_button_payload(button) for button in buttons]


class ListChoice(BaseModel):
    """Opcao exibida em mensagem de lista."""

    item: str = Field(min_length=1)
    id: str | None = Field(default=None, min_length=1)
    description: str | None = None


def _list_choice_value(choice: ListChoice) -> str:
    parts = [choice.item]
    if choice.id is not None:
        parts.append(choice.id)
    if choice.description is not None:
        if choice.id is None:
            parts.append("")
        parts.append(choice.description)
    return "|".join(parts)


class ListMessage(BaseMessage):
    """Mensagem com lista de opcoes."""

    delay: int | None = None
    text: str  # Texto principal da mensagem. Ex.: "Escolha uma das opcoes abaixo:"
    category: str | None = Field(
        default=None,
        min_length=1,
        exclude=True,
    )
    choices: list[ListChoice] | list[str]
    list_button: str | None = Field(default=None, alias="listButton")
    footer_text: str | None = Field(default=None, alias="footerText")

    @field_validator("choices", mode="before")
    @classmethod
    def _normalize_choices(cls, choices: object) -> object:
        if isinstance(choices, str):
            return json.loads(choices)
        return choices

    @model_validator(mode="after")
    def _validate_category_for_typed_choices(self) -> ListMessage:
        if self.category is None and any(
            isinstance(choice, ListChoice) for choice in self.choices
        ):
            raise ValueError("ListMessage.category is required when choices use ListChoice")
        return self

    @field_serializer("choices")
    def _serialize_choices(
        self, choices: list[ListChoice] | list[str]
    ) -> list[str]:
        serialized_choices = [
            _list_choice_value(choice) if isinstance(choice, ListChoice) else choice
            for choice in choices
        ]
        if self.category is None:
            return serialized_choices
        category_value = f"[{self.category}]"
        if serialized_choices and serialized_choices[0] == category_value:
            return serialized_choices
        return [category_value, *serialized_choices]


class PollMessage(BaseMessage):
    """Mensagem de enquete."""

    delay: int | None = None
    text: str
    choices: list[str] | str
    selectable_count: int | str | None = Field(default=None, alias="selectableCount")

    @field_serializer("choices")
    def _serialize_choices(self, choices: list[str] | str) -> str:
        if isinstance(choices, str):
            return choices
        return json.dumps(choices, ensure_ascii=False, separators=(",", ":"))

    @field_serializer("selectable_count")
    def _serialize_selectable_count(self, selectable_count: int | str | None) -> str | None:
        if selectable_count is None:
            return None
        return str(selectable_count)


class CarouselButtonType(str, Enum):
    """Tipos confirmados de botao em cards de carrossel."""

    REPLY = "REPLY"


class CarouselButton(BaseModel):
    """Botao usado dentro de um card de carrossel."""

    text: str
    id: str
    type: CarouselButtonType = CarouselButtonType.REPLY


def _carousel_button_payload(button: CarouselButton) -> dict[str, Any]:
    raw_payload = button.to_payload()
    ordered_keys = ("type", "text", "id")
    return {key: raw_payload[key] for key in ordered_keys if key in raw_payload}


class CarouselCard(BaseModel):
    """Card de carrossel."""

    text: str
    image: str | None = None
    buttons: list[CarouselButton] | None = None


class CarouselMessage(BaseMessage):
    """Mensagem de carrossel."""

    text: str
    carousel: list[CarouselCard]

    @field_serializer("carousel")
    def _serialize_carousel(self, carousel: list[CarouselCard]) -> list[dict[str, Any]]:
        payload = []
        for card in carousel:
            card_payload = card.to_payload()
            if card.buttons is not None:
                card_payload["buttons"] = [
                    _carousel_button_payload(button) for button in card.buttons
                ]
            payload.append(card_payload)
        return payload

    @field_validator("carousel", mode="before")
    @classmethod
    def _normalize_carousel(cls, carousel: object) -> object:
        if isinstance(carousel, str):
            return json.loads(carousel)
        return carousel


class PixButtonMessage(BaseMessage):
    """Mensagem com botao PIX."""

    pix_type: PixType = Field(alias="pixType")
    pix_key: str = Field(alias="pixKey")
    pix_name: str | None = Field(default=None, alias="pixName")
    async_: bool | None = Field(default=None, alias="async")
    read_chat: bool | None = Field(default=None, alias="readchat")
    read_messages: bool | None = Field(default=None, alias="readmessages")
    mentions: str | None = None
    track_source: str | None = None
    track_id: str | None = None


class RequestPaymentMessage(BaseMessage):
    """Mensagem de solicitacao de pagamento."""

    amount: float
    pix_key: str | None = Field(default=None, alias="pixKey")
    pix_type: PixType | None = Field(default=None, alias="pixType")
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
    background_color: StatusBackgroundColor | None = None
    font: FontType | None = None
    file: str | None = None
