# Arquitetura — NexVigil v1.0.0

```text
Purple Team Simulation
        |
        v
FastAPI Security Lab
        |
        | JSON telemetry
        v
logs/security_events.jsonl
       / \
      /   \
     v     v
Detection  Wazuh SIEM
 Engine       |
     |        |
     v        v
Local       Dashboard
Alerts        |
     \        /
      \      /
       v    v
      SOC Analyst
```

## Application

A aplicação FastAPI é executada localmente e gera eventos sintéticos de autenticação.

## Telemetria

Os eventos são armazenados em JSON Lines.

Senhas e tokens não são registrados.

## Detection Engine

Responsável por:

- parsing;
- correlação;
- classificação de severidade;
- persistent state;
- deduplicação;
- alert IDs.

## Wazuh

A infraestrutura single-node foi validada com:

- Manager;
- Indexer;
- Dashboard.

A integração contínua do Agent é disponibilizada como configuração reproduzível, mas não foi submetida a execução prolongada.

## Attack Simulation

Os simuladores possuem restrição explícita para impedir alvos remotos arbitrários.

## Trust Boundaries

O laboratório utiliza:

- localhost;
- dados sintéticos;
- credenciais locais via `.env`;
- serviços restritos ao ambiente autorizado.