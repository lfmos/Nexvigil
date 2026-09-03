# NexVigil

**Continuous Security Validation & Detection Lab**

> Attack. Detect. Investigate. Improve. Validate.

NexVigil é um laboratório de cibersegurança desenvolvido para demonstrar, de forma prática, conceitos de **Detection Engineering, Blue Team, Purple Team, SIEM e DevSecOps**.

O projeto utiliza uma aplicação local em FastAPI para gerar telemetria sintética, simulações ofensivas controladas para produzir comportamento malicioso e um Detection Engine desenvolvido em Python para identificar e correlacionar eventos de segurança.

A arquitetura também possui integração documentada com o **Wazuh SIEM**, permitindo aproximar o laboratório de um fluxo real de SOC.

---

## Objetivos

O NexVigil foi criado para praticar e demonstrar:

- Detection Engineering;
- Blue Team;
- Purple Team;
- análise e correlação de eventos;
- resposta a incidentes;
- MITRE ATT&CK;
- SIEM;
- Secure Coding;
- DevSecOps;
- testes automatizados;
- SAST;
- auditoria de dependências;
- persistência de estado;
- deduplicação de alertas.

---

## Arquitetura

```text
                 Purple Team Simulation
                         |
                         v
                    FastAPI Lab
                         |
                  JSON Telemetry
                         |
                         v
              security_events.jsonl
                    /         \
                   /           \
                  v             v
        NexVigil Detection     Wazuh SIEM
              Engine               |
                  |                 |
                  +--------+--------+
                           |
                           v
                      SOC Analyst
                           |
                           v
                     Investigation
                           |
                           v
                       Response
                           |
                           v
                       Improvement
```

---

## Principais funcionalidades

### Security Lab

Aplicação FastAPI local responsável por gerar eventos estruturados de autenticação.

Cada evento possui campos como:

```json
{
  "event_id": "NV-EVT-example",
  "timestamp": "2026-09-03T16:00:00+00:00",
  "event_type": "authentication",
  "action": "login",
  "result": "failed",
  "username": "analyst@nexvigil.local",
  "source_ip": "127.0.0.1",
  "service": "nexvigil-lab-api"
}
```

Senhas não são registradas na telemetria.

### Detection Engine

Engine desenvolvido em Python com:

- parsing de eventos;
- processamento incremental;
- correlação temporal;
- classificação de severidade;
- estado persistente;
- deduplicação de alertas;
- IDs determinísticos de alerta;
- restart safety.

### Brute Force Detection

Detecta múltiplas falhas de autenticação da mesma origem dentro de uma janela temporal.

```text
5+ failed logins
same source
within 60 seconds
        |
        v
HIGH - Brute Force
MITRE ATT&CK T1110
```

### Possible Account Compromise

Correlaciona múltiplas falhas seguidas de autenticação bem-sucedida para o mesmo usuário e origem.

```text
Failed
Failed
Failed
Failed
Failed
   |
Success
   |
   v
CRITICAL
Possible Account Compromise
```

### Persistent Detection State

O Detection Engine mantém estado entre reinicializações.

Isso permite:

- processar somente eventos novos;
- evitar reprocessamento do histórico;
- impedir alertas duplicados;
- preservar contexto de correlação;
- continuar detectando novas atividades após restart.

---

## Purple Team

Os scripts de simulação reproduzem comportamentos controlados contra exclusivamente o laboratório local.

Cenários implementados:

### NV-PT-001 — Brute Force

Resultado:

`HIGH - Brute Force`

MITRE ATT&CK:

`T1110 - Brute Force`

### NV-PT-002 — Failed Logins → Successful Login

Resultado:

```text
HIGH     - Brute Force
CRITICAL - Possible Account Compromise
```

### NV-PT-003 — Restart Safety

Validado:

- alertas históricos não são emitidos novamente após restart;
- novos eventos continuam sendo detectados;
- novos alert IDs são gerados.

