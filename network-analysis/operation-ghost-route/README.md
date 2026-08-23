# Operation GHOST ROUTE

Category: Network Analysis / Incident Response

Difficulty: Advanced

Estimated time: 90 to 150 minutes

Author: Ranjan Marasini

Operation GHOST ROUTE is a synthetic incident investigation. Students receive
authentication, web proxy, endpoint, and DNS telemetry from a fictional finance
network. They must distinguish useful evidence from deliberate noise, identify
the compromised identity and workstation, reconstruct the attack timeline, and
recover data carried through DNS queries.

This challenge is defensive and self-contained. It does not require attacking a
live service or contacting any domain found in the evidence.

## Hosted portal

The Flask application in this directory provides a browser-based case portal,
downloadable evidence locker, field guide, progressive answer validation, and
session-based progress. Run it locally with:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The root `render.yaml` deploys this portal as a Render web service.

## Student package

Give students only these items:

- `brief.md`
- `learning-materials.md`
- `evidence/auth.csv`
- `evidence/proxy.csv`
- `evidence/endpoint.jsonl`
- `evidence/dns.csv`

Keep `organizer/` private during an active class because it contains the
generator, validation logic, and complete solution.

## Investigation goals

Students should determine:

1. The compromised username
2. The affected workstation and internal IP address
3. The initial payload URL
4. The staging archive path
5. The start and end of the suspicious activity
6. The decoding pipeline used for DNS exfiltration
7. The final flag

A complete submission should include a short timeline and evidence references,
not only the flag.

## Generate a fresh edition

The committed evidence is a ready-to-use edition. Instructors can create a
different deterministic edition with Python 3 and no third-party packages:

```bash
cd network-analysis/operation-ghost-route
python3 organizer/generate.py --output evidence --seed 20260817
python3 organizer/generate.py --selftest --output evidence
```

Change the scenario constants near the top of `organizer/generate.py` to create
a new identity, host, payload, or flag. Run the self-test after every change.

## Suggested delivery

- Release the evidence as a ZIP or private classroom repository.
- Allow command-line tools, spreadsheets, CyberChef, and short scripts.
- Require an evidence-backed incident timeline.
- Award partial credit for correct scoping even if the final payload is not
  decoded.

## Safety

All domains use the reserved `.invalid` top-level domain, all people are
fictional, and all telemetry is generated locally. Do not replace these with
real third-party systems unless you have explicit permission.
