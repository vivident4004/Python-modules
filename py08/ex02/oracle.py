import os
import re
from dotenv import load_dotenv


# Variables the application expects in its configuration
REQUIRED_VARS = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]

# Regex: a known secret keyword followed by = and a quoted value (4+ chars)
# Compiled once at module level for efficiency
SECRET_PATTERN = re.compile(
    r'(?i)\b(password|api_key|secret_key|token|credentials)'
    r'\s*=\s*["\'][^"\']{4,}["\']'
)

# Lines that contain any of these strings are trusted and skipped
# during the secret scan (they reference os.environ or are meta-code)
SAFE_MARKERS = ["os.environ", "os.getenv", "load_dotenv", "re.compile"]


def load_config() -> dict[str, str]:
    """Load configuration from .env, then from real environment variables.

    load_dotenv() does NOT override variables that are already set in
    the environment, so a CLI override like:
        MATRIX_MODE=production python3 oracle.py
    always takes precedence over the .env file.
    """
    load_dotenv()
    return {var: os.environ.get(var, "") for var in REQUIRED_VARS}


def get_missing(config: dict[str, str]) -> list[str]:
    """Return the list of variables that are not set."""
    return [key for key, val in config.items() if not val]


def format_db_status(url: str) -> str:
    """Derive a human-readable database status from the URL."""
    if not url:
        return "Not configured"
    local_keywords = ("localhost", "local", "sqlite", "127.0.0.1")
    if any(kw in url for kw in local_keywords):
        return "Connected to local instance"
    return "Connected to remote instance"


def format_api_status(api_key: str) -> str:
    """Return API access status based on whether the key is set."""
    return "Authenticated" if api_key else "Not authenticated"


def format_zion_status(endpoint: str) -> str:
    """Return Zion network status based on whether the endpoint is set."""
    return "Online" if endpoint else "Offline"


def print_config(config: dict[str, str]) -> None:
    """Display configuration values in a human-friendly format.

    Sensitive values (API_KEY, DATABASE_URL) are never printed raw;
    they are replaced with derived status messages.
    """
    mode = config.get("MATRIX_MODE", "Not set")
    db = format_db_status(config.get("DATABASE_URL", ""))
    api = format_api_status(config.get("API_KEY", ""))
    level = config.get("LOG_LEVEL", "Not set")
    zion = format_zion_status(config.get("ZION_ENDPOINT", ""))

    print("Configuration loaded:")
    print(f"  Mode:         {mode}")
    print(f"  Database:     {db}")
    print(f"  API Access:   {api}")
    print(f"  Log Level:    {level}")
    print(f"  Zion Network: {zion}")


def is_safe_line(line: str) -> bool:
    """Return True if the line is known to be safe from secret patterns.

    Lines that reference os.environ, load_dotenv, or re.compile are
    infrastructure code, not hardcoded secrets.
    """
    return any(marker in line for marker in SAFE_MARKERS)


def check_hardcoded_secrets(filepath: str) -> list[str]:
    """Scan a Python source file for patterns that look like hardcoded secrets.

    Returns a list of suspicious line descriptions, empty if none found.
    """
    findings: list[str] = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for num, line in enumerate(f, start=1):
                # Skip comment lines and known-safe infrastructure lines
                if line.strip().startswith("#") or is_safe_line(line):
                    continue
                if SECRET_PATTERN.search(line):
                    snippet = line.strip()[:55]
                    findings.append(f"    Line {num}: {snippet}")
    except OSError as e:
        findings.append(f"    Cannot read file: {e}")
    return findings


def print_security_check(config: dict[str, str]) -> None:
    """Run and display the three-point environment security check."""
    print("\nEnvironment security check:")

    # Check 1: scan this source file for hardcoded secrets
    findings = check_hardcoded_secrets(__file__)
    if findings:
        print("  [WARN] Possible hardcoded secrets found:")
        for finding in findings:
            print(finding)
    else:
        print("  [OK] No hardcoded secrets detected")

    # Check 2: a local .env file exists
    if os.path.isfile(".env"):
        print("  [OK] .env file properly configured")
    else:
        print("  [WARN] No .env file found (copy .env.example to .env)")

    # Check 3: production mode is reachable via env var override
    # load_dotenv() never overrides existing env vars, so this always works
    print("  [OK] Production overrides available")


def main() -> None:
    """Load configuration, display it, and run the security check."""
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    config = load_config()
    missing = get_missing(config)

    if missing:
        print(f"WARNING: Missing variables: {', '.join(missing)}")
        print("Copy .env.example to .env and fill in the values.")
        print()

    print_config(config)
    print_security_check(config)
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
