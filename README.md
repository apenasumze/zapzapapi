# ZapZapApi Python Client

Cliente Python sincrono para integracao com a ZapZapApi.

Esta biblioteca fornece um `ZapZapClient` central, servicos por dominio e models Pydantic para
montar payloads validados antes de chamar a API.

## Instalacao

Enquanto a biblioteca nao estiver publicada no PyPI, instale a partir do repositorio local:

```powershell
pip install -e .
```

Dependencias principais:

- Python 3.10+
- `httpx`
- `pydantic v2`

## Inicializando O Client

```python
from zapzapapi import ZapZapClient

client = ZapZapClient(
    api_key="SUA_API_KEY",
    api_secret="SUA_API_SECRET",
    base_url="https://app.zapzapapi.com",
)
```

Uso com gerenciador de contexto:

```python
from zapzapapi import ZapZapClient

with ZapZapClient(
    api_key="SUA_API_KEY",
    api_secret="SUA_API_SECRET",
) as client:
    account = client.account.get()
```

## Conta

### Consultar Conta

```python
account = client.account.get()
```

## Instancias

### Listar Instancias

```python
instances = client.instances.list()
```

### Criar Instancia

```python
from zapzapapi.models.instance import CreateInstanceRequest

instance = client.instances.create(
    CreateInstanceRequest(
        name="Minha instancia",
        system_name="Meu App",
        metadata={"clientId": "123", "plan": "pro"},
    )
)
```

`system_name` gera `systemName` no payload. `metadata` pode ser informado como string JSON ja
pronta ou como dicionario; quando for dicionario, o SDK serializa para a string JSON esperada pela
API.

### Custo De Criacao

```python
cost = client.instances.cost()
```

### Consultar Instancia

```python
instance = client.instances.get("ID_DA_INSTANCIA")
```

### Atualizar Instancia

```python
from zapzapapi.models.instance import UpdateInstanceRequest

response = client.instances.update(
    "ID_DA_INSTANCIA",
    UpdateInstanceRequest(
        webhook_url="https://seu-servidor.com/webhook",
        metadata={"clientId": "123"},
    ),
)
```

A atualizacao administrativa aceita `webhook_url` e `metadata`, conforme o contrato atual da API.

### Remover Instancia

```python
response = client.instances.delete("ID_DA_INSTANCIA")
```

### QR Code

```python
qrcode = client.instances.qrcode("ID_DA_INSTANCIA")
```

### Webhook Administrativo Da Instancia

```python
from zapzapapi.models.instance import (
    ConfigureInstanceWebhookRequest,
    InstanceWebhookEvent,
    InstanceWebhookExclude,
)

config = ConfigureInstanceWebhookRequest(
    webhook_url="https://seu-servidor.com/webhook",
    events=[
        InstanceWebhookEvent.MESSAGES,
        InstanceWebhookEvent.MESSAGES_UPDATE,
        InstanceWebhookEvent.CONNECTION,
    ],
    exclude_messages=[
        InstanceWebhookExclude.WAS_SENT_BY_API,
        InstanceWebhookExclude.IS_GROUP_YES,
    ],
)

response = client.instances.configure_webhook("ID_DA_INSTANCIA", config)
webhook = client.instances.get_webhook("ID_DA_INSTANCIA")
test = client.instances.test_webhook("ID_DA_INSTANCIA")
```

`events` e `exclude_messages` aceitam enums, strings ou listas. Listas sao serializadas como texto
separado por virgula, conforme o payload externo da API.

Eventos confirmados:

- `InstanceWebhookEvent.MESSAGES`: mensagens recebidas.
- `InstanceWebhookEvent.CONNECTION`: conexao.
- `InstanceWebhookEvent.MESSAGES_UPDATE`: status de mensagens.
- `InstanceWebhookEvent.GROUPS`: grupos.
- `InstanceWebhookEvent.CHATS`: chats.
- `InstanceWebhookEvent.LEADS`: leads.
- `InstanceWebhookEvent.CONTACTS`: contatos.
- `InstanceWebhookEvent.HISTORY`: historico inicial.
- `InstanceWebhookEvent.QRCODE`: QR Code.
- `InstanceWebhookEvent.LABELS`: etiquetas.
- `InstanceWebhookEvent.PRESENCE`: presenca.
- `InstanceWebhookEvent.CHAT_LABELS`: etiquetas de chat.
- `InstanceWebhookEvent.BLOCKS`: bloqueios.
- `InstanceWebhookEvent.CALL`: chamadas.

Filtros de exclusao confirmados:

- `InstanceWebhookExclude.WAS_SENT_BY_API`: enviadas pela API.
- `InstanceWebhookExclude.WAS_NOT_SENT_BY_API`: nao enviadas pela API.
- `InstanceWebhookExclude.FROM_ME_YES`: mensagens que eu enviei.
- `InstanceWebhookExclude.FROM_ME_NO`: mensagens recebidas.
- `InstanceWebhookExclude.IS_GROUP_YES`: mensagens de grupos.
- `InstanceWebhookExclude.IS_GROUP_NO`: mensagens individuais.

