import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

from termcolor import cprint

from logviz.utils import (
    parse_args,
    check_validity,
)

from logviz.data_processing import(
    instantiate_data,
    save_plot,
)

from logviz.visualizations import (
    generate_timeline,
    generate_bar_graph,
)

def main() -> None:
    """
    App entry point
    """
    cprint("[-] Generating plots...")
    args = parse_args(args=sys.argv)
    save_file: dict[str, str] = {
        "name": "",
        "graph_type": "",
    }



    for file in args["files"]: 
        cprint(f"[-] Working: {file}")
        if not check_validity(file):
            continue

        if args["timeline"]:
            df: pd.DataFrame = instantiate_data(
                            file=file, 
                            time_col=args["timeline"]["time_col"]
                        )
        else:
            df: pd.DataFrame = instantiate_data(file)

        try: 
            if args["timeline"]:
                save_file = {
                    "name": os.path.basename(file).split(sep=".")[0],
                    "graph_type": "timeline"
                }
                new_timeline: tuple[plt.Figure, plt.Axes] = generate_timeline(
                    df=df, 
                    timeline=args["timeline"], 
                    filename=save_file["name"]
                )
                save_plot(
                    plot=new_timeline,
                    output_destination=args["output_directory"], 
                    save_file=save_file
                )
            if args["bar"]:
                cprint(f"{args['bar'] = }")
                save_file = {
                    "name": os.path.basename(file).split(sep=".")[0],
                    "graph_type": 'bar'
                }
                new_histogram: plt.Axes = generate_bar_graph(
                    df=df, 
                    filename=save_file["name"],
                    x_col=args["bar"]["x"],
                    y_col=args["bar"]["y"],
                )
                save_plot(
                    plot=(new_histogram),
                    output_destination=args["output_directory"],
                    save_file=save_file
                )
        except Exception as e:
            cprint(f"[X] {e}", color="red", attrs=["bold"])
            continue

    cprint("[\u2713] Plot generation complete", color="green")
    cprint(f"[\u2713] Plots saved at: {os.path.abspath(args['output_directory'])}", color="green")
        

if __name__ == "__main__":
    main()
