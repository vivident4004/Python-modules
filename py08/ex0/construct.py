import sys
import os
import site


def check_virtual_environment() -> dict:
    """
    Raccoglie informazioni complete sull'ambiente Python corrente.

    Returns:
        dict: dizionario con le informazioni sull'ambiente.
    """
    in_venv = sys.prefix != sys.base_prefix
    virtual_env = os.environ.get("VIRTUAL_ENV")

    info = {
        "in_venv": in_venv,
        "python_executable": sys.executable,
        "python_version": sys.version,
        "sys_prefix": sys.prefix,
        "sys_base_prefix": sys.base_prefix,
        "virtual_env_var": virtual_env,
    }

    if in_venv:
        env_name = os.path.basename(sys.prefix)
        try:
            packages_path = site.getsitepackages()[0]
        except AttributeError:
            packages_path = "non disponibile"

        info["env_name"] = env_name
        info["env_path"] = sys.prefix
        info["packages_path"] = packages_path

    return info


def print_environment_report() -> None:
    """Stampa un report leggibile dell'ambiente corrente."""
    info = check_virtual_environment()

    if info["in_venv"]:
        print("\nMATRIX STATUS: welcome to the construct\n")
        print(f"Current python: {info['python_executable']}")
        print(f"Virtual environment: {info.get('env_name')}")
        print(f"Environment path: {info.get('env_path')}")
        print("\nSUCCESS: you're in an isolated environment!"
              "\nSafe to install packages without affecting the global system.")
        print(f"Package installation path: {info.get('packages_path')}")
    else:
        print("\nMATRIX STATUS: you're still plugged in\n")
        print(f"Current python: {info['python_executable']}")
        print("Virtual environment: None detected")
        print("\nWARNING: you're in the global environment!"
              "\nThe machines can see everything you install.")
        print("\nTo enter the construct, run:")
        print("$> python -m venv matrix_env")
        print("$> source matrix_env/bin/activate  # on UNIX")
        print("$> matrix_env\\Scripts\\activate     # on Windows")
        print("\nThen run this program again.")


if __name__ == "__main__":
    print_environment_report()
