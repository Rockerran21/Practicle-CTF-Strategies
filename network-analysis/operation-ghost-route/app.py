#!/usr/bin/env python3
"""Browser-based delivery portal for Operation GHOST ROUTE."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, send_from_directory, session, url_for


BASE_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = BASE_DIR / "evidence"
EVIDENCE_FILES = {
    "auth.csv": "Identity-provider authentication events",
    "proxy.csv": "Secure web proxy requests",
    "endpoint.jsonl": "Endpoint process and file events",
    "dns.csv": "Internal DNS resolver queries",
}

STAGES = [
    {
        "title": "Scope the identity",
        "prompt": "Which user account was involved?",
        "placeholder": "firstname.lastname",
        "answers": {"mira.shrestha"},
        "hint": "Correlate successful authentication with the host that later produces unusual network traffic. The high-risk denied login is not necessarily the incident.",
    },
    {
        "title": "Scope the endpoint",
        "prompt": "Submit the affected hostname and internal IP, separated by a comma.",
        "placeholder": "HOSTNAME, 10.0.0.10",
        "answers": {"ws-fin-07,10.42.7.23", "10.42.7.23,ws-fin-07"},
        "hint": "Use the username as your pivot across authentication, proxy, endpoint, and DNS records.",
    },
    {
        "title": "Find initial access",
        "prompt": "What complete URL delivered the suspicious payload?",
        "placeholder": "https://…",
        "answers": {"https://updates-check.invalid/assets/quarterly_update.zip"},
        "hint": "Look for a successful download immediately before the first suspicious process starts. Preserve its SHA-256 value.",
    },
    {
        "title": "Identify staging",
        "prompt": "What full path contains the staged archive?",
        "placeholder": r"C:\path\archive.ext",
        "answers": {r"c:\programdata\cache\q3-forecast.7z"},
        "hint": "A process event creates an archive, followed by a file-create event for the same path.",
    },
    {
        "title": "Recover the exfiltrated data",
        "prompt": "Reconstruct and decode the DNS payload, then submit the flag.",
        "placeholder": "flag{…}",
        "answers": {"flag{correlation_beats_single_alerts}"},
        "hint": "Filter by source IP, sort numbered labels, join their data, restore Base32 padding, decode, XOR with the first eight bytes of the payload SHA-256, then decompress with zlib.",
    },
]


app = Flask(__name__)
app.secret_key = os.environ.get("GHOST_ROUTE_SECRET", os.urandom(32).hex())
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")


def progress() -> int:
    return min(int(session.get("progress", 0)), len(STAGES))


def normalize(value: str) -> str:
    return "".join((value or "").strip().lower().split())


@app.get("/")
def home():
    return render_template("index.html", progress=progress(), total=len(STAGES))


@app.route("/investigate", methods=["GET", "POST"])
def investigate():
    current = progress()
    if current >= len(STAGES):
        return redirect(url_for("complete"))

    stage = STAGES[current]
    feedback = None
    if request.method == "POST":
        submitted = normalize(request.form.get("answer", ""))
        accepted = {normalize(answer) for answer in stage["answers"]}
        if submitted in accepted:
            session["progress"] = current + 1
            session.modified = True
            if current + 1 >= len(STAGES):
                return redirect(url_for("complete"))
            return redirect(url_for("investigate"))
        feedback = "That conclusion does not match the evidence. Recheck your pivots and preserve exact values."

    return render_template(
        "investigate.html",
        stage=stage,
        stage_number=current + 1,
        total=len(STAGES),
        feedback=feedback,
    )


@app.get("/evidence")
def evidence():
    return render_template("evidence.html", files=EVIDENCE_FILES)


@app.get("/evidence/<path:filename>")
def download_evidence(filename: str):
    if filename not in EVIDENCE_FILES:
        abort(404)
    return send_from_directory(EVIDENCE_DIR, filename, as_attachment=True)


@app.get("/learning")
def learning():
    return render_template("learning.html")


@app.get("/complete")
def complete():
    if progress() < len(STAGES):
        return redirect(url_for("investigate"))
    return render_template("complete.html")


@app.post("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), debug=False)
