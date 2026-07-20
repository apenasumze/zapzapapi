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
from zapzapapi.models.messages import TextMessage

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
from zapzapapi.models.messages import QuotedMessage, TextMessage

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
from zapzapapi.models.messages import MediaMessage, MediaType

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
from zapzapapi.models.messages import ContactMessage

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
from zapzapapi.models.messages import LocationMessage

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
from zapzapapi.models.messages import LocationButtonMessage

message = LocationButtonMessage(
    number=number,
    text="Compartilhe sua localizacao, por favor.",
)

response = client.messages.request_location(instance_id, message)
```

### Botoes

```python
from zapzapapi.models.messages import Button, ButtonsMessage

message = ButtonsMessage(
    number=number,
    text="Como podemos ajudar?",
    buttons=[
        Button.reply(text="Sim", id="yes"),
        Button.link(text="Site", url="https://exemplo.com"),
        Button.copy_text(text="Copiar cupom", copy_code="ABC123"),
    ],
    footer="Escolha uma opcao",
)

response = client.messages.send_buttons(instance_id, message)
```

O SDK aceita ate 3 botoes e envia `buttons` como array JSON real, igual ao payload validado na
aplicacao web.
Use `Button.reply()` para `text + id`, `Button.link()` para `text + url`,
`Button.call()` para `text + phone` e `Button.copy_text()` para `text + copy`.
O construtor direto tambem e aceito, desde que exatamente uma acao seja informada:
`id`, `url`, `phone` ou `copy_code`.
O SDK ainda aceita string JSON por compatibilidade e normaliza para lista antes do envio.

Observacao: durante validacao real, endpoints interativos como botoes, lista e carrossel podem
retornar `invalid payload` dependendo do comportamento atual da API. A modelagem do SDK preserva o
contrato documentado e deixa a investigacao desses endpoints para etapa especifica.

### Lista De Opcoes

```python
from zapzapapi.models.messages import ListChoice, ListMessage

message = ListMessage(
    number=number,
    text="Escolha uma opcao:",
    category="Produtos",
    choices=[
        ListChoice(item="Camiseta", id="p1", description="R$ 50"),
        ListChoice(item="Calca", id="p2", description="R$ 120"),
    ],
    list_button="Opcoes",
    footer_text="Gostou?",
)

response = client.messages.send_list(instance_id, message)
```

`category` e inserido como primeiro elemento da lista final, no formato `[Produtos]`.
Cada `ListChoice` gera uma string no formato `item|id|description`. Apenas `item` e obrigatorio;
`id` e `description` podem ser omitidos quando a API permitir. O payload final envia `choices`
como array JSON real. String JSON pronta ainda e aceita apenas como compatibilidade de entrada.

### Enquete

```python
from zapzapapi.models.messages import PollMessage

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
from zapzapapi.models.messages import CarouselButton, CarouselCard, CarouselMessage

message = CarouselMessage(
    number=number,
    text="Confira nossas opcoes:",
    carousel=[
        CarouselCard(
            text="Produto 1",
            image="https://exemplo.com/img.jpg",
            buttons=[CarouselButton(text="Quero!", id="quero")],
        )
    ],
)

response = client.messages.send_carousel(instance_id, message)
```

`carousel` deve ser informado como lista de `CarouselCard` e sai no payload como array JSON real.
O SDK ainda aceita string JSON por compatibilidade e normaliza para lista antes do envio.
O botao de carrossel usa `CarouselButton`; o tipo confirmado e `REPLY` e e aplicado por padrao.

### Botao PIX

```python
from zapzapapi.models.messages import PixButtonMessage, PixType

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
from zapzapapi.models.messages import RequestPaymentMessage, PixType

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
from zapzapapi.models.messages import FontType, StatusBackgroundColor, StatusMessage, StatusType

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
from zapzapapi.models.messages import ReactionMessage

message = ReactionMessage(
    number=number,
    message_id="5511991515364:2A6E2F02CE4125FDBA1B",
    emoji="\U0001f44d",
)

