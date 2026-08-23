# Cybersecurity CTF Labs

Open-source, classroom-tested cybersecurity challenges for students, instructors,
and independent learners. Each lab emphasizes investigation, evidence-based
reasoning, and explaining the complete solution path rather than submitting a
flag without understanding it.

## Play online

No installation is required for the hosted editions.

| Challenge | Difficulty | Live challenge | What you will practice |
| --- | --- | --- | --- |
| Operation GHOST ROUTE | Advanced | [Start the investigation](https://operation-ghost-route.onrender.com) | Cross-log correlation, incident scoping, DNS exfiltration, Base32, XOR, zlib |
| Operation NIGHTJAR | Intermediate | [Start the cryptography mission](https://nightjar-ctf.onrender.com) | Base64, ROT13, Vigenère, single-byte XOR, SHA-256, AES-256-CBC |

Render's free services sleep when inactive, so the first visit may take up to
about 50 seconds to start.

## Clone and run locally

```bash
git clone https://github.com/Rockerran21/cybersecurity-ctf-labs.git
cd cybersecurity-ctf-labs
```

Run GHOST ROUTE:

```bash
cd network-analysis/operation-ghost-route
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Run NIGHTJAR:

```bash
cd cryptography/operation-nightjar
./run.sh
```

Both applications open on `http://localhost:8000` by default.

## Use these labs in a class

- GHOST ROUTE: give students `brief.md`, `learning-materials.md`, and the
  `evidence/` directory. Keep `organizer/` private during an active class.
- NIGHTJAR: the public source contains the organizer answer set. Change the
  constants in `app.py`, run the self-test, and deploy the customized edition
  from a private repository before assigning it.
- Require a short evidence-backed write-up alongside every recovered flag.

These challenges may be used in classes, labs, homework, workshops, or
self-paced study. All scenarios are synthetic and intended only for authorized
education.

## Domains

Challenges will be organized by topic. The current plan includes:

- Forensics
- Web Exploitation
- Network Analysis
- Reverse Engineering
- Cryptography
- OSINT
- Miscellaneous

Additional domains may be added as the course grows.

## Repository Structure

```text
Practice-CTF-Strategies/
├── README.md
├── forensics/
│   └── silent-gallery/
│       ├── README.md
│       ├── gallery.png
│       ├── incident_report.txt
│       └── unlock.js
├── web/
├── network-analysis/
├── reverse-engineering/
├── cryptography/
├── osint/
├── misc/
└── templates/
    └── challenge-template.md
```

Each challenge should live in its own folder with a distinctive name. Student-facing challenge files should be included in that folder. Official solutions should not be placed in public challenge folders.

## Flag Format

Unless a challenge says otherwise, flags use this format:

```text
flag{example_flag_here}
```

Submit the full flag, including `flag{}`.

## How to Work on a Challenge

1. Open the challenge folder.
2. Read the challenge `README.md`.
3. Download or inspect the provided files.
4. Keep notes on commands, observations, and failed attempts.
5. Recover the flag.
6. Be prepared to explain your solution path.

The final answer is important, but the reasoning matters just as much. A correct flag without an explanation may not receive full credit.

## Student Rules

- Do not modify or delete challenge files in the shared repository.
- Do not publish flags or full solutions publicly.
- Do not share direct answers with classmates.
- You may discuss general approaches, tools, and concepts.
- You may use documentation, manuals, and legitimate security tools.
- When in doubt, ask for clarification before using automated exploit tools.

## Suggested Tools

Different challenges require different tools. Useful starting points include:

- `file` for identifying file types
- `strings` for printable text extraction
- `exiftool` for metadata inspection
- `binwalk` for embedded file discovery
- `xxd` or `hexdump` for byte-level inspection
- `CyberChef` for encoding and decoding experiments
- `Wireshark` for packet analysis
- `Audacity` or `Sonic Visualiser` for audio and spectrogram analysis
- `Ghidra` for reverse engineering
- Browser developer tools for web challenges
- Python for scripting small decoders or parsers

Tool choice is part of the learning process. Do not assume one tool will solve every challenge.

## Challenge Difficulty

Challenge difficulty is approximate:

- Beginner: introduces one main idea or tool
- Intermediate: combines multiple steps or requires deeper analysis
- Advanced: requires chaining techniques, writing scripts, or handling misleading artifacts

A challenge may feel easier or harder depending on your experience with the domain.

## Challenge Folder Template

Each challenge should include a short `README.md` using this structure:

```markdown
# Challenge Name

Category: Forensics
Difficulty: Intermediate
Author: Instructor

## Description

Brief story or scenario for the challenge.

## Provided Files

- file1.ext
- file2.ext

## Objective

Recover the flag.

## Flag Format

flag{...}

## Notes

Any rules, warnings, or special instructions.
```

## Current Challenges

| Domain | Challenge | Difficulty | Main Skills |
| --- | --- | --- | --- |
| Forensics | Silent Gallery | Intermediate | File carving, spectrogram analysis, whitespace steganography, basic reverse engineering |
| Cryptography | [Operation NIGHTJAR](cryptography/operation-nightjar/) | Intermediate | Base64, ROT13, Vigenere cipher, single-byte XOR, SHA-256, AES-256-CBC |
| Network Analysis | [Operation GHOST ROUTE](network-analysis/operation-ghost-route/) | Advanced | Multi-log correlation, intrusion scoping, DNS exfiltration, Base32, XOR, zlib |

Operation NIGHTJAR is a self-hosted Flask challenge intended for instructors and
workshop organizers. Its public source includes the organizer solution, so hosts
should customize the answer set before assigning it to students.

Operation GHOST ROUTE is an advanced blue-team investigation built from four
synthetic evidence sources. A student release can be prepared by distributing
only its `brief.md`, `learning-materials.md`, and `evidence/` directory.

## Flag Validation

For classroom use, there are three practical ways to validate flags:

1. Manual validation by the instructor.
2. A GitHub Pages validator that checks submitted flags against hashed values.
3. A dedicated CTF platform such as CTFd.

For casual practice, a GitHub Pages validator is simple and free, but students can inspect client-side code. For serious scoring, hidden flags, accounts, hints, and leaderboards, CTFd is the better option.

Recommended setup:

- Keep this repository public with only student-facing files.
- Keep official solutions in a separate private repository.
- Use CTFd if automated grading and score tracking are required.

## Instructor Notes

Do not place official writeups, source generators, answer keys, or raw flags in public folders unless the challenge is retired.

A good private solution record should include:

- Flag
- Intended solve path
- Required tools
- Hint ladder
- Grading rubric
- Common mistakes
- Cleanup or reset instructions, if needed

## Disclaimer

These challenges are for educational use in a controlled classroom environment. Students should only test systems, files, and services that are explicitly provided for the course or that they have permission to analyze.

## License

This repository is available under the [MIT License](LICENSE).

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
challenge format and safety requirements.