Tambem e possivel testar uma URL alternativa:

```python
from zapzapapi.models.instance import TestInstanceWebhookRequest

test = client.instances.test_webhook(
    "ID_DA_INSTANCIA",
    TestInstanceWebhookRequest(url="https://seu-servidor.com/webhook-teste"),
)
```

## Envio De Mensagens

Todos os exemplos abaixo usam:

```python
instance_id = "ID_DA_INSTANCIA"
number = "5511999999999"
```

Os models de envio herdam campos comuns quando o endpoint envia para um contato:

- `number`: destinatario da mensagem.
- `delay`: atraso em milissegundos. O padrao consolidado e `1000` quando o endpoint aceita delay.
- `reply_id`: alias de payload `replyid`.
- `quoted`: objeto completo de mensagem citada/respondida.

Campos opcionais com valor `None` nao entram no payload.

### Mensagem De Texto

```python
from zapzapapi.models.message import TextMessage

message = TextMessage(
    number=number,
    text="Ola! Tudo bem?",
)

response = client.messages.send_text(instance_id, message)
```

Com delay explicito:

```python
message = TextMessage(
    number=number,
    text="Mensagem com delay customizado.",
    delay=1200,
)
```

Com link preview:

```python
message = TextMessage(
    number=number,
    text="Confira: https://exemplo.com",
    link_preview=True,
)
```

Com mencoes:

```python
message = TextMessage(
    number=number,
    text="@5511999999999 Ola!",
    mentioned=["5511999999999"],
)
```

Com citacao por `replyid`:

```python
message = TextMessage(
    number=number,
    text="Respondendo a mensagem anterior.",
    reply_id="ABCDEF123456",
)
```

Com citacao completa:

```python
from zapzapapi.models.message import QuotedMessage, TextMessage

quoted = QuotedMessage(
    key={
        "remoteJid": "5511999999999@s.whatsapp.net",
        "fromMe": False,
        "id": "ABCDEF123456",
    },
    message={"conversation": "Mensagem original"},
)

message = TextMessage(
    number=number,
    text="Esta e uma resposta.",
    quoted=quoted,
)
```

### Mensagem De Midia

```python
from zapzapapi.models.message import MediaMessage, MediaType

message = MediaMessage(
    number=number,
    type=MediaType.IMAGE,
    file="https://exemplo.com/imagem.jpg",
    caption="Legenda da imagem",
)

response = client.messages.send_media(instance_id, message)
```

Tipos de midia consolidados:

- `MediaType.IMAGE`
- `MediaType.VIDEO`
- `MediaType.AUDIO`
- `MediaType.PTT`
- `MediaType.MYAUDIO`
- `MediaType.PTV`
- `MediaType.DOCUMENT`
- `MediaType.STICKER`

Documento com nome de arquivo:

```python
message = MediaMessage(
    number=number,
    type=MediaType.DOCUMENT,
    file="https://exemplo.com/arquivo.pdf",
    caption="Documento em anexo",
    file_name="arquivo.pdf",
)
```

`caption` e `file_name` sao aliases amigaveis:

- `caption` gera `text` no payload.
- `file_name` gera `docName` no payload.

### Contato

```python
from zapzapapi.models.message import ContactMessage

message = ContactMessage(
    number=number,
    full_name="Joao Silva",
    phone_number="5511888888888",
    organization="Empresa XYZ",
    email="joao@empresa.com",
)

response = client.messages.send_contact(instance_id, message)
```

Neste contrato:

- `number` e o destinatario.
- `phone_number` gera `phoneNumber` e representa o telefone do contato enviado.

### Localizacao

```python
from zapzapapi.models.message import LocationMessage

message = LocationMessage(
    number=number,
    latitude=-23.55052,
    longitude=-46.633308,
    name="Sao Paulo",
    address="Sao Paulo, SP",
)

response = client.messages.send_location(instance_id, message)
```

### Solicitar Localizacao

```python
from zapzapapi.models.message import LocationButtonMessage

message = LocationButtonMessage(
    number=number,
    text="Compartilhe sua localizacao, por favor.",
)

response = client.messages.request_location(instance_id, message)
```

### Botoes

```python
from zapzapapi.models.message import Button, ButtonsMessage

message = ButtonsMessage(
    number=number,
    text="Como podemos ajudar?",
    buttons=[
        Button(text="Sim", id="yes"),
        Button(text="Site", url="https://exemplo.com"),
        Button(text="Ligar", phone="+5511999999999"),
        Button(text="Copiar", copy_code="ABC123"),
    ],
    footer="Escolha uma opcao",
)

response = client.messages.send_buttons(instance_id, message)
```

O SDK aceita lista de `Button` e serializa para a string JSON esperada pela API.

Observacao: durante validacao real, endpoints interativos como botoes, lista e carrossel podem
retornar `invalid payload` dependendo do comportamento atual da API. A modelagem do SDK preserva o
contrato documentado e deixa a investigacao desses endpoints para etapa especifica.

