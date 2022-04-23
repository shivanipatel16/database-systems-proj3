import sys
import pandas as pd


def valid_args(args):
    # TODO
    return True


def main():
    args = tuple(sys.argv[1:])

    # error message if the arguments are invalid
    if not valid_args(args):
        print("Invalid arguments.")
        print("Usage: python3 run.py INTEGRATED-DATASET.csv <min_sup> <min_conf>")
        return

    dataset_file, min_sup, min_conf = args
    min_sup = float(min_sup)
    min_conf = float(min_conf)

    df = pd.read_csv(dataset_file)
    print(df.head)
    print(df.columns)


if __name__ == "__main__":
    main()