response = client.messages.send_reaction(instance_id, message)
```

Para reagir a uma mensagem enviada pela propria biblioteca:

```python
from zapzapapi.models.messages import ReactionMessage, TextMessage

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

## Conversas

Operacoes sobre conversas e mensagens ja existentes ficam em `client.chats`. O envio de novas
mensagens permanece em `client.messages`.

### Buscar Conversas

```python
from zapzapapi.models.chat import FindChatsRequest

chats = client.chats.find(
    instance_id,
    FindChatsRequest(
        sort="-wa_lastMsgTimestamp",
        limit=50,
        wa_is_group=False,
        lead_is_ticket_open=True,
    ),
)
```

Filtros booleanos aceitam `bool` no SDK e sao enviados como as strings `"true"` ou `"false"`
esperadas pela API. Campos com nomes mistos preservam aliases do payload externo, por exemplo:

- `wa_is_group` gera `wa_isGroup`.
- `wa_contact_name` gera `wa_contactName`.
- `lead_is_ticket_open` gera `lead_isTicketOpen`.

### Marcar Conversa Como Lida

```python
from zapzapapi.models.chat import ReadChatRequest

response = client.chats.read(
    instance_id,
    ReadChatRequest(number="5511999999999@s.whatsapp.net"),
)
```

### Arquivar, Fixar, Silenciar E Bloquear

```python
from zapzapapi.models.chat import (
    ArchiveChatRequest,
    BlockChatRequest,
    MuteChatRequest,
    PinChatRequest,
)

client.chats.archive(
    instance_id,
    ArchiveChatRequest(number="5511999999999@s.whatsapp.net", archive=True),
)
client.chats.pin(
    instance_id,
    PinChatRequest(number="5511999999999@s.whatsapp.net", pin=False),
)
client.chats.mute(
    instance_id,
    MuteChatRequest(number="5511999999999@s.whatsapp.net", duration=86400000),
)
client.chats.block(
    instance_id,
    BlockChatRequest(number=number, block=True),
)

blocked = client.chats.blocklist(instance_id)
```

### Deletar Ou Limpar Conversa

```python
from zapzapapi.models.chat import DeleteChatRequest

response = client.chats.delete(
    instance_id,
    DeleteChatRequest(
        number=number,
        delete_chat_db=True,
        delete_messages_db=True,
        clear_chat_whatsapp=True,
    ),
)
```

Aliases relevantes:

- `delete_chat_db` gera `deleteChatDB`.
- `delete_messages_db` gera `deleteMessagesDB`.
- `delete_chat_whatsapp` gera `deleteChatWhatsApp`.
- `clear_chat_whatsapp` gera `clearChatWhatsApp`.

### Notas Do Chat

```python
from zapzapapi.models.chat import ChatNotesRequest, EditChatNotesRequest, RefreshChatNotesRequest

notes = client.chats.notes(
    instance_id,
    ChatNotesRequest(number="5511999999999@s.whatsapp.net"),
)

updated = client.chats.edit_notes(
    instance_id,
    EditChatNotesRequest(
        number="5511999999999@s.whatsapp.net",
        notes="Cliente prefere contato no periodo da tarde",
    ),
)

refreshed = client.chats.refresh_notes(
    instance_id,
    RefreshChatNotesRequest(number="5511999999999@s.whatsapp.net", force=False),
)
```

### Historico E Operacoes De Mensagem

