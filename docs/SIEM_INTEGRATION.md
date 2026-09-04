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