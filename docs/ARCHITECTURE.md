# Architecture — v0.1

```text
Synthetic Client
      |
      v
FastAPI Application
      |
      | JSON telemetry
      v
logs/security_events.jsonl
      |
      v
Detection Engine
      |
      | threshold/rule
      v
alerts/security_alerts.jsonl
```

## Trust boundaries

### Application
Aceita tráfego somente local na v0.1.

### Telemetry
Eventos são sintéticos e não devem conter senha ou token.

### Detection Engine
Lê somente o arquivo de eventos e escreve alertas.

### Attack Simulation
O simulador possui bloqueio explícito para impedir alvo remoto.
