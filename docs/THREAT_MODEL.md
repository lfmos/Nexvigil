# Threat Model — v0.1

## Ativos

- código-fonte;
- telemetria;
- regras de detecção;
- alertas;
- ambiente local do desenvolvedor.

## Principais ameaças

| Ameaça | Controle inicial |
|---|---|
| segredo commitado | `.gitignore`, `.env.example`, CI |
| simulador apontado para terceiro | bloqueio de host não-loopback |
| dados sensíveis em log | esquema sem senha/token |
| DoS acidental | volume pequeno na simulação |
| path traversal | caminhos internos fixos |
| dependência vulnerável | pip-audit / CI |
| código inseguro | Bandit / testes |
| regra com falso positivo | threshold + janela temporal |

## Risco residual

A v0.1 é laboratório local e não deve ser tratada como aplicação de produção.
