# Threat Model — NexVigil v1.0.0

## Ativos

- código-fonte;
- telemetria;
- regras de detecção;
- alertas;
- estado do Detection Engine;
- credenciais sintéticas locais;
- ambiente local do laboratório.

## Principais ameaças

| Ameaça | Controle |
|---|---|
| segredo commitado | `.gitignore`, `.env.example` e revisão |
| simulador apontado para terceiro | bloqueio de host não-loopback |
| dados sensíveis em log | esquema sem senha/token |
| DoS acidental | volume controlado nas simulações |
| path traversal | caminhos internos definidos pela aplicação |
| dependência vulnerável | pip-audit e CI |
| código inseguro | Bandit e testes |
| alerta duplicado após restart | persistent state e deduplicação |
| reprocessamento de histórico | leitura incremental por offset |
| falso positivo | threshold, janela temporal e correlação |

## Risco residual

O NexVigil v1.0.0 é um laboratório local de segurança e não deve ser tratado como plataforma de produção.

A integração contínua com o Wazuh Agent não foi submetida a validação prolongada.

Novas técnicas de detecção, cloud, SOAR e AI Security permanecem fora do escopo implementado da v1.0.0.