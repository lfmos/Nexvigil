# NexVigil SIEM Integration

## Overview

NexVigil integrates its local security telemetry with Wazuh to demonstrate how application events can enter a Security Information and Event Management workflow.

The project intentionally keeps the custom NexVigil Detection Engine and the external SIEM as separate components.

## Architecture

```text
Controlled Attack Simulation
          |
          v
      FastAPI Lab
          |
          v
security_events.jsonl
      |          |
      |          +------------------+
      v                             v
NexVigil Detection Engine      Wazuh Collector
      |                             |
      v                             v
Local Alerts                  Wazuh Manager
                                    |
                                    v
                              Wazuh Indexer
                                    |
                                    v
                              Wazuh Dashboard
                                    |
                                    v
                                SOC Analyst