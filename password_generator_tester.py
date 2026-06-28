import argparse
import hashlib
import secrets
import string
import unicodedata
import getpass
import urllib.request
import urllib.error


MIN_LENGTH = 15
MAX_LENGTH = 64
DEFAULT_WORD_COUNT = 4

SYLLABLE_STARTS = [
    "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "r",
    "s", "t", "v", "w", "z", "br", "cr", "dr", "fl", "fr", "gl",
    "gr", "pl", "pr", "sl", "st", "tr"
]

SYLLABLE_VOWELS = [
    "a", "e", "i", "o", "u", "ai", "au", "ea", "ee", "ia", "oa", "oo"
]

SYLLABLE_ENDS = [
    "", "", "", "b", "ck", "d", "f", "k", "l", "m", "n", "p", "r",
    "s", "t", "th"
]


def normalize_password(password: str) -> str:
    return unicodedata.normalize("NFKC", password)


def generate_pseudo_word(min_syllables: int = 2, max_syllables: int = 4) -> str:
    syllable_count = secrets.randbelow(max_syllables - min_syllables + 1) + min_syllables
    parts = []

    for _ in range(syllable_count):
        parts.append(
            secrets.choice(SYLLABLE_STARTS)
            + secrets.choice(SYLLABLE_VOWELS)
            + secrets.choice(SYLLABLE_ENDS)
        )

    word = "".join(parts)
    return word[:10]


def random_word() -> str:
    return generate_pseudo_word()


def is_sequential(password: str) -> bool:
    lowered = password.lower()

    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm",
    ]

    for sequence in sequences:
        for i in range(len(sequence) - 3):
            chunk = sequence[i:i + 4]

            if chunk in lowered or chunk[::-1] in lowered:
                return True

    return False


def is_repetitive(password: str) -> bool:
    return len(set(password)) <= 3


def character_mix_score(password: str) -> int:
    groups = [
        any(char.islower() for char in password),
        any(char.isupper() for char in password),
        any(char.isdigit() for char in password),
        any(char in string.punctuation for char in password),
    ]

    return sum(groups)


def check_pwned_password(password: str) -> int | None:
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    request = urllib.request.Request(
        f"https://api.pwnedpasswords.com/range/{prefix}",
        headers={"User-Agent": "password-generator-tester"},
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            results = response.read().decode("utf-8")
    except urllib.error.URLError:
        return None

    for line in results.splitlines():
        leaked_suffix, count = line.split(":")

        if leaked_suffix == suffix:
            return int(count)

    return 0


def check_password(password: str, check_breaches: bool = True) -> tuple[bool, list[str]]:
    password = normalize_password(password)
    reasons = []

    if len(password) < MIN_LENGTH:
        reasons.append(f"Password must be at least {MIN_LENGTH} characters.")

    if len(password) > MAX_LENGTH:
        reasons.append(f"Password should not exceed {MAX_LENGTH} characters.")

    if is_sequential(password):
        reasons.append("Password contains sequential characters.")

    if is_repetitive(password):
        reasons.append("Password is too repetitive.")

    if check_breaches:
        pwned_count = check_pwned_password(password)

        if pwned_count is None:
            reasons.append("Could not check breached-password database.")
        elif pwned_count > 0:
            reasons.append(f"Password has appeared in breaches {pwned_count:,} times.")

    return len(reasons) == 0, reasons


def generate_password(word_count: int = DEFAULT_WORD_COUNT) -> str:
    selected_words = [
        random_word().capitalize()
        for _ in range(word_count)
    ]

    number = str(secrets.randbelow(900) + 100)
    symbol = secrets.choice("!@#$%^&*?+=")

    return "-".join(selected_words) + number + symbol


def generate_valid_password(word_count: int = DEFAULT_WORD_COUNT, check_breaches: bool = True) -> str:
    for _ in range(1_000):
        password = generate_password(word_count)
        passed, _ = check_password(password, check_breaches=check_breaches)

        if passed:
            return password

    if check_breaches:
        return generate_valid_password(word_count, check_breaches=False)

    raise RuntimeError("Could not generate a valid password after 1,000 attempts.")


def show_generated_passwords(count: int, word_count: int, check_breaches: bool) -> None:
    for _ in range(count):
        print(generate_valid_password(word_count, check_breaches=check_breaches))


def main():
    parser = argparse.ArgumentParser(description="Password tester and generator.")
    parser.add_argument("--generate", "-g", type=int, help="Generate this many passwords and exit.")
    parser.add_argument("--words", "-w", type=int, default=DEFAULT_WORD_COUNT, help="Words per generated password.")
    parser.add_argument("--offline", action="store_true", help="Skip Have I Been Pwned checks.")
    args = parser.parse_args()

    if args.words < 3:
        raise SystemExit("Use at least 3 words.")

    if args.generate:
        show_generated_passwords(args.generate, args.words, check_breaches=not args.offline)
        return

    while True:
        password = getpass.getpass("Enter password to check, or type 'exit': ")

        if password.lower() == "exit":
            break

        passed, reasons = check_password(password, check_breaches=not args.offline)

        if passed:
            print("Password meets the requirements.")
            continue

        print("\nPassword failed:")

        for reason in reasons:
            print(f"- {reason}")

        while True:
            choice = input("\nGenerate a new password? y/n/exit: ").lower()

            if choice == "exit":
                return

            if choice == "n":
                break

            if choice == "y":
                while True:
                    new_password = generate_valid_password(args.words, check_breaches=not args.offline)

                    print(f"\nGenerated password: {new_password}")

                    again = input("Generate another? y/n/exit: ").lower()

                    if again == "exit":
                        return

                    if again == "n":
                        break

                break

            print("Invalid choice. Enter y, n, or exit.")


if __name__ == "__main__":
    main()
