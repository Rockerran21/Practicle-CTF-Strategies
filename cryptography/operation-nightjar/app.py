#!/usr/bin/env python3
"""
Operation NIGHTJAR - a self-hosted, medium-difficulty cryptography CTF.

Players recover three pieces of evidence, each locked behind a different
technique, then combine them into a hash that decrypts the final plan.

  Stage 1  Base64 + ROT13 onion          -> codename   RAVEN
  Stage 2  Vigenere cipher (key reward)   -> location   HARBOR
  Stage 3  single-byte XOR brute force    -> passphrase THUNDER
  Stage 4  SHA-256 -> AES-256-CBC decrypt -> the plan + flag

All plaintext answers live only in this process. Only ciphertext is ever
sent to the browser, and every answer is checked server-side, so players
cannot read the solution out of the page source.

Run:  ./run.sh        (creates a venv, installs deps, serves on the LAN)
Self-test the whole chain:  python3 app.py --selftest
"""

import base64
import codecs
import hashlib
import os
import sys
import time

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# --------------------------------------------------------------------------
# The secret answer set. Change these to make your own edition of the game.
# Nothing here is ever sent to the browser except the derived ciphertext.
# --------------------------------------------------------------------------

CODENAME = "RAVEN"        # stage 1 answer
LOCATION = "HARBOR"       # stage 2 answer
PASSWORD = "THUNDER"      # stage 3 answer
VIGENERE_KEY = "NIGHTJAR"  # revealed as the stage 1 reward
XOR_KEY = 0x5A             # single byte, players brute force this
IV = b"\x00" * 16          # AES IV, published to players in stage 4

FLAG = "NIGHTJAR{d3ad_dr0p_0300_0ld_h4rb0r}"

STAGE1_PLAINTEXT = "INTERCEPT 001 // COURIER CODENAME IS RAVEN // SUBMIT THE CODENAME"
STAGE2_PLAINTEXT = (
    "INTERCEPT 002 // DROP POINT CONFIRMED THE OLD HARBOR WAREHOUSE DOCK SEVEN "
    "// SUBMIT THE ONE WORD LOCATION"
)
STAGE3_PLAINTEXT = (
    "INTERCEPT 003 // STRIKE WINDOW OPENS 0300 HOURS // COUNTERSIGN WORD THUNDER "
    "// SUBMIT THE COUNTERSIGN"
)
FINAL_PLAN = (
    "OPERATION NIGHTJAR // FINAL PLAN\n"
    "-------------------------------\n"
    "Rendezvous at 0300 hours, the old harbor warehouse, dock seven.\n"
    "Courier RAVEN carries the package. Countersign on contact: THUNDER.\n"
    "If the countersign fails, abort and scatter.\n\n"
    "FLAG: " + FLAG + "\n"
)


# --------------------------------------------------------------------------
# Cipher helpers
# --------------------------------------------------------------------------

def rot13(text: str) -> str:
    return codecs.encode(text, "rot_13")


