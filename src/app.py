import io
import os
import tempfile

from flask import Flask, jsonify, send_file, abort

# Ensure matplotlib writes cache to a writable temp directory (must be set before import).
if "MPLCONFIGDIR" not in os.environ:
    _mpl_dir = os.path.join(tempfile.gettempdir(), "matplotlib")
    os.makedirs(_mpl_dir, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = _mpl_dir

import matplotlib
matplotlib.use("Agg")  # non-GUI backend for headless/server environments
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# ------------------------------------------------------
# App setup
# ------------------------------------------------------

app = Flask(__name__)

DATA_PATH = os.environ.get("DATA_PATH", "cfb23.csv")

# cache the dataframe so we only read the csv once
_df_cache = None


def get_data() -> pd.DataFrame:
    """
    Load cfb23.csv into a pandas DataFrame (cached).
    Adjust DATA_PATH above if your file lives elsewhere.
    """
    global _df_cache
    if _df_cache is None:
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Could not find dataset at: {DATA_PATH}")
        _df_cache = pd.read_csv(DATA_PATH)
    return _df_cache


# Utility to make sure required columns exist
def require_columns(df: pd.DataFrame, cols):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        abort(400, description=f"Missing required column(s) in dataset: {missing}")


# ------------------------------------------------------
# Plot helpers
# (You can swap out the internals with your own graph code)
# ------------------------------------------------------

def _scatter_ppg_vs(df: pd.DataFrame, x_col: str, x_label: str = None, title: str = None) -> io.BytesIO:
    """
    Generic helper to build a scatter plot of Points Per Game vs x_col.

    Returns a BytesIO buffer containing the PNG image.
    """
    require_columns(df, ["Points Per Game", x_col])

    x = df[x_col]
    y = df["Points Per Game"]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y)

    ax.set_xlabel(x_label or x_col)
    ax.set_ylabel("Points Per Game")
    ax.set_title(title or f"Points Per Game vs {x_label or x_col}")

    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf


def plot_ppg_vs_pass_tds(df: pd.DataFrame) -> io.BytesIO:
    df["Points Per Game"] = pd.to_numeric(df["Points Per Game"], errors="coerce")
    df["Pass Touchdowns"] = pd.to_numeric(df["Pass Touchdowns"], errors="coerce")
    
    plot_df = df.dropna(subset=["Points Per Game", "Pass Touchdowns"])
    
    print(plot_df.shape)
    plt.figure(figsize=(8, 6))
    plt.scatter(
    plot_df["Points Per Game"],
    plot_df["Pass Touchdowns"],
    alpha=0.7
    )
    plt.xlabel("Points Per Game")
    plt.ylabel("Pass Touchdowns")
    plt.title("Points Per Game vs Pass Touchdowns (All Teams)")
    
    x_data = plot_df["Points Per Game"].values
    y_data = plot_df["Pass Touchdowns"].values
    
    coefficients = np.polyfit(x_data, y_data, 1)
    slope, intercept = coefficients
    
    correlation = np.corrcoef(x_data, y_data)[0, 1]
    
    line_x = np.array([x_data.min(), x_data.max()])
    line_y = slope * line_x + intercept
    plt.plot(line_x, line_y, 'r--', linewidth=2, label=f'Line of Best Fit (r={correlation:.3f})')
    plt.legend()
    plt.tight_layout()
    plt.show()
    return buf


def plot_ppg_vs_rush_tds(df: pd.DataFrame) -> io.BytesIO:
    df["Points Per Game"] = pd.to_numeric(df["Points Per Game"], errors="coerce")
    df["Rushing TD"] = pd.to_numeric(df["Rushing TD"], errors="coerce")
    
    plot_df = df.dropna(subset=["Points Per Game", "Rushing TD"])
    
    print(plot_df.shape)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(
    plot_df["Points Per Game"],
    plot_df["Rushing TD"],
    alpha=0.7
    )
    plt.xlabel("Points Per Game")
    plt.ylabel("Rushing TD")
    plt.title("Points Per Game vs Rush Touchdowns (All Teams)")
    
    x_data = plot_df["Points Per Game"].values
    y_data = plot_df["Rushing TD"].values
    
    coefficients = np.polyfit(x_data, y_data, 1)
    slope, intercept = coefficients
    
    correlation = np.corrcoef(x_data, y_data)[0, 1]
    
    line_x = np.array([x_data.min(), x_data.max()])
    line_y = slope * line_x + intercept
    plt.plot(line_x, line_y, 'r--', linewidth=2, label=f'Line of Best Fit (r={correlation:.3f})')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    return buf


