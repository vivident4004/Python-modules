import sys
import importlib.util
from typing import Any


# The three packages this program depends on
REQUIRED_PACKAGES = ["pandas", "numpy", "matplotlib"]


def check_dependency(package_name: str) -> tuple[bool, str]:
    """Check if a package is importable. Return (ok, version_or_error).

    Uses find_spec first (no side effects) and only imports to read
    the version if the package is actually present.
    """
    if importlib.util.find_spec(package_name) is None:
        return False, "not installed"
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, "__version__", "version unknown")
        return True, version
    except ImportError as e:
        return False, str(e)


def check_all_dependencies() -> dict[str, tuple[bool, str]]:
    """Return check results for every required package."""
    return {pkg: check_dependency(pkg) for pkg in REQUIRED_PACKAGES}


def all_dependencies_ok(results: dict[str, tuple[bool, str]]) -> bool:
    """Return True only if every dependency is available."""
    return all(ok for ok, _ in results.values())


def print_dependency_status(
    results: dict[str, tuple[bool, str]]
) -> None:
    """Print a line per package showing its status and version."""
    print("Checking dependencies:")
    for pkg, (ok, info) in results.items():
        tag = "[OK]     " if ok else "[MISSING]"
        print(f"  {tag} {pkg} ({info})")


def generate_matrix_data() -> tuple[Any, Any, Any]:
    """Simulate resistance signal data using numpy arrays."""
    import numpy as np

    time = np.arange(0, 1000)
    # Zion signal: sine wave with added noise
    zion = (
        np.sin(time * 0.05) * 50 + 50
        + np.random.normal(0, 3, 1000)
    )
    # Machine signal: cosine wave with added noise
    machines = (
        np.cos(time * 0.05) * 50 + 50
        + np.random.normal(0, 3, 1000)
    )
    return time, zion, machines


def analyze_data(time: Any, zion: Any, machines: Any) -> None:
    """Load data into a DataFrame and print a short summary."""
    import pandas as pd

    df = pd.DataFrame({
        "time": time,
        "zion_signal": zion,
        "machine_signal": machines,
    })
    print(f"Processing {len(df)} data points...")
    print(f"  Zion mean:    {df['zion_signal'].mean():.2f}")
    print(f"  Machine mean: {df['machine_signal'].mean():.2f}")
    print(f"  Zion peak:    {df['zion_signal'].max():.2f}")
    print(f"  Machine peak: {df['machine_signal'].max():.2f}")


def generate_visualization(time: Any, zion: Any, machines: Any) -> None:
    """Save a matplotlib plot of the signal data to disk."""
    import matplotlib

    # Use a non-interactive backend: we want a file, not a GUI window
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    print("Generating visualization...")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(time, zion, label="Zion Signal", color="green", alpha=0.8)
    ax.plot(
        time, machines,
        label="Machine Signal", color="red", alpha=0.8
    )
    ax.set_title("Matrix Signal Analysis")
    ax.set_xlabel("Time")
    ax.set_ylabel("Signal Strength")
    ax.legend()
    fig.tight_layout()

    output_file = "matrix_analysis.png"
    fig.savefig(output_file)
    plt.close(fig)

    print("\nAnalysis complete!")
    print(f"Results saved to: {output_file}")


def show_pip_vs_poetry() -> None:
    """Print a side-by-side comparison of pip and Poetry."""
    print()
    print("--- pip vs Poetry ---")
    print("pip:    installs into whatever environment is currently active")
    print("        version pinning is done manually via requirements.txt")
    print("        no automatic lock file (use 'pip freeze')")
    print("Poetry: creates and manages its own venv automatically")
    print("        pyproject.toml + poetry.lock guarantee reproducibility")
    print("        resolves dependency conflicts before installing")


def main() -> None:
    """Check dependencies, run analysis, generate visualization."""
    print("LOADING STATUS: Loading programs...")
    print()

    results = check_all_dependencies()
    print_dependency_status(results)

    if not all_dependencies_ok(results):
        print()
        print("Install missing packages before running:")
        print("  pip:    pip install -r requirements.txt")
        print("  Poetry: poetry install")
        sys.exit(1)

    print()
    print("Analyzing Matrix data...")
    time, zion, machines = generate_matrix_data()
    analyze_data(time, zion, machines)
    generate_visualization(time, zion, machines)
    show_pip_vs_poetry()


if __name__ == "__main__":
    main()
