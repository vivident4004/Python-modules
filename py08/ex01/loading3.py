import sys
import importlib.util
from typing import Any


# =========================================================================== #
# Configuration
# =========================================================================== #

# GDP (Maddison Project 2023, 2011 int-$) — GitHub raw CSV
DATA_URL_GDP = (
    "https://raw.githubusercontent.com/owid/"
    "co2-data/master/owid-co2-data.csv"
)

# Gini coefficient (World Bank PIP) — OWID Grapher CSV
DATA_URL_GINI = (
    "https://ourworldindata.org/grapher/"
    "economic-inequality-gini-index.csv"
)

# Modern slavery prevalence (Walk Free / Global Slavery Index) — OWID Grapher
# NOTE: This survey is published every ~5 years, not annually.
# Years available: approx. 2013, 2016, 2018, 2021.
DATA_URL_SLAVERY = (
    "https://ourworldindata.org/grapher/"
    "share-of-population-in-modern-slavery.csv"
)

# Country highlighted in all European charts
HIGHLIGHT_COUNTRY = "Italy"
HIGHLIGHT_COLOR = "#009246"   # Italian green (tricolore)

# All European countries — OWID naming conventions
# Russia and Belarus are included (geographically European)
EUROPEAN_COUNTRIES = [
    "Albania", "Austria", "Belarus", "Belgium",
    "Bosnia and Herzegovina", "Bulgaria", "Croatia",
    "Cyprus", "Czechia", "Denmark", "Estonia",
    "Finland", "France", "Germany", "Greece",
    "Hungary", "Iceland", "Ireland", "Italy",
    "Kosovo", "Latvia", "Lithuania", "Luxembourg",
    "Malta", "Moldova", "Montenegro", "Netherlands",
    "North Macedonia", "Norway", "Poland", "Portugal",
    "Romania", "Russia", "Serbia", "Slovakia",
    "Slovenia", "Spain", "Sweden", "Switzerland",
    "Ukraine", "United Kingdom",
]

# Year range for time-series charts
YEAR_START = 1970
YEAR_END = 2023

REQUIRED_PACKAGES = ["pandas", "numpy", "matplotlib", "requests"]


# =========================================================================== #
# Dependency check
# =========================================================================== #