def plot_ppg_vs_total_yds(df: pd.DataFrame) -> io.BytesIO:
    df["Points Per Game"] = pd.to_numeric(df["Points Per Game"], errors="coerce")
    df["Off Yards"] = pd.to_numeric(df["Off Yards"], errors="coerce")
    
    plot_df = df.dropna(subset=["Points Per Game", "Off Yards"])
    
    print(plot_df.shape)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(
    plot_df["Points Per Game"],
    plot_df["Off Yards"],
    alpha=0.7
    )
    plt.xlabel("Points Per Game")
    plt.ylabel("Off Yards")
    plt.title("Points Per Game vs Offense Yards (All Teams)")
    
    x_data = plot_df["Points Per Game"].values
    y_data = plot_df["Off Yards"].values
    coefficients = np.polyfit(x_data, y_data, 1)
    slope, intercept = coefficients
    
    correlation = np.corrcoef(x_data, y_data)[0, 1]
    
    line_x = np.array([x_data.min(), x_data.max()])
    line_y = slope * line_x + intercept
    plt.plot(line_x, line_y, 'r--', linewidth=2, label=f'Line of Best Fit (r={correlation:.3f})')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    return buf


def plot_ppg_vs_turnovers(df: pd.DataFrame) -> io.BytesIO:
    df["Points Per Game"] = pd.to_numeric(df["Points Per Game"], errors="coerce")
    df["Turnover Margin"] = pd.to_numeric(df["Turnover Margin"], errors="coerce")
    
    plot_df = df.dropna(subset=["Points Per Game", "Turnover Margin"])
    
    print(plot_df.shape)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(
    plot_df["Points Per Game"],
    plot_df["Turnover Margin"],
    alpha=0.7
    )
    plt.xlabel("Points Per Game")
    plt.ylabel("Turnover Margin")
    plt.title("Points Per Game vs Turnover Margin (All Teams)")
    
    x_data = plot_df["Points Per Game"].values
    y_data = plot_df["Turnover Margin"].values
    
    coefficients = np.polyfit(x_data, y_data, 1)
    slope, intercept = coefficients
    
    correlation = np.corrcoef(x_data, y_data)[0, 1]
    
    line_x = np.array([x_data.min(), x_data.max()])
    line_y = slope * line_x + intercept
    plt.plot(line_x, line_y, 'r--', linewidth=2, label=f'Line of Best Fit (r={correlation:.3f})')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    return buf


# ------------------------------------------------------
# Endpoints
# ------------------------------------------------------

@app.route("/api/stats", methods=["GET"])
def stats():
    """
    Summarize the dataset so users understand what they are looking at.
    Returns JSON with:
      - number of rows/columns
      - column names
      - basic numeric summary for key stats (including Points Per Game)
    """
    df = get_data()

    # Basic metadata
    n_rows = len(df)
    n_cols = df.shape[1]
    columns = list(df.columns)

    # Try to pull a numeric summary (describe) for a few main stats if present
    key_numeric_cols = [
        "Points Per Game",
        "Pass Touchdowns",
        "Rushing TD",
        "Off Yards",
        "Turnover Margin",
    ]
    numeric_cols_present = [c for c in key_numeric_cols if c in df.columns]

    numeric_summary = {}
    if numeric_cols_present:
        describe_df = df[numeric_cols_present].describe(include="all")
        # convert to native Python types for JSON
        numeric_summary = describe_df.to_dict()

    response = {
        "dataset_path": DATA_PATH,
        "n_rows": n_rows,
        "n_columns": n_cols,
        "columns": columns,
        "numeric_summary": numeric_summary,
    }
    return jsonify(response)


@app.route("/api/ppg-vs-pass-tds", methods=["GET"])
def ppg_vs_pass_tds_endpoint():
    """
    Returns a PNG graph comparing Points Per Game with Pass Touchdowns.
    """
    df["Points Per Game"] = pd.to_numeric(df["Points Per Game"], errors="coerce")
    df["Pass Touchdowns"] = pd.to_numeric(df["Pass Touchdowns"], errors="coerce")
    
    plot_df = df.dropna(subset=["Points Per Game", "Pass Touchdowns"])
    
    print(plot_df.shape)
    plt.figure(figsize=(8, 6))
    plt.scatter(
    plot_df["Points Per Game"],
    plot_df["Pass Touchdowns"],
    alpha=0.7
    )
    plt.xlabel("Points Per Game")
    plt.ylabel("Pass Touchdowns")
    plt.title("Points Per Game vs Pass Touchdowns (All Teams)")
    
    x_data = plot_df["Points Per Game"].values
    y_data = plot_df["Pass Touchdowns"].values
    
    coefficients = np.polyfit(x_data, y_data, 1)
    slope, intercept = coefficients
    
    correlation = np.corrcoef(x_data, y_data)[0, 1]
    
    line_x = np.array([x_data.min(), x_data.max()])
    line_y = slope * line_x + intercept
    plt.plot(line_x, line_y, 'r--', linewidth=2, label=f'Line of Best Fit (r={correlation:.3f})')
    plt.legend()
    plt.tight_layout()
    plt.show()
    return buf