### Lista De Opcoes

```python
from zapzapapi.models.message import ListMessage

message = ListMessage(
    number=number,
    text="Escolha uma opcao:",
    choices=["[Produtos]", "Camiseta|p1|R$ 50", "Calca|p2|R$ 120"],
    list_button="Ver opcoes",
)

response = client.messages.send_list(instance_id, message)
```

Tambem e possivel enviar `choices` como string JSON ja pronta:

```python
message = ListMessage(
    number=number,
    text="Escolha uma opcao:",
    choices='["[Produtos]","Camiseta|p1|R$ 50","Calca|p2|R$ 120"]',
    list_button="Ver opcoes",
)
```

### Enquete

```python
from zapzapapi.models.message import PollMessage

message = PollMessage(
    number=number,
    text="Qual o melhor dia?",
    choices=["Segunda", "Terca", "Quarta"],
    selectable_count=1,
)

response = client.messages.send_poll(instance_id, message)
```

`selectable_count` gera `selectableCount` no payload.

### Carrossel

```python
from zapzapapi.models.message import Button, CarouselCard, CarouselMessage

message = CarouselMessage(
    number=number,
    text="Confira nossas opcoes:",
    carousel=[
        CarouselCard(
            text="Produto 1",
            image="https://exemplo.com/img.jpg",
            buttons=[Button(type="REPLY", text="Quero!", id="quero")],
        )
    ],
)

response = client.messages.send_carousel(instance_id, message)
```

Tambem e possivel enviar `carousel` como string JSON ja pronta.

### Botao PIX

```python
from zapzapapi.models.message import PixButtonMessage, PixType

message = PixButtonMessage(
    number=number,
    pix_type=PixType.CPF,
    pix_key="12345678900",
    pix_name="Loja Exemplo",
)

response = client.messages.send_pix_button(instance_id, message)
```

Tipos de chave PIX:

- `PixType.EMAIL`
- `PixType.CPF`
- `PixType.CNPJ`
- `PixType.PHONE`
- `PixType.EVP`

### Solicitar Pagamento

```python
from zapzapapi.models.message import RequestPaymentMessage, PixType

message = RequestPaymentMessage(
    number=number,
    amount=49.90,
    pix_key="12345678900",
    pix_type=PixType.CPF,
    item_name="Assinatura Plano Ouro",
    title="Detalhes do pedido",
    text="Pagamento referente ao pedido #123",
)

response = client.messages.request_payment(instance_id, message)
```

A API exige pelo menos um metodo de pagamento: `pix_key`, `boleto_code`, `payment_link` ou
`allow_cards=True`.

### Status / Story

```python
from zapzapapi.models.message import FontType, StatusBackgroundColor, StatusMessage, StatusType

message = StatusMessage(
    type=StatusType.TEXT,
    text="Ola mundo!",
    background_color=StatusBackgroundColor.CINZA_ESCURO,
    font=FontType.SANS_SERIF,
)

response = client.messages.send_status(instance_id, message)
```

Tipos de status:

- `StatusType.TEXT`
- `StatusType.IMAGE`
- `StatusType.VIDEO`
- `StatusType.AUDIO`
- `StatusType.PTT`

Cores de fundo de status:

- `AMARELO`, `AMARELO_MEDIO`, `AMARELO_ESCURO`
- `VERDE_CLARO`, `VERDE`, `VERDE_ESCURO`
- `AZUL_CLARO`, `AZUL`, `AZUL_ESCURO`
- `LILAS_CLARO`, `LILAS`, `LILAS_ESCURO`
- `MAGENTA`
- `ROSA_CLARO`, `ROSA`
- `MARROM_CLARO`
- `CINZA_CLARO`, `CINZA`, `CINZA_ESCURO`

### Reacao Com Emoji

```python
from zapzapapi.models.message import ReactionMessage

message = ReactionMessage(
    number=number,
    message_id="5511991515364:2A6E2F02CE4125FDBA1B",
    emoji="\U0001f44d",
)

response = client.messages.send_reaction(instance_id, message)
```

Para reagir a uma mensagem enviada pela propria biblioteca:

```python
from zapzapapi.models.message import ReactionMessage, TextMessage

text_response = client.messages.send_text(
    instance_id,
    TextMessage(number=number, text="Mensagem que recebera reacao."),
)

message_id = text_response["id"]

reaction_response = client.messages.send_reaction(
    instance_id,
    ReactionMessage(
        number=number,
        message_id=message_id,
        emoji="\U0001f44d",
    ),
)
```

## Validacao Local

```powershell
python -m pytest
python -m ruff check .
python -m mypy src/zapzapapi
```

## Escopo Atual

Este README documenta apenas o que ja foi consolidado na biblioteca:

- core do client;
- conta;
- instancias basicas;
- envio de mensagens;
- reacao a mensagem.

Operacoes avancadas de conversas, contatos, grupos, webhooks, campanhas, filas e outros dominios
devem ser documentadas conforme forem implementadas e validadas.
