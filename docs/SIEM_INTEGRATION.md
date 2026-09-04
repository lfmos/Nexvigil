# Integração com Wazuh SIEM

## Visão geral

O NexVigil combina um Detection Engine desenvolvido em Python com uma integração documentada para o Wazuh SIEM.

A proposta é demonstrar tanto os fundamentos internos de detecção quanto a utilização de uma plataforma próxima de ambientes reais de SOC.

## Arquitetura

```text
Simulação Purple Team
        |
        v
    FastAPI Lab
        |
        v
security_events.jsonl
     |          |
     |          |
     v          v
NexVigil      Wazuh
Detection     SIEM
Engine          |
     |          |
     +----+-----+
          |
          v
       Analista
```

## Detection Engine próprio

Antes da integração com o Wazuh, o NexVigil implementou em Python:

- leitura e parsing de eventos;
- detecção de brute force;
- correlação temporal;
- correlação entre falhas e autenticação bem-sucedida;
- classificação de severidade;
- MITRE ATT&CK T1110;
- estado persistente;
- leitura incremental;
- deduplicação de alertas;
- identificadores de alerta;
- restart safety.

## Wazuh

Foi implantado localmente um ambiente Wazuh 4.14.7 single-node com:

- Wazuh Manager;
- Wazuh Indexer;
- Wazuh Dashboard.

Os três componentes foram executados com sucesso e o Dashboard foi acessado localmente via HTTPS.

## Telemetria NexVigil

A aplicação produz eventos JSON Lines em:

`logs/security_events.jsonl`

Campos utilizados:

- `event_id`;
- `timestamp`;
- `event_type`;
- `action`;
- `result`;
- `username`;
- `source_ip`;
- `service`.

Credenciais não são armazenadas nos eventos.

## Regras Wazuh incluídas

| Regra | Finalidade |
|---|---|
| `100100` | Evento de autenticação NexVigil |
| `100101` | Falha de autenticação |
| `100102` | Múltiplas falhas da mesma origem |
| MITRE ATT&CK | `T1110 - Brute Force` |

As regras estão disponíveis em:

`integrations/wazuh/rules/nexvigil_rules.xml`

## Configuração do Agent

Um exemplo para coleta da telemetria está disponível em:

`integrations/wazuh/agent-config-example.xml`

## Status de validação

Validado:

- deployment Wazuh single-node;
- Wazuh Manager;
- Wazuh Indexer;
- Wazuh Dashboard;
- acesso ao Dashboard.

Preparado para reprodução, mas não submetido a execução prolongada:

- ingestão contínua pelo Wazuh Agent;
- execução contínua das regras customizadas no SIEM.

Essa limitação é documentada explicitamente devido aos recursos disponíveis no laboratório local.

## Escopo de segurança

O NexVigil utiliza dados sintéticos e segue uma abordagem local-first.

Todas as simulações ofensivas são restritas a localhost, loopback ou ambientes explicitamente autorizados.