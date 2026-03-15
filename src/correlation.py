import pandas as pd
from scipy import stats


def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Returns Pearson correlation matrix for the 3 indicators."""
    cols = ["poverty_rate", "grdp", "unemployment_rate"]
    return df[cols].corr(method="pearson").round(3)


def get_pearson_stats(df: pd.DataFrame) -> list[dict]:
    """
    Returns Pearson r and p-value for each indicator pair.
    Useful for displaying significance in the dashboard.
    """
    pairs = [
        ("poverty_rate", "grdp",             "Poverty vs GRDP"),
        ("poverty_rate", "unemployment_rate", "Poverty vs Unemployment"),
        ("grdp",         "unemployment_rate", "GRDP vs Unemployment"),
    ]

    results = []
    for x_col, y_col, label in pairs:
        r, p = stats.pearsonr(df[x_col], df[y_col])
        results.append({
            "pair":        label,
            "r":           round(r, 3),
            "p_value":     round(p, 4),
            "significant": "Yes ✅" if p < 0.05 else "No ❌",
            "strength":    interpret_r(r),
        })

    return results


def interpret_r(r: float) -> str:
    """Human-readable interpretation of Pearson r value."""
    abs_r = abs(r)
    direction = "positive" if r > 0 else "negative"

    if abs_r >= 0.8:
        strength = "Very strong"
    elif abs_r >= 0.6:
        strength = "Strong"
    elif abs_r >= 0.4:
        strength = "Moderate"
    elif abs_r >= 0.2:
        strength = "Weak"
    else:
        strength = "Very weak"

    return f"{strength} {direction}"