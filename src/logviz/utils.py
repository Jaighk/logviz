import argparse
import os

from typing import Any

def parse_args(args: list[str]) -> dict[str, Any]:
    """
    Parses arguements passed in when the program is run
    """

    parser = argparse.ArgumentParser(
        prog="data-summarizer",
        description="A utility that ingests reports from various text-based raw-data formats such as logs, processes them, and returns a summary of the report",
    )
    _ = parser.add_argument(
        "-f",
        "--files", 
        required=True,
        nargs="*",
        type=str,
        help="path of the data file to summarize"
        )
    _ = parser.add_argument(
        "-t",
        "--timeline",
        nargs=3,
        type=str,
        help="Generates a timeline from the data set, optionally based on a count of unique values in a column.\nSyntax: -t {required: time column} {required: time bucket size (minutes)} {required: column to plot over time}"
    )
    _ = parser.add_argument(
        "-o",
        "--output_directory", 
        required=False,
        default="./plots",
        type=str,
        help="path of the directory to save the plots to"
        )
    return get_context(args=parser.parse_args())


def get_context(args: argparse.Namespace): 
    """
    Converts parser.parse_args Namespace to a dictionary for processing later
    """
    timeline= {}
    files = []
    for item in args.files:
        if os.path.isdir(item):
            for file in os.listdir(item):
                files.append(f"{item}/{file}")
        else:
            files.append(item)

    if args.timeline:
        timeline: dict[str, str]= {
            "time_col": args.timeline[0],
            "interval": args.timeline[1],
            "data_col": args.timeline[2],
        }
    return {
        "files": files,
        "timeline": timeline,
        "output_directory": args.output_directory
    }
