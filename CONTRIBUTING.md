# Contributing a Challenge

Contributions from educators, students, and security practitioners are welcome.
Please propose one challenge per pull request.

## Before you begin

- Use only fictional or synthetic data.
- Do not include credentials, personal data, malware, or targets that you do not
  own or have permission to test.
- Choose a clear learning objective and an approximate difficulty level.
- Keep flags, answer keys, generators, and official solutions out of public
  student-facing folders unless the challenge is explicitly marked as retired.

## Challenge structure

Create a folder inside the closest matching domain and include a `README.md`
that identifies:

- Challenge name, category, difficulty, and author
- Learning objective
- Student scenario and provided files
- Expected flag format
- Required tools or environment
- Safety or cleanup instructions, when relevant

Use `templates/challenge-template.md` as a starting point.

## Pull request checklist

- Confirm that every included file is safe to publish.
- Test the intended solve path from a clean environment.
- Remove answer keys and accidental metadata from student-facing files.
- Explain what the challenge teaches and how you tested it.
- Confirm that your contribution may be distributed under the repository's MIT
  License.