@app.route("/api/ppg-vs-rush-tds", methods=["GET"])
def ppg_vs_rush_tds_endpoint():
    """
    Returns a PNG graph comparing Points Per Game with Rushing TD.
    """
    df["Points Per Game"] = pd.to_numeric(df["Points Per Game"], errors="coerce")
    df["Rushing TD"] = pd.to_numeric(df["Rushing TD"], errors="coerce")
    
    plot_df = df.dropna(subset=["Points Per Game", "Rushing TD"])
    
    print(plot_df.shape)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(
    plot_df["Points Per Game"],
    plot_df["Rushing TD"],
    alpha=0.7
    )
    plt.xlabel("Points Per Game")
    plt.ylabel("Rushing TD")
    plt.title("Points Per Game vs Rush Touchdowns (All Teams)")
    
    x_data = plot_df["Points Per Game"].values
    y_data = plot_df["Rushing TD"].values
    
    coefficients = np.polyfit(x_data, y_data, 1)
    slope, intercept = coefficients
    
    correlation = np.corrcoef(x_data, y_data)[0, 1]
    
    line_x = np.array([x_data.min(), x_data.max()])
    line_y = slope * line_x + intercept
    plt.plot(line_x, line_y, 'r--', linewidth=2, label=f'Line of Best Fit (r={correlation:.3f})')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    return buf


@app.route("/api/ppg-vs-total-yds", methods=["GET"])
def ppg_vs_total_yds_endpoint():
    """
    Returns a PNG graph comparing Points Per Game with Off Yards.
    """
    df["Points Per Game"] = pd.to_numeric(df["Points Per Game"], errors="coerce")
    df["Off Yards"] = pd.to_numeric(df["Off Yards"], errors="coerce")
    
    plot_df = df.dropna(subset=["Points Per Game", "Off Yards"])
    
    print(plot_df.shape)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(
    plot_df["Points Per Game"],
    plot_df["Off Yards"],
    alpha=0.7
    )
    plt.xlabel("Points Per Game")
    plt.ylabel("Off Yards")
    plt.title("Points Per Game vs Offense Yards (All Teams)")
    
    x_data = plot_df["Points Per Game"].values
    y_data = plot_df["Off Yards"].values
    coefficients = np.polyfit(x_data, y_data, 1)
    slope, intercept = coefficients
    
    correlation = np.corrcoef(x_data, y_data)[0, 1]
    
    line_x = np.array([x_data.min(), x_data.max()])
    line_y = slope * line_x + intercept
    plt.plot(line_x, line_y, 'r--', linewidth=2, label=f'Line of Best Fit (r={correlation:.3f})')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    return buf


@app.route("/api/ppg-vs-turnovers", methods=["GET"])
def ppg_vs_turnovers_endpoint():
    """
    Returns a PNG graph comparing Points Per Game with Turnover Margin.
    """
    df["Points Per Game"] = pd.to_numeric(df["Points Per Game"], errors="coerce")
    df["Turnover Margin"] = pd.to_numeric(df["Turnover Margin"], errors="coerce")
    
    plot_df = df.dropna(subset=["Points Per Game", "Turnover Margin"])
    
    print(plot_df.shape)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(
    plot_df["Points Per Game"],
    plot_df["Turnover Margin"],
    alpha=0.7
    )
    plt.xlabel("Points Per Game")
    plt.ylabel("Turnover Margin")
    plt.title("Points Per Game vs Turnover Margin (All Teams)")
    
    x_data = plot_df["Points Per Game"].values
    y_data = plot_df["Turnover Margin"].values
    
    coefficients = np.polyfit(x_data, y_data, 1)
    slope, intercept = coefficients
    
    correlation = np.corrcoef(x_data, y_data)[0, 1]
    
    line_x = np.array([x_data.min(), x_data.max()])
    line_y = slope * line_x + intercept
    plt.plot(line_x, line_y, 'r--', linewidth=2, label=f'Line of Best Fit (r={correlation:.3f})')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    return buf


@app.route("/health", methods=["GET"])
def health():
    """
    Simple health check endpoint.
    """
    return jsonify({"status": "ok"})


# ------------------------------------------------------
# Main entrypoint
# ------------------------------------------------------

if __name__ == "__main__":
    # Run locally with: python app.py
    # Then visit: http://127.0.0.1:5000/api/stats, /api/ppg-vs-pass-tds, etc.
    app.run(host="0.0.0.0", port=5000, debug=True)