def make_stage1_blob() -> str:
    """base64( rot13( plaintext ) ) - players peel base64 then ROT13."""
    inner = rot13(STAGE1_PLAINTEXT).encode()
    return base64.b64encode(inner).decode()


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Classic Vigenere. Only A-Z are shifted; other chars pass through."""
    out = []
    key = key.upper()
    ki = 0
    for ch in plaintext.upper():
        if "A" <= ch <= "Z":
            k = ord(key[ki % len(key)]) - ord("A")
            out.append(chr((ord(ch) - ord("A") + k) % 26 + ord("A")))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


def single_byte_xor(data: bytes, key: int) -> bytes:
    return bytes(b ^ key for b in data)


def make_stage3_blob() -> str:
    """Single-byte XOR, delivered as a hex string for brute forcing."""
    return single_byte_xor(STAGE3_PLAINTEXT.encode(), XOR_KEY).hex()


def pkcs7_pad(data: bytes, block: int = 16) -> bytes:
    pad = block - (len(data) % block)
    return data + bytes([pad]) * pad


def derive_key() -> bytes:
    """The key players must reconstruct: SHA-256 of the joined codewords."""
    joined = f"{CODENAME}-{LOCATION}-{PASSWORD}".upper()
    return hashlib.sha256(joined.encode()).digest()


def make_final_blob() -> str:
    """AES-256-CBC encrypt the plan; key = SHA-256(joined codewords)."""
    key = derive_key()
    padded = pkcs7_pad(FINAL_PLAN.encode())
    enc = Cipher(algorithms.AES(key), modes.CBC(IV)).encryptor()
    ct = enc.update(padded) + enc.finalize()
    return base64.b64encode(ct).decode()


# --------------------------------------------------------------------------
# Build all puzzle artifacts once at startup.
# --------------------------------------------------------------------------

ARTIFACTS = {
    "stage1_blob": make_stage1_blob(),
    "stage2_blob": vigenere_encrypt(STAGE2_PLAINTEXT, VIGENERE_KEY),
    "stage3_blob": make_stage3_blob(),
    "final_blob": make_final_blob(),
    "sha_key_hex": derive_key().hex(),
    "iv_hex": IV.hex(),
    "join_example": f"{CODENAME}-{LOCATION}-{PASSWORD}".upper(),
}


# --------------------------------------------------------------------------
# Flask app
# --------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = os.environ.get("NIGHTJAR_SECRET", os.urandom(24).hex())

STAGES = [1, 2, 3, 4]

# Hints for a stage stay hidden until the player has been on that stage this
# long. Each stage has its own countdown, started the first time the player
# opens it. Override with e.g. HINT_DELAY_SECONDS=300 ./run.sh
HINT_DELAY = int(os.environ.get("HINT_DELAY_SECONDS", "600"))


def solved() -> set:
    return set(session.get("solved", []))


def mark_solved(stage: int) -> None:
    s = solved()
    s.add(stage)
    session["solved"] = sorted(s)


def unlocked(stage: int) -> bool:
    """Stage 1 is always open; later stages need the previous one solved."""
    if stage == 1:
        return True
    return (stage - 1) in solved()


def norm(value: str) -> str:
    return (value or "").strip().upper()


def stage_started_at(stage: int) -> int:
    """Epoch seconds when the player first opened this stage (set on first view)."""
    started = session.get("started", {})
    key = str(stage)
    if key not in started:
        started[key] = int(time.time())
        session["started"] = started
    return started[key]


@app.route("/robots.txt")
def robots():
    body = (
        "User-agent: *\n"
        "Disallow: /brief\n"
        "# analyst note: the intercepts are chained. solve one to unlock the next.\n"
        "# start here -> /brief\n"
    )
    return app.response_class(body, mimetype="text/plain")


@app.route("/")
def index():
    return render_template(
        "index.html",
        solved=solved(),
        total=len(STAGES),
    )


@app.route("/brief")
def brief():
    return render_template("brief.html", solved=solved(), total=len(STAGES))


@app.route("/stage/<int:stage>", methods=["GET", "POST"])
def stage(stage: int):
    if stage not in STAGES:
        return redirect(url_for("index"))
    if not unlocked(stage):
        return render_template("locked.html", stage=stage)

    # Start this stage's hint countdown on first view, then compute how long is
    # left before hints unlock for this player.
    started_at = stage_started_at(stage)
    elapsed = int(time.time()) - started_at
    hints_available = elapsed >= HINT_DELAY
    hint_remaining = max(0, HINT_DELAY - elapsed)

    feedback = None
    just_solved = False

    if request.method == "POST":
        answer = norm(request.form.get("answer"))
        expected = {
            1: norm(CODENAME),
            2: norm(LOCATION),
            3: norm(PASSWORD),
            4: norm(FLAG),
        }[stage]
        if answer == expected:
            mark_solved(stage)
            just_solved = True
        else:
            feedback = "Rejected. That is not the value we intercepted. Keep digging."

    return render_template(
        f"stage{stage}.html",
        stage=stage,
        solved=solved(),
        total=len(STAGES),
        art=ARTIFACTS,
        feedback=feedback,
        just_solved=just_solved,
        already=stage in solved(),
        hints_available=hints_available,
        hint_remaining=hint_remaining,
        hint_delay_min=HINT_DELAY // 60,
    )


@app.route("/win")
def win():
    if 4 not in solved():
        return redirect(url_for("index"))
    return render_template("win.html", flag=FLAG)


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


# --------------------------------------------------------------------------
# Self-test: solve the whole chain to prove the artifacts are consistent.
# --------------------------------------------------------------------------

def selftest() -> int:
    ok = True

    # Stage 1: base64 decode then rot13.
    s1 = rot13(base64.b64decode(ARTIFACTS["stage1_blob"]).decode())
    ok &= CODENAME in s1
    print(f"[stage1] {'PASS' if CODENAME in s1 else 'FAIL'}: {s1}")

    # Stage 2: Vigenere decrypt with the key.
    def vig_dec(ct, key):
        out, ki, key = [], 0, key.upper()
        for ch in ct.upper():
            if "A" <= ch <= "Z":
                k = ord(key[ki % len(key)]) - ord("A")
                out.append(chr((ord(ch) - ord("A") - k) % 26 + ord("A")))
                ki += 1
            else:
                out.append(ch)
        return "".join(out)

    s2 = vig_dec(ARTIFACTS["stage2_blob"], VIGENERE_KEY)
    ok &= LOCATION in s2
    print(f"[stage2] {'PASS' if LOCATION in s2 else 'FAIL'}: {s2}")

    # Stage 3: brute force all 256 single-byte XOR keys.
    raw = bytes.fromhex(ARTIFACTS["stage3_blob"])
    found = None
    for k in range(256):
        cand = single_byte_xor(raw, k)
        try:
            text = cand.decode("ascii")
        except UnicodeDecodeError:
            continue
        if PASSWORD in text and "INTERCEPT" in text:
            found = (k, text)
            break
    ok &= found is not None
    if found:
        print(f"[stage3] PASS (key=0x{found[0]:02X}): {found[1]}")
    else:
        print("[stage3] FAIL: no key recovered")

    # Stage 4: SHA-256 the joined codewords, AES-256-CBC decrypt.
    joined = f"{CODENAME}-{LOCATION}-{PASSWORD}".upper()
    key = hashlib.sha256(joined.encode()).digest()
    dec = Cipher(algorithms.AES(key), modes.CBC(IV)).decryptor()
    padded = dec.update(base64.b64decode(ARTIFACTS["final_blob"])) + dec.finalize()
    plan = padded[: -padded[-1]].decode()
    ok &= FLAG in plan
    print(f"[stage4] {'PASS' if FLAG in plan else 'FAIL'}:\n{plan}")

    print("\nALL PASS" if ok else "\nSOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=False)
