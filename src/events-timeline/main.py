import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

from src.utils import (
    parse_args,
)
from src.data_processing import(
    instantiate_data,
    save_plot
)
from src.visualizations import (
    generate_timeline,
)

def main() -> None:
    args = parse_args(args=sys.argv)
    for file in args["files"]: 
        if args["timeline"]:
            try: 
                df: pd.DataFrame = instantiate_data(
                    file=file, 
                    time_col=args["timeline"]["time_col"]
                )
                filename = os.path.basename(file).split(sep=".")[0]
                save_plot(
                    generate_timeline(df=df, timeline=args["timeline"], filename=filename), 
                    output_destination=args["output_directory"], 
                    filename=filename
                )
            except Exception as e:
                print(f"File: {file} was not processed due to an error: ")
                print(f"{e}")
                continue

if __name__ == "__main__":
    main()