def check_dependency(package_name: str) -> tuple[bool, str]:
    """Return (available, version_or_error) for a package.

    Uses find_spec (no side effect) before importing, so the check works
    even when a package is missing.
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
    return {pkg: check_dependency(pkg) for pkg in REQUIRED_PACKAGES}


def all_ok(results: dict[str, tuple[bool, str]]) -> bool:
    return all(ok for ok, _ in results.values())


def print_dependency_status(results: dict[str, tuple[bool, str]]) -> None:
    print("Checking dependencies:")
    for pkg, (ok, info) in results.items():
        tag = "[OK]     " if ok else "[MISSING]"
        print(f"  {tag} {pkg} ({info})")


# =========================================================================== #
# Generic download helper
# =========================================================================== #

def download_csv(url: str, label: str) -> Any:
    """Download a CSV from url and return it as a pandas DataFrame.

    Raises RuntimeError on any network or HTTP error.
    """
    import requests
    import pandas as pd
    from io import StringIO

    print(f"  {label}: {url}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Download failed for {label}: {e}") from e

    df = pd.read_csv(StringIO(response.text))
    print(f"    → {len(df):,} rows, {len(df.columns)} columns")
    return df


def get_value_col(df: Any) -> str:
    """Return the first data column (i.e. not Entity / Code / Year).

    OWID Grapher CSVs always have Entity, Code, Year as the first
    three columns and then one or more indicator columns.
    """
    meta = {"Entity", "Code", "Year"}
    for col in df.columns:
        if col not in meta:
            return col
    raise ValueError(
        f"No value column found. Columns seen: {list(df.columns)}"
    )


# =========================================================================== #
# GDP analysis
# =========================================================================== #

def prepare_gdp(df: Any) -> Any:
    """Return a European time-series DataFrame with gdp_per_capita."""
    # Drop OWID aggregate rows (no iso_code or codes starting with OWID_)
    countries = df[
        df["iso_code"].notna()
        & ~df["iso_code"].str.startswith("OWID_", na=False)
    ].copy()

    # Derive GDP per capita
    mask = countries["gdp"].notna() & countries["population"].notna()
    with_gdp = countries[mask].copy()
    with_gdp["gdp_per_capita"] = with_gdp["gdp"] / with_gdp["population"]

    europe = with_gdp[
        with_gdp["country"].isin(EUROPEAN_COUNTRIES)
        & with_gdp["year"].between(YEAR_START, YEAR_END)
    ][["country", "year", "gdp_per_capita"]].copy()

    return europe


def print_gdp_summary(df: Any) -> None:
    latest = int(df["year"].max())
    print(f"\n--- GDP per capita (2011 int-$) in {latest} ---")
    snap = (
        df[df["year"] == latest]
        .sort_values("gdp_per_capita", ascending=False)
    )
    for _, row in snap.iterrows():
        marker = " ◀" if row["country"] == HIGHLIGHT_COUNTRY else ""
        print(
            f"  {row['country']:<25}"
            f"${row['gdp_per_capita']:>9,.0f}{marker}"
        )


def plot_gdp(df: Any) -> str:
    """Spaghetti plot: all European countries in grey, Italy in green."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(13, 7))

    for country, group in df.groupby("country"):
        g = group.sort_values("year")
        if country == HIGHLIGHT_COUNTRY:
            continue  # draw last so it appears on top
        ax.plot(
            g["year"],
            g["gdp_per_capita"] / 1_000,
            color="#aaaaaa",
            linewidth=0.8,
            alpha=0.6,
        )

    # Italy on top
    italy = df[df["country"] == HIGHLIGHT_COUNTRY].sort_values("year")
    if not italy.empty:
        ax.plot(
            italy["year"],
            italy["gdp_per_capita"] / 1_000,
            color=HIGHLIGHT_COLOR,
            linewidth=2.8,
            label=HIGHLIGHT_COUNTRY,
            zorder=5,
        )
        # Annotate the last data point
        last = italy.iloc[-1]
        ax.annotate(
            f"Italy\n${last['gdp_per_capita']/1_000:.0f}k",
            (last["year"], last["gdp_per_capita"] / 1_000),
            xytext=(6, 0),
            textcoords="offset points",
            fontsize=8,
            color=HIGHLIGHT_COLOR,
        )

    ax.set_title(
        f"GDP per Capita — European countries ({YEAR_START}–{YEAR_END})\n"
        "Source: Maddison Project Database via Our World in Data  "
        "| Grey = other European countries",
        fontsize=12,
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("GDP per capita (thousands of 2011 int-$)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    output = "gdp_per_capita.png"
    fig.savefig(output, dpi=150)
    plt.close(fig)
    return output


# =========================================================================== #
# Inequality (Gini) analysis
# =========================================================================== #

def prepare_gini(df: Any) -> tuple[Any, str]:
    """Return (European time-series DataFrame, gini_column_name)."""
    gini_col = get_value_col(df)

    europe = df[
        df["Entity"].isin(EUROPEAN_COUNTRIES)
        & df["Year"].between(YEAR_START, YEAR_END)
        & df[gini_col].notna()
    ][["Entity", "Year", gini_col]].copy()

    return europe, gini_col


def print_gini_summary(df: Any, gini_col: str) -> None:
    latest = int(df["Year"].max())
    print(f"\n--- Gini coefficient (most recent year ≤ {latest}) ---")
    # Use the latest available year per country (surveys are sporadic)
    snap = (
        df.sort_values("Year")
        .groupby("Entity")
        .last()
        .reset_index()
        .sort_values(gini_col)
    )
    for _, row in snap.iterrows():
        marker = " ◀" if row["Entity"] == HIGHLIGHT_COUNTRY else ""
        print(
            f"  {row['Entity']:<25}"
            f"{row[gini_col]:.3f}{marker}"
        )


def plot_gini(df: Any, gini_col: str) -> str:
    """Spaghetti plot: Gini coefficient over time, Italy highlighted."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(13, 7))

    for country, group in df.groupby("Entity"):
        g = group.sort_values("Year")
        if country == HIGHLIGHT_COUNTRY:
            continue
        ax.plot(
            g["Year"],
            g[gini_col],
            color="#aaaaaa",
            linewidth=0.8,
            alpha=0.6,
        )

    # Italy on top
    italy = df[df["Entity"] == HIGHLIGHT_COUNTRY].sort_values("Year")
    if not italy.empty:
        ax.plot(
            italy["Year"],
            italy[gini_col],
            color=HIGHLIGHT_COLOR,
            linewidth=2.8,
            label=HIGHLIGHT_COUNTRY,
            zorder=5,
        )
        last = italy.iloc[-1]
        ax.annotate(
            f"Italy\n{last[gini_col]:.3f}",
            (last["Year"], last[gini_col]),
            xytext=(6, 0),
            textcoords="offset points",
            fontsize=8,
            color=HIGHLIGHT_COLOR,
        )

    ax.set_title(
        f"Income Inequality (Gini) — European countries "
        f"({YEAR_START}–{YEAR_END})\n"
        "Source: World Bank PIP via Our World in Data  "
        "| 0 = perfect equality, 1 = perfect inequality",
        fontsize=12,
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Gini coefficient")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    output = "gini_europe.png"
    fig.savefig(output, dpi=150)
    plt.close(fig)
    return output


# =========================================================================== #
# Modern slavery analysis
# =========================================================================== #

def prepare_slavery(df: Any) -> tuple[Any, Any, str]:
    """Return (world_trend, europe_snapshot, slavery_col_name).

    The GSI is published every ~5 years so there are only 3-4 data
    points per country.  World trend uses the 'World' entity if present;
    otherwise it is None.
    """
    slavery_col = get_value_col(df)

    # World-level trend
    world = df[df["Entity"] == "World"][["Year", slavery_col]].dropna()
    if world.empty:
        world = None

    # European countries — most recent year available per country
    europe = df[
        df["Entity"].isin(EUROPEAN_COUNTRIES)
        & df[slavery_col].notna()
    ].copy()
    if not europe.empty:
        # Keep the most recent observation per country
        europe = (
            europe.sort_values("Year")
            .groupby("Entity")
            .last()
            .reset_index()
            .sort_values(slavery_col, ascending=False)
        )

    return world, europe, slavery_col


def print_slavery_summary(
    world: Any, europe: Any, slavery_col: str
) -> None:
    print("\n--- Modern slavery (share of population, %) ---")
    print("  NOTE: Global Slavery Index is published every ~5 years,")
    print("        so data points are sparse (2013, 2016, 2018, 2021).")
    if world is not None:
        print("\n  World trend:")
        for _, row in world.sort_values("Year").iterrows():
            print(
                f"    {int(row['Year'])}: {row[slavery_col]:.3f}%"
            )
    if europe is not None and not europe.empty:
        print("\n  European countries (most recent year available):")
        for _, row in europe.iterrows():
            marker = " ◀" if row["Entity"] == HIGHLIGHT_COUNTRY else ""
            print(
                f"    {row['Entity']:<25}"
                f"{row[slavery_col]:.3f}%{marker}"
            )


def plot_slavery(
    world: Any, europe: Any, slavery_col: str
) -> str:
    """Two-panel figure: world trend (top) + European bar chart (bottom).

    If world data is not available (no 'World' entity in the dataset)
    the top panel is skipped and only the European bar chart is shown.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    has_world = world is not None and not world.empty
    n_panels = 2 if has_world else 1
    fig_height = 5 * n_panels
    fig, axes = plt.subplots(n_panels, 1, figsize=(12, fig_height))
    # axes is always iterable even with a single panel
    if n_panels == 1:
        axes = [axes]

    # --- Panel 1: world trend (if available) ---
    if has_world:
        ax = axes[0]
        world_sorted = world.sort_values("Year")
        ax.plot(
            world_sorted["Year"],
            world_sorted[slavery_col],
            marker="o",
            linewidth=2,
            color="steelblue",
            markersize=7,
        )
        for _, row in world_sorted.iterrows():
            ax.annotate(
                f"{row[slavery_col]:.3f}%",
                (row["Year"], row[slavery_col]),
                xytext=(0, 8),
                textcoords="offset points",
                ha="center",
                fontsize=8,
            )
        ax.set_title(
            "Modern Slavery: World Trend (% of population)\n"
            "Source: Walk Free Global Slavery Index via Our World in Data",
            fontsize=11,
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Share of population (%)")
        ax.grid(True, alpha=0.3)

    # --- Panel 2: European bar chart ---
    if europe is not None and not europe.empty:
        ax = axes[-1]
        colors = [
            HIGHLIGHT_COLOR if c == HIGHLIGHT_COUNTRY else "#aaaaaa"
            for c in europe["Entity"]
        ]
        ax.barh(
            europe["Entity"],
            europe[slavery_col],
            color=colors,
            edgecolor="white",
            linewidth=0.5,
        )
        ax.set_title(
            "Modern Slavery: European Countries (most recent survey year)\n"
            "Source: Walk Free Global Slavery Index via Our World in Data",
            fontsize=11,
        )
        ax.set_xlabel("Share of population (%)")
        ax.invert_yaxis()
        ax.grid(True, alpha=0.3, axis="x")

    fig.tight_layout(pad=2.0)
    output = "slavery_world.png"
    fig.savefig(output, dpi=150)
    plt.close(fig)
    return output


# =========================================================================== #
# pip vs Poetry reminder
# =========================================================================== #

def show_pip_vs_poetry() -> None:
    print()
    print("--- pip vs Poetry ---")
    print("pip:    installs into whatever environment is currently active")
    print("        version pinning is manual via requirements.txt")
    print("        no automatic lock file (use 'pip freeze')")
    print("Poetry: creates and manages its own venv automatically")
    print("        pyproject.toml + poetry.lock guarantee reproducibility")
    print("        resolves dependency conflicts before installing")


# =========================================================================== #
# Entry point
# =========================================================================== #

def main() -> None:
    """Check dependencies, download three datasets, analyse, plot."""
    print("LOADING STATUS: Loading programs...")
    print()

    results = check_all_dependencies()
    print_dependency_status(results)

    if not all_ok(results):
        print()
        print("Install missing packages:")
        print("  pip:    pip install -r requirements.txt")
        print("  Poetry: poetry install")
        sys.exit(1)

    print()
    print("Downloading datasets...")

    try:
        df_gdp = download_csv(DATA_URL_GDP, "GDP (CO2-data repo)")
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    try:
        df_gini = download_csv(DATA_URL_GINI, "Gini (OWID Grapher)")
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    try:
        df_slavery = download_csv(DATA_URL_SLAVERY, "Modern slavery (OWID)")
    except RuntimeError as e:
        print(f"WARNING: {e}")
        df_slavery = None

    # --- GDP ---
    print("\nPreparing GDP data...")
    gdp = prepare_gdp(df_gdp)
    print_gdp_summary(gdp)
    f1 = plot_gdp(gdp)
    print(f"  Saved: {f1}")

    # --- Gini ---
    print("\nPreparing Gini data...")
    gini_df, gini_col = prepare_gini(df_gini)
    print(f"  Gini column: '{gini_col}'")
    print(f"  {len(gini_df)} observations across European countries")
    print_gini_summary(gini_df, gini_col)
    f2 = plot_gini(gini_df, gini_col)
    print(f"  Saved: {f2}")

    # --- Slavery ---
    print("\nPreparing modern slavery data...")
    if df_slavery is not None:
        world, europe, slavery_col = prepare_slavery(df_slavery)
        print(f"  Slavery column: '{slavery_col}'")
        print_slavery_summary(world, europe, slavery_col)
        f3 = plot_slavery(world, europe, slavery_col)
        print(f"  Saved: {f3}")
    else:
        print("  Skipped (download failed).")

    show_pip_vs_poetry()
    print()
    print("Analysis complete.")


if __name__ == "__main__":
    main()