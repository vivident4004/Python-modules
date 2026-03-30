import sys
import importlib.util
from typing import Any


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Raw CSV from the Our World in Data CO2-data repository (GitHub).
# No authentication required.  Columns used: country, year, iso_code,
# population, gdp (Maddison Project Database 2023, 2011 int-$), co2.
DATA_URL = (
    "https://raw.githubusercontent.com/owid/"
    "co2-data/master/owid-co2-data.csv"
)

# Countries to compare in the GDP-per-capita time-series chart
COUNTRIES = [
    "United States",
    "Germany",
    "Japan",
    "China",
    "Brazil",
    "India",
]

# Year range for the time-series chart (data is sparser before 1950)
YEAR_START = 1950
YEAR_END = 2022

# The four packages this program depends on
REQUIRED_PACKAGES = ["pandas", "numpy", "matplotlib", "requests"]


# --------------------------------------------------------------------------- #
# Dependency check
# --------------------------------------------------------------------------- #

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


def all_ok(results: dict[str, tuple[bool, str]]) -> bool:
    """Return True only if every dependency is available."""
    return all(ok for ok, _ in results.values())


def print_dependency_status(
    results: dict[str, tuple[bool, str]]
) -> None:
    """Print one line per package showing its status and version."""
    print("Checking dependencies:")
    for pkg, (ok, info) in results.items():
        tag = "[OK]     " if ok else "[MISSING]"
        print(f"  {tag} {pkg} ({info})")


# --------------------------------------------------------------------------- #
# Data download
# --------------------------------------------------------------------------- #

