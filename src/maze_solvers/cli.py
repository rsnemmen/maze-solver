import argparse
import sys

from tqdm import tqdm

from .benchmark import run_trial, aggregate, format_table


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="maze-bench",
        description="Benchmark maze-solving algorithms across many randomly generated mazes.",
    )
    parser.add_argument("--trials", type=int, default=100, metavar="N", help="number of mazes to generate (default: 100)")
    parser.add_argument("--size", type=int, default=20, metavar="N", help="maze grid dimension N×N (default: 20)")
    parser.add_argument("--seed", type=int, default=0, help="base random seed; each trial uses seed+i (default: 0)")
    parser.add_argument("--log", default="benchmark_results.txt", metavar="FILE", help="path to write the results table (default: benchmark_results.txt)")
    args = parser.parse_args()

    all_trials = []
    for i in tqdm(range(args.trials), desc="Running trials", unit="maze"):
        all_trials.append(run_trial(args.size, args.seed + i))

    stats = aggregate(all_trials)
    table = format_table(stats, n_trials=args.trials, maze_size=args.size)

    print(table)
    with open(args.log, "w") as f:
        f.write(table)
    print(f"Results written to {args.log}")


if __name__ == "__main__":
    main()
