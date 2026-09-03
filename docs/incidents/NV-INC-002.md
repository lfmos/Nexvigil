# NV-INC-002 — Possible Account Compromise

## Status

Confirmed — True Positive

## Severity

Critical

## MITRE ATT&CK

T1110 — Brute Force

## Summary

NexVigil detected five consecutive failed authentication attempts
against the synthetic account `analyst@nexvigil.local`.

Immediately after the failed attempts, a successful authentication
was observed from the same source IP and against the same account.

The correlation triggered a Critical alert for possible account
compromise.

## Evidence

- Source IP: 127.0.0.1
- Target account: analyst@nexvigil.local
- Failed attempts: 5
- Failed authentication response: HTTP 401
- Final successful authentication: HTTP 200
- Environment: NexVigil authorized local laboratory

## Detection

### Detection 1

Credential Brute Force

Severity: High

Condition:

5 or more failed authentication attempts from the same source
within 60 seconds.

### Detection 2

Possible Account Compromise

Severity: Critical

Condition:

5 or more failed authentication attempts followed by a successful
authentication from the same source IP against the same account.

## Analysis

The activity represents a simulated credential attack followed by
successful authentication.

Unlike NV-INC-001, where all authentication attempts failed,
this scenario contains evidence that valid credentials were
eventually used.

In a production environment, this behavior would require immediate
investigation of the affected account.

## Impact

No real account was compromised.

The account, credentials, traffic and environment were synthetic
and restricted to the NexVigil local laboratory.

## Classification

True Positive.

## Recommended Response

In a real environment:

1. Review the successful authentication.
2. Validate the user's activity.
3. Review subsequent actions performed by the account.
4. Revoke active sessions if compromise is suspected.
5. Reset credentials.
6. Review MFA events.
7. Search for additional authentication attempts.
8. Consider temporary source blocking.

## Purple Team Validation

Red Team behavior generated the expected telemetry.

Blue Team detection identified:

- brute force activity;
- successful authentication following the attack;
- possible account compromise.

Result: PASS.