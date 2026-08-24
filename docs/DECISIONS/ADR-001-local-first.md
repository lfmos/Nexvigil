# ADR-001 — Local-first Architecture

**Status:** Accepted

## Context

A primeira fase precisa ter custo operacional zero e baixo risco de exposição.

## Decision

Aplicação, detecção, telemetria e cenários ofensivos iniciais serão executados localmente.

## Consequences

### Positive
- custo recorrente zero;
- ambiente reproduzível;
- menor superfície pública;
- rápido desenvolvimento.

### Negative
- comportamento de cloud não é reproduzido integralmente.

## Mitigation

Cloud será adicionada posteriormente por Terraform e utilizada sob demanda.