```python
from zapzapapi.models.chat import (
    DeleteMessageRequest,
    DownloadMessageRequest,
    EditMessageRequest,
    FindMessagesRequest,
    HistorySyncRequest,
    MarkMessagesReadRequest,
)

messages = client.chats.find_messages(
    instance_id,
    FindMessagesRequest(chat_id="5511999999999@s.whatsapp.net", limit=100),
)

edited = client.chats.edit_message(
    instance_id,
    EditMessageRequest(
        message_id="ABCDEF123456",
        number=number,
        text="Texto corrigido.",
    ),
)

deleted = client.chats.delete_message(
    instance_id,
    DeleteMessageRequest(message_id="ABCDEF123456", number=number),
)

media = client.chats.download_message(
    instance_id,
    DownloadMessageRequest(
        message_id="7EB0F01D7244B421048F0706368376E0",
        return_link=True,
    ),
)

read = client.chats.mark_messages_read(
    instance_id,
    MarkMessagesReadRequest(message_ids=["3EB0538DA65A59F6D8A251"]),
)

sync = client.chats.history_sync(
    instance_id,
    HistorySyncRequest(
        message_id="3EB01234567890ABCDEF",
        number="5511999999999@s.whatsapp.net",
        count=20,
    ),
)
```

`message_id` gera `id` nos endpoints de mensagem, exceto em `HistorySyncRequest`, onde gera
`messageid`. `chat_id` gera `chatid`. `MarkMessagesReadRequest.message_ids` deve ser informado
como lista Python e sai no payload como array JSON real.

### Indicador De Digitacao

```python
from zapzapapi.models.chat import PresenceRequest, PresenceType

response = client.chats.presence(
    instance_id,
    PresenceRequest(
        number=number,
        presence=PresenceType.COMPOSING,
        delay=3000,
    ),
)
```

Tipos de presenca:

- `PresenceType.COMPOSING`
- `PresenceType.RECORDING`
- `PresenceType.PAUSED`

### Reacao Pelo Dominio De Conversas

```python
from zapzapapi.models.chat import ReactionMessage

response = client.chats.react_message(
    instance_id,
    ReactionMessage(
        number=number,
        message_id="5511991515364:2A6E2F02CE4125FDBA1B",
        emoji="\U0001f44d",
    ),
)
```

O endpoint documentado pela API para reacao e `/api/v1/{instanceId}/message/react`. Por
compatibilidade, `client.messages.send_reaction(...)` continua disponivel e usa o mesmo endpoint em
uma unica chamada.

## Contatos

Operacoes de agenda, verificacao de numero e detalhes publicos ficam em `client.contacts`.
Os endpoints reais de verificacao e detalhes usam o prefixo HTTP `/chat/*`, mas permanecem neste
dominio por tratarem de identidade de contato/chat, nao de manipulacao de conversa.

### Verificar Numeros

```python
from zapzapapi.models.contacts import CheckNumbersRequest

response = client.contacts.check_numbers(
    instance_id,
    CheckNumbersRequest(numbers=["5511999999999", "5521888888888"]),
)
```

`numbers` deve ser enviado como lista de strings. O SDK ainda aceita string JSON ou CSV por
compatibilidade e normaliza para array JSON, que e o formato aceito pela API real.

### Detalhes Do Contato Ou Grupo

```python
from zapzapapi.models.contacts import ContactDetailsRequest

details = client.contacts.details(
    instance_id,
    ContactDetailsRequest(number="5511999999999", preview=True),
)
```

`preview` aceita `bool` no SDK e e enviado como `"true"` ou `"false"`.

### Agenda De Contatos

```python
from zapzapapi.models.contacts import AddContactRequest, ListContactsRequest, RemoveContactRequest

created = client.contacts.add(
    instance_id,
    AddContactRequest(phone="5511999999999", name="Joao Silva"),
)

removed = client.contacts.remove(
    instance_id,
    RemoveContactRequest(number="5511999999999"),
)

fast_contacts = client.contacts.list_fast(instance_id)

contacts = client.contacts.list(
    instance_id,
    ListContactsRequest(limit=50, offset=0),
)
```

## Perfil Da Instancia

Operacoes sobre nome e foto do perfil publico da instancia conectada ficam em `client.profile`.
Este dominio nao representa o perfil de um contato.

```python
from zapzapapi.models.profile import UpdateProfileImageRequest, UpdateProfileNameRequest

updated_image = client.profile.update_image(
    instance_id,
    UpdateProfileImageRequest(image="https://exemplo.com/logo.jpg"),
)

updated_name = client.profile.update_name(
    instance_id,
    UpdateProfileNameRequest(name="Minha Empresa"),
)
```

