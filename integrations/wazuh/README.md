# Integração NexVigil × Wazuh SIEM

Esta pasta contém os arquivos de integração entre o NexVigil e o Wazuh SIEM.

## Objetivo

O NexVigil gera telemetria estruturada a partir do laboratório local em FastAPI.

A integração com o Wazuh demonstra como esses eventos podem ser encaminhados para uma plataforma SIEM e utilizados em um fluxo de monitoramento e análise de segurança.

## Arquitetura

```text
NexVigil FastAPI
       |
       | Telemetria JSON
       v
security_events.jsonl
       |
       v
Wazuh Agent / Log Collector
       |
       v
Wazuh Manager
       |
       v
Wazuh Indexer
       |
       v
Wazuh Dashboard
       |
       v
SOC Analyst
```

## Infraestrutura validada

Foi realizado localmente o deployment single-node do Wazuh 4.14.7 utilizando Docker.

Componentes validados:

- Wazuh Manager
- Wazuh Indexer
- Wazuh Dashboard
- acesso ao Dashboard via HTTPS

## Integração fornecida

O diretório inclui:

- exemplo de configuração do Wazuh Agent;
- coleta do arquivo `security_events.jsonl`;
- regras customizadas para eventos de autenticação;
- correlação de múltiplas falhas;
- mapeamento para MITRE ATT&CK T1110 - Brute Force.

## Telemetria NexVigil

Os eventos são registrados em `logs/security_events.jsonl`.

Os principais campos são:

- `event_id`;
- `timestamp`;
- `event_type`;
- `action`;
- `result`;
- `username`;
- `source_ip`;
- `service`.

Nenhuma senha é registrada na telemetria.

## Regras customizadas

| Regra | Detecção |
|---|---|
| `100100` | Evento de autenticação do NexVigil |
| `100101` | Falha de autenticação |
| `100102` | Múltiplas falhas da mesma origem |
| MITRE ATT&CK | `T1110 - Brute Force` |

As regras estão em `rules/nexvigil_rules.xml`.

## Configuração do Agent

O exemplo de configuração para coleta dos logs está disponível em `agent-config-example.xml`.

## Limite da validação

A infraestrutura principal do Wazuh foi implantada e validada localmente.

A ingestão contínua através do Wazuh Agent e as regras customizadas não foram submetidas a execução prolongada devido ao consumo de recursos do stack no hardware utilizado pelo laboratório.

A configuração necessária para reprodução foi mantida no projeto sem apresentar funcionalidades não testadas integralmente como validadas.

## Escopo de segurança

As simulações ofensivas do NexVigil são destinadas exclusivamente a localhost, interfaces de loopback ou ambientes explicitamente autorizados.
