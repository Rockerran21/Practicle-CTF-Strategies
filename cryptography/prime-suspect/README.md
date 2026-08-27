# Prime Suspect

Category: Cryptography

Difficulty: Beginner / Intermediate

Estimated time: 30 to 60 minutes

Author: Ranjan Marasini

## Hosted challenge

[Open Prime Suspect on Render](https://prime-suspect-crypto-ctf.onrender.com/)

## Description

Two RSA gateways generated fresh keys during the same virtual machine boot
sequence. A monitoring sensor captured both public keys and one encrypted
diagnostic message.

Analyze the relationship between the captured RSA values, recover the plaintext
sent to Gateway Alpha, and submit the flag.

The challenge uses deliberately small training keys and raw RSA. These choices
are unsafe in real systems and exist only to make the cryptographic failure
clear enough to study.

## Learning objectives

Students should be able to:

1. Recognize an RSA modulus, public exponent, and ciphertext.
2. Compare multiple RSA public keys for unsafe mathematical relationships.
3. Reconstruct a private key after identifying a key-generation failure.
4. Convert between large integers and byte strings.
5. Explain why secure randomness and reviewed cryptographic libraries matter.

## Provided files

- `capture.txt`: the forensic evidence containing two public keys and one
  ciphertext
- `index.html`, `styles.css`, and `app.js`: the static browser challenge

## Objective

Recover the plaintext encrypted for Gateway Alpha and submit the flag it
contains.

## Flag format

```text
forbes{...}
```

## Run locally

```bash
cd cryptography/prime-suspect
python3 -m http.server 8000
```

Open `http://localhost:8000` in a browser.

Python 3 or any language with arbitrary-precision integers is sufficient to
solve the challenge. External packages and brute force are not required.

## Instructor note

This public folder contains only the student-facing challenge and a client-side
validator based on a SHA-256 digest. Keep the intended solve script, raw flag,
generator, and official write-up in private instructor materials during an
active class.
