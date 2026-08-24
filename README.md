# NexVigil v0.1 Starter

**Continuous Security Validation & AI-Assisted Defense Platform**

NexVigil é um laboratório de Security Engineering criado para integrar Blue Team, Red Team controlado, Purple Team, DevSecOps, Cloud Security e automação com Python.

## Objetivo da v0.1

A primeira versão implementa um ciclo mínimo:

1. aplicação local gera eventos de autenticação;
2. eventos são gravados em JSON Lines;
3. um detector Python analisa falhas repetidas;
4. um cenário de brute force **estritamente local** produz telemetria;
5. o detector gera um alerta;
6. testes e CI validam o código.

## Segurança por padrão

- o simulador ofensivo aceita apenas `127.0.0.1` e `localhost`;
- somente dados sintéticos;
- nenhum segredo real;
- nenhuma ação automática destrutiva;
- ambiente ofensivo deve permanecer isolado;
- IA futura será apenas copiloto, sem shell arbitrário.

## Requisitos

- Windows 11, Linux ou macOS
- Python 3.11+
- Git

Docker/Podman é opcional nesta fase.

## Início rápido — Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Terminal 1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2
python detection_engine/main.py

# Terminal 3
python scripts/simulate_bruteforce.py
```

Abra:

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

## Estrutura

```text
nexvigil/
├── app/
│   └── main.py
├── detection_engine/
│   ├── detector.py
│   └── main.py
├── scripts/
│   └── simulate_bruteforce.py
├── tests/
│   └── test_detector.py
├── logs/
├── alerts/
├── docs/
├── .github/workflows/
├── requirements.txt
└── README.md
```

## Próximos marcos

- v0.2: Wazuh / SIEM
- v0.3: MITRE ATT&CK mapping
- v0.4: pipeline DevSecOps ampliado
- v0.5: Terraform + cloud deployment temporário
- v0.6: AI SOC Copilot local
