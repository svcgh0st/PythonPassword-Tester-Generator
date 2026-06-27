# Password Generator Tester

A small, self-contained Python password tester and passphrase generator.

It uses only Python's standard library, so it can be shared as a single script without installing extra packages.

## Features

- Generates readable random passphrases
- Uses cryptographically secure randomness with `secrets`
- Checks length, repetition, simple sequences, and character variety
- Optionally checks passwords against the Have I Been Pwned breached-password API
- Supports offline mode when you do not want internet checks
- No required dependencies

## Requirements

- Python 3.10 or newer

## Usage

Run the interactive tester:

```powershell
python password_generator_tester.py
```

Generate 10 passwords:

```powershell
python password_generator_tester.py --generate 10
```

Generate passwords without checking Have I Been Pwned:

```powershell
python password_generator_tester.py --generate 10 --offline
```

Use more words per generated password:

```powershell
python password_generator_tester.py --generate 10 --words 5 --offline
```

## Breach Checking

When online checking is enabled, the script uses the Have I Been Pwned k-anonymity API.

The full password is not sent over the internet. The script hashes the password locally, sends only the first 5 characters of the SHA-1 hash, then checks the returned hash suffixes locally.

Use `--offline` to skip this check entirely.

## Notes

Generated passwords use made-up pronounceable words rather than a fixed fallback dictionary. This keeps the script portable while still giving a very large number of possible combinations.

This tool is meant as a learning-friendly password helper, not a replacement for a password manager. For real accounts, use a trusted password manager and enable multi-factor authentication where possible.
