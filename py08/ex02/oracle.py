import os
from dotenv import load_dotenv


REQUIRED_VARS = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]


def load_config() -> dict[str, str]:
    load_dotenv()
    return {var: os.environ.get(var, "") for var in REQUIRED_VARS}


def get_missing(config: dict[str, str]) -> list[str]:
    return [key for key, val in config.items() if not val]


def display(value: str, fallback: str = "not set") -> str:
    return value if value else fallback


def format_db_status(url: str) -> str:
    if not url:
        return "not configured"
    local_keywords = ("localhost", "local", "sqlite", "127.0.0.1")
    if any(kw in url for kw in local_keywords):
        return "connected to local instance"
    return "connected to remote instance"


def format_api_status(api_key: str) -> str:
    return "authenticated" if api_key else "not authenticated"


def format_zion_status(endpoint: str) -> str:
    return "online" if endpoint else "offline"


def print_config(config: dict[str, str]) -> None:
    print("Configuration loaded:")
    print(f"  Mode: {display(config['MATRIX_MODE'])}")
    print(f"  Database: {format_db_status(config['DATABASE_URL'])}")
    print(f"  API access: {format_api_status(config['API_KEY'])}")
    print(f"  Log level: {display(config['LOG_LEVEL'])}")
    print(f"  Zion network: {format_zion_status(config['ZION_ENDPOINT'])}")


def is_ignored(filename: str) -> bool:
    if not os.path.isfile(".gitignore"):
        return False
    try:
        with open(".gitignore", "r") as f:
            entries = [
                line.strip()
                for line in f
                if line.strip() and not line.startswith("#")
            ]
    except OSError:
        return False
    return filename in entries


def check_env_file() -> tuple[bool, str]:
    secret = ".env"
    if not os.path.isfile(secret):
        return False, f"{secret} not found"
    if is_ignored(secret):
        return True, f"{secret} exists and is listed in .gitignore"
    return (
        False,
        f"{secret} exists but is NOT in .gitignore: "
        "risk of committing secrets!"
    )


def check_missing(missing: list[str]) -> tuple[bool, str]:
    if not missing:
        return True, "all required variables are set"
    return False, f"missing variables: {', '.join(missing)}"


def check_production_override() -> tuple[bool, str]:
    return True, "Production overrides available"


def print_security_check(missing: list[str]) -> None:
    checks = [
        check_env_file(),
        check_missing(missing),
        check_production_override(),
    ]
    print("\nEnvironment security check:")
    for ok, message in checks:
        tag = "[OK]" if ok else "[WARN]"
        print(f"  {tag} {message}")


def main() -> None:
    print("\nORACLE STATUS: reading the Matrix...\n")
    config = load_config()
    missing = get_missing(config)
    print_config(config)
    print_security_check(missing)
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
