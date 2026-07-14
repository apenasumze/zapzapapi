# Arquitetura da ZapZapApi Python Client

Este documento é a fonte de verdade técnica da biblioteca. Ele deve orientar qualquer alteração
estrutural, inclusão de endpoint, modelagem de contrato, comportamento HTTP e documentação pública.
O `README.md` não substitui este arquivo; ele apenas expõe o uso da lib para consumidores.

## Objetivo

Criar uma biblioteca Python class-based, tipada e modular para integração com a ZapZapApi, mantendo
um padrão semelhante ao da `evolutionapi`: um client central, serviços por domínio funcional e
contracts/models separados.

## Decisões fechadas

- O pacote Python público chama-se `zapzapapi`.
- A versão mínima de Python é `3.10`.
- O primeiro client é síncrono.
- O client não faz retry automático.
- O transporte HTTP executa uma única requisição por chamada de método.
- A aplicação consumidora decide se deve tentar novamente uma operação.
- Contratos de entrada e saída usam `pydantic v2`.
- O transporte usa `httpx`.
- A URL base padrão é `https://app.zapzapapi.com`.
- Os caminhos HTTP seguem o prefixo `/api/v1`.
- A autenticação usa headers `x-api-key` e `x-api-secret`.
- Docstrings públicas devem seguir o padrão Google e estar em português.
- Campos externos da API devem ser preservados por alias, sem forçar nomes Python no payload.
- A conversão de model para payload deve ser determinística, sem lógica de negócio escondida.

## Não objetivos

- Não implementar retry implícito em envio de mensagens, campanhas, fluxos ou chamadas.
- Não esconder falhas da API com fallback automático.
- Não acoplar a biblioteca a Flask, FastAPI, Django ou outro framework.
- Não misturar parsing de webhooks recebidos com serviços HTTP outbound.
- Não gerar código automaticamente sem revisão dos contratos.

## Estrutura alvo

```text
zapzapapi/
  client.py
  config.py
  transport.py
  exceptions.py
  services/
    account.py
    instances.py
    messages.py
    chats.py
    contacts.py
    groups.py
    newsletters.py
    campaigns.py
    calls.py
    business.py
    settings.py
    webhooks.py
    async_queue.py
    chatbot.py
    crm.py
    chatwoot.py
    flows.py
  models/
    base.py
    common.py
    account.py
    instance.py
    message.py
    chat.py
    contact.py
    group.py
    newsletter.py
    campaign.py
    business.py
    webhook.py
    chatbot.py
    crm.py
    responses.py
  webhooks/
    events.py
    parser.py
```

## Responsabilidades

### `ZapZapClient`

Fachada principal da biblioteca. Recebe credenciais e expõe serviços por domínio:

```python
client.account.get()
client.instances.list()
client.messages.send_text(...)
```

O client não deve conter regra específica de endpoint. Ele apenas instancia os serviços e delega
requisições ao transporte.

### Serviços

Cada serviço representa um domínio funcional da documentação:

- `account`: dados da conta.
- `instances`: criação, listagem, detalhes, QR Code e webhook administrativo.
- `messages`: envio de texto, mídia, botões, lista, enquete, localização, PIX e pagamento.
- `chats`: busca, leitura, notas, bloqueio, arquivamento e operações de mensagem existente.
- `contacts`: contatos, perfil e verificação de número.
- `groups`: grupos e comunidades.
- `newsletters`: newsletters e canais.
- `campaigns`: disparos e fila de campanhas.
- `webhooks`: configuração, erros e SSE.
- `chatbot`: agentes, funções, conhecimento e triggers.
- `business`: perfil comercial e catálogo.
- `crm`: leads e campos personalizados.
- `chatwoot`: integração Chatwoot.
- `flows`: listagem e disparo de fluxos.
- `calls`: chamadas.
- `settings`: configurações operacionais da instância.

Um serviço deve:

- expor métodos públicos com nomes Python claros;
- receber models tipados nos endpoints com body;
- retornar models de resposta quando o contrato for conhecido;
- retornar `dict[str, Any]` apenas enquanto o contrato de resposta ainda não foi consolidado;
- não montar headers diretamente;
- não tratar retry;
- não duplicar lógica de transporte.

### Models

Models representam contratos da API, não entidades de domínio internas. O contrato deve preservar
nomes externos por alias quando a API usa nomes como `replyid`, `pixType`, `readchat` ou `async`.

Contratos compartilhados devem ser extraídos antes de duplicar campos. Exemplo:

```text
BaseMessage
  TextMessage
  MediaMessage
  PollMessage
  LocationMessage
```

### Transporte HTTP

O transporte deve:

- normalizar `base_url`;
- montar headers de autenticação;
- aceitar payload já validado;
- executar exatamente uma requisição;
- converter a resposta JSON quando possível;
- lançar exceções tipadas para erros conhecidos.

O transporte não deve:

- fazer retry automático;
- corrigir payload;
- decidir idempotência;
- registrar credenciais em logs;
- acoplar-se a um serviço específico.

## Tratamento de erro

Erros HTTP devem virar exceções próprias:

- `ZapZapAuthenticationError`: 401 ou 403.
- `ZapZapNotFoundError`: 404.
- `ZapZapValidationError`: 400 ou 422.
- `ZapZapRateLimitError`: 429.
- `ZapZapAPIError`: demais erros HTTP.

O erro deve carregar, sempre que possível:

- status code;
- método;
- URL;
- corpo da resposta;
- mensagem resumida.

## Ordem de implementação

1. Base do projeto e este documento.
2. Core: client, config, transport, exceptions.
3. Models compartilhados.
4. Serviços `account`, `instances` e `messages`.
5. Testes do core e dos primeiros serviços.
6. Matriz de cobertura dos 148 endpoints.
7. Expansão por domínio.
8. Parser dos 10 webhooks recebidos.
9. Documentação de uso no README.

## Validação mínima

Antes de considerar uma entrega pronta:

```powershell
python -m pytest
python -m ruff check .
python -m mypy src/zapzapapi
```

Se alguma ferramenta não estiver instalada no ambiente atual, a limitação deve ser registrada no
fechamento da tarefa.
