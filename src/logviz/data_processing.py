import pandas as pd
import matplotlib.pyplot as plt
import os

from termcolor import cprint

def instantiate_data(file: str, time_col: str) -> pd.DataFrame:
    """
    Generates and returns the pd.DataFrame from the specified file
    """

    file_type: str = file.split(sep=".")[-1]
    df: pd.DataFrame = pd.DataFrame()
    match file_type:
        case "csv":
            try: 
                if time_col:
                    df: pd.DataFrame = pd.read_csv(
                        file,
                        parse_dates=[time_col],
                    )
            except Exception as e:
                cprint(f"{e}", color="red", attrs=["bold"])
        case _: pass
    cprint(f"[\u2713] Data from file: {file}, processed", color="green")
    return df


def save_plot(plot: tuple[plt.Figure, plt.Axes], output_destination: str, save_file: dict[str, str]) -> None:
    """
    Saves generated plots to specified output_desitnation
    """

    try: 
        if not os.path.exists(output_destination):
            os.mkdir(output_destination)
        destination_path: str = f"{output_destination}{save_file['name']}_{save_file['graph_type']}"
        plot[0].savefig(
            fname=destination_path,
            dpi="figure",
        )
        cprint(f"[\u2713] Plot saved: {destination_path}", color="green")
    except Exception as e:
        cprint(f"[X] {e}", color="red", attrs=["bold"])

