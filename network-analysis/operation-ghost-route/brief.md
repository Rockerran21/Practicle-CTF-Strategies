# Incident Brief: GHOST ROUTE

At 09:42 NPT on 17 August 2026, the network monitoring team noticed a burst of
unusual DNS queries from the finance VLAN. The resolver retained the queries,
but the alert did not identify whether the activity was malicious.

You have four exports from the same morning:

- Identity-provider authentication events
- Secure web proxy requests
- Endpoint process and file events
- Internal DNS resolver queries

The exports contain ordinary activity, scanner traffic, and at least one
high-confidence but unrelated alert. Timestamps use UTC and may not appear in
chronological order.

## Your task

Determine what happened and recover the exfiltrated flag. Submit:

1. Compromised account
2. Affected host and source IP
3. Initial payload URL
4. Staging archive path
5. Incident timeline in UTC
6. Decoding steps
7. Final flag

## Rules

- Work only with the supplied files.
- Do not browse to any domain appearing in the evidence.
- Scripts are allowed and expected.
- Every conclusion must cite at least one evidence record.

Flag format: `flag{...}`
