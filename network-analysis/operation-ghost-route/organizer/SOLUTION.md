# Organizer Solution: Operation GHOST ROUTE

Do not distribute this file during an active class.

## Expected findings

- Compromised user: `mira.shrestha`
- Workstation: `WS-FIN-07`
- Internal IP: `10.42.7.23`
- Payload URL: `https://updates-check.invalid/assets/quarterly_update.zip`
- Staging archive: `C:\ProgramData\Cache\q3-forecast.7z`
- Exfiltration domain: `telemetry-cache.invalid`
- Flag: `flag{correlation_beats_single_alerts}`

## Reasoning path

1. The authentication export establishes that `mira.shrestha` was active from
   `WS-FIN-07` at `10.42.7.23`. The denied `admin.ops` events are conspicuous but
   unrelated noise.
2. The proxy export shows that the same user and IP downloaded
   `quarterly_update.zip` at `03:35:22Z`. Preserve its SHA-256 value because it
   becomes key material later.
3. Endpoint events show PowerShell starting at `03:36:07Z`, followed by 7-Zip
   staging finance documents and a second PowerShell command describing the
   transformation pipeline.
4. DNS events from the affected IP contain numbered Base32-looking labels under
   `telemetry-cache.invalid`. The similarly named query from `VULN-SCANNER` is
   noise and must be excluded by source IP.
5. Sort the labels by their numeric prefix, concatenate the data after the
   hyphen, and restore Base32 padding.
6. Decode Base32. XOR the result with a repeating eight-byte key made from the
   first 16 hexadecimal characters of the payload SHA-256. Decompress the result
   with zlib.

## Reference decoder

```python
import base64
import zlib

encoded = "".join(chunks[index] for index in sorted(chunks))
encoded += "=" * ((8 - len(encoded) % 8) % 8)
encrypted = base64.b32decode(encoded)
key = bytes.fromhex(payload_sha256[:16])
compressed = bytes(
    value ^ key[index % len(key)]
    for index, value in enumerate(encrypted)
)
print(zlib.decompress(compressed).decode())
```

## Suggested scoring

- Identity, host, and IP: 15 points
- Payload and hash correlation: 15 points
- Archive and endpoint timeline: 20 points
- Correct DNS stream isolation and ordering: 20 points
- Correct transformation pipeline: 20 points
- Flag and evidence-backed report: 10 points

## Common mistakes

- Following the high-risk denied login instead of correlating successful events
- Sorting sequence labels as arbitrary strings instead of integers
- Including the vulnerability-scanner query
- Decoding each Base32 chunk separately
- Using the hexadecimal hash characters as an ASCII key instead of converting
  the first 16 hex characters into eight bytes
- Forgetting zlib decompression after XOR