def download_data() -> Any:
    """Download the OWID CSV and return it as a pandas DataFrame.

    Raises RuntimeError if the request fails so the caller can handle
    it gracefully without a bare traceback.
    """
    import requests
    import pandas as pd
    from io import StringIO

    print(f"Downloading data from:\n  {DATA_URL}")
    try:
        response = requests.get(DATA_URL, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Download failed: {e}") from e

    df = pd.read_csv(StringIO(response.text))
    print(f"  Downloaded {len(df):,} rows, {len(df.columns)} columns.")
    return df


# --------------------------------------------------------------------------- #
# Data preparation
# --------------------------------------------------------------------------- #

def prepare_data(df: Any) -> tuple[Any, Any]:
    """Return two clean DataFrames ready for plotting.

    Returns:
        time_series  -- GDP per capita for selected countries, 1950-2022
        scatter      -- GDP per capita vs CO2 per capita, latest year
    """
    import numpy as np

    # Drop aggregate rows added by OWID (continents, "World", etc.)
    # They have no ISO code, or the special code starting with "OWID_".
    countries = df[
        df["iso_code"].notna()
        & ~df["iso_code"].str.startswith("OWID_", na=False)
    ].copy()

    # Compute GDP per capita (gdp is total GDP in 2011 int-$)
    mask_gdp = countries["gdp"].notna() & countries["population"].notna()
    with_gdp = countries[mask_gdp].copy()
    with_gdp["gdp_per_capita"] = (
        with_gdp["gdp"] / with_gdp["population"]
    )

    # --- Time series: selected countries, YEAR_START to YEAR_END ---
    time_series = with_gdp[
        with_gdp["country"].isin(COUNTRIES)
        & with_gdp["year"].between(YEAR_START, YEAR_END)
    ][["country", "year", "gdp_per_capita"]].copy()

    # --- Scatter: all countries in the most recent year that has both
    #     gdp_per_capita and co2_per_capita populated ---
    scatter_cols = [
        "country", "year", "gdp_per_capita", "co2_per_capita"
    ]
    scatter_pool = with_gdp[
        with_gdp["co2_per_capita"].notna()
        & with_gdp["gdp_per_capita"].notna()
    ][scatter_cols].copy()

    latest_year = int(scatter_pool["year"].max())
    scatter = scatter_pool[scatter_pool["year"] == latest_year].copy()

    # Log-transform: GDP and CO2 per capita span orders of magnitude
    scatter["log_gdp_pc"] = np.log10(scatter["gdp_per_capita"])
    scatter["log_co2_pc"] = np.log10(scatter["co2_per_capita"])

    print(
        f"  Time-series: {len(time_series)} rows "
        f"({YEAR_START}–{YEAR_END}, {len(COUNTRIES)} countries)"
    )
    print(
        f"  Scatter:     {len(scatter)} countries "
        f"(latest year with data: {latest_year})"
    )
    return time_series, scatter


# --------------------------------------------------------------------------- #
# Summary statistics
# --------------------------------------------------------------------------- #

def print_summary(time_series: Any, scatter: Any) -> None:
    """Print brief descriptive statistics to stdout."""
    latest_year = int(time_series["year"].max())
    print()
    print(
        f"--- GDP per capita (2011 int-$) "
        f"in {latest_year} ---"
    )
    latest = (
        time_series[time_series["year"] == latest_year]
        .sort_values("gdp_per_capita", ascending=False)
    )
    for _, row in latest.iterrows():
        print(
            f"  {row['country']:<18}"
            f"${row['gdp_per_capita']:>10,.0f}"
        )

    print()
    print("--- Top 5 CO2 emitters per capita (scatter year) ---")
    for _, row in scatter.nlargest(5, "co2_per_capita").iterrows():
        print(
            f"  {row['country']:<20}"
            f"{row['co2_per_capita']:.1f} t/person"
        )


# --------------------------------------------------------------------------- #
# Chart 1 – GDP per capita time series
# --------------------------------------------------------------------------- #

def plot_gdp_time_series(time_series: Any) -> str:
    """Line chart: GDP per capita over time for selected countries.

    Returns the output filename.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(11, 6))

    for country, group in time_series.groupby("country"):
        group_sorted = group.sort_values("year")
        ax.plot(
            group_sorted["year"],
            group_sorted["gdp_per_capita"] / 1_000,  # → thousands
            label=country,
            linewidth=2,
        )

    ax.set_title(
        f"GDP per Capita ({YEAR_START}–{YEAR_END})\n"
        "Source: Maddison Project Database via Our World in Data",
        fontsize=13,
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("GDP per capita (thousands of 2011 int-$)")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    output = "gdp_per_capita.png"
    fig.savefig(output, dpi=150)
    plt.close(fig)
    return output


# --------------------------------------------------------------------------- #
# Chart 2 – CO2 per capita vs GDP per capita scatter
# --------------------------------------------------------------------------- #

def plot_co2_vs_gdp(scatter: Any) -> str:
    """Scatter: log10 GDP per capita vs log10 CO2 per capita.

    Both axes are log-transformed because values differ by orders of
    magnitude across countries.  Returns the output filename.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.scatter(
        scatter["log_gdp_pc"],
        scatter["log_co2_pc"],
        alpha=0.55,
        edgecolors="white",
        linewidths=0.4,
        s=45,
        color="steelblue",
    )

    # Label a handful of notable countries for reference
    highlight = {
        "United States", "China", "India", "Germany",
        "Nigeria", "Qatar", "Brazil", "Japan",
    }
    for _, row in scatter[scatter["country"].isin(highlight)].iterrows():
        ax.annotate(
            row["country"],
            (row["log_gdp_pc"], row["log_co2_pc"]),
            fontsize=7.5,
            xytext=(4, 2),
            textcoords="offset points",
        )

    latest_year = int(scatter["year"].max())
    ax.set_title(
        f"CO\u2082 vs GDP per Capita — {latest_year} (log\u2081\u2080 scale)\n"
        "Source: Our World in Data / Maddison Project Database",
        fontsize=13,
    )
    ax.set_xlabel("log\u2081\u2080 GDP per capita (2011 int-$)")
    ax.set_ylabel("log\u2081\u2080 CO\u2082 per capita (tonnes/person)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    output = "co2_vs_gdp.png"
    fig.savefig(output, dpi=150)
    plt.close(fig)
    return output


# --------------------------------------------------------------------------- #
# pip vs Poetry comparison
# --------------------------------------------------------------------------- #

def show_pip_vs_poetry() -> None:
    """Print a concise side-by-side comparison of pip and Poetry."""
    print()
    print("--- pip vs Poetry ---")
    print("pip:    installs into whatever environment is currently active")
    print("        version pinning is manual via requirements.txt")
    print("        no automatic lock file (use 'pip freeze')")
    print("Poetry: creates and manages its own venv automatically")
    print("        pyproject.toml + poetry.lock guarantee reproducibility")
    print("        resolves dependency conflicts before installing")


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def main() -> None:
    """Check dependencies, download data, analyse, and produce charts."""
    print("LOADING STATUS: Loading programs...")
    print()

    results = check_all_dependencies()
    print_dependency_status(results)

    if not all_ok(results):
        print()
        print("Install missing packages before running:")
        print("  pip:    pip install -r requirements.txt")
        print("  Poetry: poetry install")
        sys.exit(1)

    print()
    print("Downloading real-world data (Our World in Data / GitHub)...")
    try:
        df = download_data()
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    print()
    print("Preparing data...")
    time_series, scatter = prepare_data(df)

    print_summary(time_series, scatter)

    print()
    print("Generating charts...")
    f1 = plot_gdp_time_series(time_series)
    print(f"  Saved: {f1}")
    f2 = plot_co2_vs_gdp(scatter)
    print(f"  Saved: {f2}")

    show_pip_vs_poetry()

    print()
    print("Analysis complete.")


if __name__ == "__main__":
    main()