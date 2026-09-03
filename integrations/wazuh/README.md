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