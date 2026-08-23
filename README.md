# Practice CTF Strategies

A classroom repository for hands-on cybersecurity practice challenges across multiple Capture the Flag domains. The goal is to help students build practical investigation habits: inspect artifacts carefully, document their reasoning, recover flags, and explain how they solved each challenge.

This repository is intended for learning, not competition pressure. Challenges may be used during class, labs, homework, workshops, or self-paced practice.

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

Operation NIGHTJAR is a self-hosted Flask challenge intended for instructors and
workshop organizers. Its public source includes the organizer solution, so hosts
should customize the answer set before assigning it to students.

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
