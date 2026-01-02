import pandas as pd
import matplotlib.pyplot as plt
import os

def instantiate_data(file: str, time_col=None) -> pd.DataFrame:
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
                raise Exception(f"{e}")
        case _: pass
    return df


def save_plot(plot: tuple[plt.Figure, plt.Axes], output_destination: str, filename: str) -> None:
    if not os.path.exists(output_destination):
        os.mkdir(output_destination)

    plot[0].savefig(
        fname=f"{output_destination}/{filename}",
        dpi="figure",
    )
