import pandas as pd
import os

# Base path relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")


def load_poverty() -> pd.DataFrame:
    """Load and return poverty rate data."""
    path = os.path.join(RAW_DIR, "poverty.csv")
    df = pd.read_csv(path)
    return df


def load_gdp() -> pd.DataFrame:
    """Load and return GRDP data."""
    path = os.path.join(RAW_DIR, "gdp.csv")
    df = pd.read_csv(path)
    return df


def load_unemployment() -> pd.DataFrame:
    """Load and return unemployment rate data."""
    path = os.path.join(RAW_DIR, "unemployment.csv")
    df = pd.read_csv(path)
    return df


def load_merged() -> pd.DataFrame:
    """
    Merge all three datasets on region_code.
    Returns a single wide DataFrame with all indicators.
    """
    poverty = load_poverty()[["region_code", "region_name", "poverty_rate_2021"]]
    gdp = load_gdp()[["region_code", "grdp_2021"]]
    unemployment = load_unemployment()[["region_code", "unemployment_2021"]]

    df = poverty.merge(gdp, on="region_code")
    df = df.merge(unemployment, on="region_code")
    df = df.drop_duplicates(subset="region_code").reset_index(drop=True)

    # Rename for clarity
    df = df.rename(columns={
        "poverty_rate_2021": "poverty_rate",
        "grdp_2021": "grdp",
        "unemployment_2021": "unemployment_rate"
    })

    # Save processed copy
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df.to_csv(os.path.join(PROCESSED_DIR, "merged.csv"), index=False)

    return df


def get_region_list() -> list:
    """Return sorted list of region names."""
    df = load_merged()
    return sorted(df["region_name"].tolist())