# Password Generator Tester

A small, self-contained Python password tester and passphrase generator.

It uses only Python's standard library, so it can be shared as a single script without installing extra packages.

## Features

- Generates readable random passphrases
- Uses cryptographically secure randomness with `secrets`
- Checks length, repetition, simple sequences, and known breach exposure
- Optionally checks passwords against the Have I Been Pwned breached-password API
- Supports offline mode when you do not want internet checks
- No required dependencies

## NIST-Inspired Design

This project follows several recommendations from NIST SP 800-63B guidance for passwords and passphrases:

- Length matters: generated passwords are long passphrases, and the tester requires at least 15 characters.
- Long passwords are allowed: the tester accepts passwords up to 64 characters by default.
- Passphrases are encouraged: generated passwords are built from multiple readable word-like chunks.
- Known-compromised passwords are rejected when online checking is enabled.
- The script avoids old-school forced composition rules for user-entered passwords.
- Unicode input is normalized before checking so visually similar text is handled more consistently.

This is not an official NIST certification. It is a small tool designed to follow the spirit of current NIST password advice: prefer longer, easier-to-use secrets, check for compromised passwords, and avoid rules that push people toward predictable passwords like `Password1!`.

Reference: [NIST SP 800-63B](https://pages.nist.gov/800-63-4/sp800-63b.html)

## How Generated Passwords Are Built

The generator creates passphrases using:

- 4 word-like chunks by default
- hyphens between chunks for readability
- a random 3-digit number
- a random symbol
- secure randomness from Python's `secrets` module

Example shape:

```text
Brisproath-Mauwaumtre-Broanpread-Flirvu291=
```

The word-like chunks are generated from random syllable parts rather than a fixed fallback list. That means the script remains portable as a single file while still producing a very large number of possible combinations.

By default, generated passwords are usually well over the 15-character minimum and stay under the 64-character maximum.

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

## Fun Fact

A typical 8-character random password using letters, numbers, and symbols has about:

```text
94^8 = 6,095,689,385,410,816 possible combinations
```

At a hypothetical 1 trillion guesses per second, that entire space could be searched in roughly 1.7 hours.

This generator's default 4-chunk passphrases have an estimated search space above `10^35` combinations. Under the same simplified 1 trillion guesses per second assumption, that is far longer than the age of the universe.

Real cracking speed depends heavily on password storage, hashing algorithm, attacker hardware, password reuse, leaks, and whether the password was randomly generated. The safest move is still to use a password manager and never reuse passwords.

## Notes

Generated passwords use made-up pronounceable words rather than a fixed fallback dictionary. This keeps the script portable while still giving a very large number of possible combinations.

This tool is meant as a learning-friendly password helper, not a replacement for a password manager. For real accounts, use a trusted password manager and enable multi-factor authentication where possible.
