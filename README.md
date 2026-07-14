# ZapZapApi Python Client

Cliente Python para integração com a API WhatsApp não oficial ZapZapApi.

Este README é a documentação pública da biblioteca. As decisões formais de arquitetura ficam em
[`docs/ARQUITETURA.md`](docs/ARQUITETURA.md), que deve ser consultado antes de expandir módulos,
contratos ou comportamento de transporte HTTP.

## Exemplo inicial

```python
from zapzapapi import ZapZapClient
from zapzapapi.models.message import TextMessage

client = ZapZapClient(
    api_key="SUA_API_KEY",
    api_secret="SEU_API_SECRET",
    base_url="https://app.zapzapapi.com",
)

response = client.messages.send_text(
    instance_id="ID_DA_INSTANCIA",
    message=TextMessage(
        number="5511999999999",
        text="Olá!",
    ),
)
```