Para remover a foto, envie `image="remove"`, conforme o contrato da API.

## Grupos

Operacoes de grupos e comunidades ficam em `client.groups`.

### Criar E Consultar Grupos

```python
from zapzapapi.models.groups import (
    CreateGroupRequest,
    GroupInfoRequest,
    GroupInviteInfoRequest,
    JoinGroupRequest,
    LeaveGroupRequest,
    ListGroupsRequest,
)

created = client.groups.create(
    instance_id,
    CreateGroupRequest(
        name="Meu Time",
        participants=["5511999990001", "5511999990002"],
    ),
)

info = client.groups.info(
    instance_id,
    GroupInfoRequest(group_jid="120363000000000000@g.us", get_invite_link=True),
)

invite_info = client.groups.invite_info(
    instance_id,
    GroupInviteInfoRequest(invite_code="ABC123"),
)

joined = client.groups.join(
    instance_id,
    JoinGroupRequest(invite_code="https://chat.whatsapp.com/ABC123"),
)

left = client.groups.leave(
    instance_id,
    LeaveGroupRequest(group_jid="120363000000000000@g.us"),
)

groups = client.groups.list(instance_id)

groups_with_participants = client.groups.search(
    instance_id,
    ListGroupsRequest(get_participants=True),
)
```

Aliases relevantes:

- `group_jid` gera `groupjid`.
- `invite_code` gera `invitecode`.
- `get_invite_link` gera `getInviteLink`.
- `get_participants` gera `getParticipants`.

`participants` deve ser enviado como lista de strings. O SDK ainda aceita string JSON ou CSV por
compatibilidade e normaliza para array JSON, que e o formato aceito pela API real.

### Administrar Grupos

```python
from zapzapapi.models.groups import (
    GroupParticipantAction,
    ResetGroupInviteCodeRequest,
    UpdateGroupAnnounceRequest,
    UpdateGroupDescriptionRequest,
    UpdateGroupImageRequest,
    UpdateGroupLockedRequest,
    UpdateGroupNameRequest,
    UpdateGroupParticipantsRequest,
)

group_jid = "120363000000000000@g.us"

invite = client.groups.reset_invite_code(
    instance_id,
    ResetGroupInviteCodeRequest(group_jid=group_jid),
)

client.groups.update_announce(
    instance_id,
    UpdateGroupAnnounceRequest(group_jid=group_jid, announce=True),
)

client.groups.update_description(
    instance_id,
    UpdateGroupDescriptionRequest(group_jid=group_jid, description="Descricao do grupo"),
)

client.groups.update_image(
    instance_id,
    UpdateGroupImageRequest(group_jid=group_jid, image="remove"),
)

client.groups.update_locked(
    instance_id,
    UpdateGroupLockedRequest(group_jid=group_jid, locked=False),
)

client.groups.update_name(
    instance_id,
    UpdateGroupNameRequest(group_jid=group_jid, name="Novo Nome"),
)

client.groups.update_participants(
    instance_id,
    UpdateGroupParticipantsRequest(
        group_jid=group_jid,
        action=GroupParticipantAction.ADD,
        participants=["5511999990003"],
    ),
)
```

`announce`, `locked`, `get_invite_link` e `get_participants` aceitam `bool` no SDK e sao enviados
como as strings `"true"` ou `"false"`.

Acoes confirmadas para participantes:

- `GroupParticipantAction.ADD`
- `GroupParticipantAction.REMOVE`
- `GroupParticipantAction.PROMOTE`
- `GroupParticipantAction.DEMOTE`
- `GroupParticipantAction.APPROVE`
- `GroupParticipantAction.REJECT`

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
- reacao a mensagem;
- conversas e operacoes sobre mensagens existentes.
- contatos e verificacao de numeros;
- perfil da instancia conectada;
- grupos e comunidades.

Operacoes de webhooks, campanhas, filas e outros dominios devem ser documentadas conforme forem
implementadas e validadas.