---

## Wazuh SIEM

Foi implantado localmente um ambiente **Wazuh 4.14.7 single-node** utilizando Docker.

Componentes validados:

- Wazuh Manager;
- Wazuh Indexer;
- Wazuh Dashboard;
- acesso ao Dashboard via HTTPS.

O projeto fornece ainda:

```text
integrations/wazuh/
├── README.md
├── agent-config-example.xml
└── rules/
    └── nexvigil_rules.xml
```

As regras demonstram:

- identificação de eventos NexVigil;
- falhas de autenticação;
- correlação de múltiplas falhas;
- MITRE ATT&CK T1110.

A ingestão contínua através do Wazuh Agent não foi submetida a execução prolongada devido às limitações de recursos do laboratório local. A configuração necessária para reprodução permanece documentada.

Veja:

`docs/SIEM_INTEGRATION.md`

---

## DevSecOps

O NexVigil possui pipeline de segurança no GitHub Actions.

Quality gates utilizados:

```text
Pytest
   |
Bandit SAST
   |
pip-audit
```

Validação atual:

- testes automatizados: PASS;
- Bandit: 0 issues;
- pip-audit: nenhuma vulnerabilidade conhecida nas dependências auditadas.

---

## Executando localmente

### 1. Ambiente virtual

Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure as credenciais locais

Copie:

```text
.env.example
```

para:

```text
.env
```

e configure as credenciais sintéticas do laboratório.

O `.env` não deve ser versionado.

### 3. Inicie a API

Terminal 1:

```cmd
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### 4. Inicie o Detection Engine

Terminal 2:

```cmd
python -m detection_engine.main
```

### 5. Execute uma simulação

Terminal 3:

```cmd
python scripts\simulate_compromise.py
```

ou:

```cmd
python scripts\simulate_bruteforce.py
```

---

## Testes e segurança

Testes:

```cmd
python -m pytest -q
```

SAST:

```cmd
bandit -r app detection_engine scripts
```

Auditoria de dependências:

```cmd
python -m pip_audit -r requirements.txt
```

---

## Estrutura

```text
Nexvigil/
├── app/
├── detection_engine/
├── scripts/
├── tests/
├── integrations/
│   └── wazuh/
├── docs/
│   ├── incidents/
│   └── SIEM_INTEGRATION.md
├── infrastructure/
├── alerts/
├── logs/
├── state/
├── .github/
│   └── workflows/
├── README.md
├── SECURITY.md
├── ROADMAP.md
├── requirements.txt
└── pyproject.toml
```

---

## Segurança e escopo

O NexVigil é um laboratório educacional e defensivo.

As simulações ofensivas são restritas a:

- localhost;
- loopback;
- ambientes explicitamente autorizados.

Os scripts não foram projetados para execução arbitrária contra sistemas externos.

Veja também:

`SECURITY.md`

---

## Status

**NexVigil v1.0**

Validado:

- FastAPI Security Lab;
- telemetria JSON;
- brute-force simulation;
- compromise simulation;
- Detection Engine;
- correlação de eventos;
- MITRE ATT&CK T1110;
- severidades HIGH e CRITICAL;
- estado persistente;
- alert deduplication;
- restart safety;
- Pytest;
- Bandit;
- pip-audit;
- GitHub Actions;
- deployment Wazuh single-node;
- acesso ao Wazuh Dashboard.

---

## Próximas evoluções

Funcionalidades futuras estão documentadas em:

`ROADMAP.md`

Entre elas:

- novas técnicas MITRE ATT&CK;
- Cloud Security;
- SOAR;
- resposta automatizada com aprovação humana;
- AI-assisted investigation;
- RAG aplicado à segurança.

---

## Autor

Projeto desenvolvido como laboratório prático e portfólio de Cibersegurança.

**NexVigil — Attack. Detect. Investigate. Improve. Validate.**