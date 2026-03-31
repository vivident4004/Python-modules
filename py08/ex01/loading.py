import sys
import importlib.util
from typing import Any


REQUIRED_PACKAGES = ["pandas", "numpy", "matplotlib"]


def check_dependency(package_name: str) -> tuple[bool, str]:
    if importlib.util.find_spec(package_name) is None:
        return False, "not installed"
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, "__version__", "version unknown")
        return True, version
    except ImportError as e:
        return False, str(e)


def check_all_dependencies() -> dict[str, tuple[bool, str]]:
    return {pkg: check_dependency(pkg) for pkg in REQUIRED_PACKAGES}


def all_dependencies_ok(results: dict[str, tuple[bool, str]]) -> bool:
    return all(ok for ok, _ in results.values())


def print_dependency_status(results: dict[str, tuple[bool, str]]) -> None:
    print("Checking dependencies:")
    for pkg, (ok, info) in results.items():
        tag = "[OK]     " if ok else "[MISSING]"
        print(f"  {tag} {pkg} ({info})")


def generate_matrix_data() -> tuple[Any, Any, Any]:
    import numpy as np

    time = np.arange(0, 1000)
    zion = (
        np.sin(time * 0.05) * 50 + 50
        + np.random.normal(0, 3, 1000)
    )
    machines = (
        np.cos(time * 0.05) * 50 + 50
        + np.random.normal(0, 3, 1000)
    )
    return time, zion, machines


def analyze_data(time: Any, zion: Any, machines: Any) -> None:
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
    import matplotlib

    # Use a non-interactive backend: we want a file, not a GUI window
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    print("Generating visualization...")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(time, zion, label="Zion signal", color="green", alpha=0.8)
    ax.plot(
        time, machines,
        label="Machine signal", color="red", alpha=0.8
    )
    ax.set_title("Matrix signal analysis")
    ax.set_xlabel("Time")
    ax.set_ylabel("Signal strength")
    ax.legend()
    fig.tight_layout()

    output_file = "matrix_analysis.png"
    fig.savefig(output_file)
    plt.close(fig)

    print("\nAnalysis complete!")
    print(f"Results saved to: {output_file}")


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


if __name__ == "__main__":
    main()
