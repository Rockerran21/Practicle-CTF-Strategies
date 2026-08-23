# Operation NIGHTJAR — a self-hosted crypto CTF

A medium-difficulty, chained cryptography capture-the-flag you host on your own
laptop. Anyone on the same network opens a browser and plays. Players may use
any online tool (CyberChef, dcode.fr, openssl, Python). Answers are checked on
the server, so the solution is never sitting in the page source.

## Run it

```bash
cd cryptography/operation-nightjar
./run.sh
```

The script builds a local virtualenv, installs Flask and cryptography, runs a
self-test on the puzzle chain, then serves the game. It prints two URLs:

- `http://localhost:8000` for you, on this machine
- `http://<your-lan-ip>:8000` to share with players on the same Wi-Fi/LAN

Stop with `Ctrl-C`. To run on a different port: `PORT=9000 ./run.sh`.

### If players on the LAN cannot connect

macOS may block incoming connections. Allow Python through the firewall in
System Settings > Network > Firewall (or turn the firewall off temporarily on a
trusted network). Everyone must be on the same network, and the network must not
use client isolation (some guest Wi-Fi does).

## Deploy to the internet (Render, free)

GitHub Pages cannot host this: it only serves static files, and this game needs
the Python server to validate answers, enforce stage order, and enforce the hint
timer. Render runs the real app on its free tier.

This directory includes the organizer implementation and solution. Before using
it with students, change the answer set and flag near the top of `app.py`, run
the self-test, and deploy your customized copy from a private repository. Render
can deploy from a private repository once you connect your GitHub.

1. Go to https://render.com and sign up (you can use "Sign in with GitHub").
2. Click **New +** > **Blueprint**.
3. Connect your GitHub and pick your customized private repository. Render reads
   `render.yaml` and fills everything in (build command, start command, a
   generated `NIGHTJAR_SECRET`, and `HINT_DELAY_SECONDS=600`).
4. Click **Apply** / **Create**. First build takes a couple of minutes.
5. You get a public URL like `https://nightjar-ctf.onrender.com`. Share that.

Notes:
- Free services sleep after ~15 minutes idle and cold-start in under a minute.
  During a live event with people actively playing it stays awake.
- To change the hint delay later: Render dashboard > your service >
  Environment > edit `HINT_DELAY_SECONDS` > save (it redeploys).
- `NIGHTJAR_SECRET` is generated once and kept, so player progress cookies
  survive restarts.

## How the game is structured

Four stages, each a different technique. Solving one reveals what is needed for
the next, so nobody can skip ahead. Each stage page has tiered hints, but they
stay hidden until the player has been on that stage for 10 minutes. Each stage
runs its own countdown, started the first time that player opens it, so the
hints reward genuine effort rather than being available immediately.

To change the hint delay, set `HINT_DELAY_SECONDS` (default 600). For example,
`HINT_DELAY_SECONDS=300 ./run.sh` unlocks hints after 5 minutes, and
`HINT_DELAY_SECONDS=0 ./run.sh` makes them available immediately.

| Stage | Technique | Recovers |
|-------|-----------|----------|
| 001 | Base64 armor + ROT13 | codename |
| 002 | Vigenère cipher (key is the reward from 001) | location |
| 003 | Single-byte XOR, brute forced | countersign |
| 004 | SHA-256 of the three words -> AES-256-CBC decrypt | the plan + flag |

---

## ORGANIZER SOLUTION (spoilers)

Keep this section to yourself.

- **Stage 1.** Base64-decode the blob, then ROT13. Message reveals codename
  **RAVEN**. Solving it reveals the Vigenère key `NIGHTJAR`.
- **Stage 2.** Vigenère-decode with key `NIGHTJAR`. Location is **HARBOR**.
- **Stage 3.** Hex-decode, brute force all 256 single-byte XOR keys (the key is
  `0x5A`). Countersign is **THUNDER**.
- **Stage 4.** Join uppercase with hyphens: `RAVEN-HARBOR-THUNDER`. SHA-256 that
  string to get the 64-hex-char AES-256 key. Decrypt the Base64 ciphertext with
  AES-256-CBC, that key (as hex), and the published IV (all zeros). The plan
  contains the flag:

  ```
  NIGHTJAR{d3ad_dr0p_0300_0ld_h4rb0r}
  ```

### Quick command-line check of stage 4

```bash
KEY=$(printf '%s' 'RAVEN-HARBOR-THUNDER' | shasum -a 256 | cut -d' ' -f1)
echo "<paste the stage 4 base64>" | \
  openssl enc -d -aes-256-cbc -K "$KEY" -iv 00000000000000000000000000000000 -a -A
```

## Make your own edition

Open `app.py` and edit the block near the top: `CODENAME`, `LOCATION`,
`PASSWORD`, `VIGENERE_KEY`, `XOR_KEY`, `FLAG`, and the three plaintext messages.
All ciphertexts are regenerated from those values at startup, and
`python3 app.py --selftest` re-solves the whole chain to confirm it stays
consistent. Nothing needs to be recomputed by hand.

## Notes

- Progress is stored per browser (Flask session cookie). "RESET" in the top bar
  clears a player's progress. There is no shared scoreboard by design; it is a
  solve-it-yourself exercise.
- This is a training exercise. The story and "plan" are fictional.
