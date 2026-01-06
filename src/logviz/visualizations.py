import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from termcolor import cprint


def generate_bar_graph(df: pd.DataFrame, filename: str, x_col: str, y_col: str) -> tuple[plt.Figure, plt.Axes]:
    """
    Returns a bar graph based on parameters passed at runtime
    """
    cprint(f"[-] Generating bar graph: {filename}")
    # ----- #
    df[x_col] = df[x_col].astype(str).str.strip()
    df[y_col] = df[y_col].astype(str).str.strip()

    counts = (
        df.groupby([x_col, y_col])
        .size()
        .reset_index(name="count")
    )
    pivot = counts.pivot(
        index=x_col, 
        columns=y_col,
        values='count'
    ).fillna(0)
    # sort by descending total y_col values
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]

    # plot
    
    width = max(12, 0.5 * len(pivot.index) + 6)
    fig, ax = plt.subplots(figsize=(width, 10), layout="constrained")
    pivot.plot(kind="bar", stacked=True, ax=ax)
    ax.set_title(f"Counts of {y_col} by {x_col}: {filename}")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.legend(title=y_col, bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.xticks(rotation=45, ha="right")
    return fig, ax


def generate_timeline(df: pd.DataFrame, timeline: dict[str, str], filename: str) -> tuple[plt.Figure, plt.Axes]:
    """
    Generates a timeline based on parameters passed at runtime
    timeline = {
        "time_column": str,
        "interval": int, # in minutes
        "data_column": str, # column of data to plot over time
    }
    """
    cprint(f"[-] Generating timeline: {filename}")

    # --- Format the dataframe ---
    df: pd.DataFrame = df.dropna(subset=[timeline["time_col"]])
    df[timeline["data_col"]] = df[timeline["data_col"]].astype("string").str.strip()

    by_action_15m = (
        df.groupby(by=[pd.Grouper(key=timeline["time_col"], freq=f"{timeline['interval']}min"), timeline["data_col"]])
        .size()
        .unstack(timeline["data_col"])
        .sort_index()
        .asfreq(f"{timeline['interval']}min", fill_value=0)
    )
    # --- Plot multiple lines on the same axes ---
    fig, ax = plt.subplots(figsize=(12, 5))
    for col in by_action_15m.columns:
        ax.step(
            x=by_action_15m.index, 
            y=by_action_15m[col], 
            where="post",
            label=col, 
            linewidth=1.0, 
        )
    # --- Plot total events
    total = by_action_15m.sum(axis=1)
    ax.plot(total.index, total.values, color="#6c6c6c", alpha=0.5, linewidth=1.2, label="Total")
    ax.set_title(f"{filename}: {timeline['interval']} Minutes by Action", pad=10)
    ax.set_ylabel("Count")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=6, maxticks=12))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d %H:%M"))
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=False, ncol=3)
    plt.tight_layout()
    return fig, ax


