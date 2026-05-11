import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

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
    parser.add_argument("--workers", type=int, default=os.cpu_count(), metavar="N", help="parallel worker processes; 1 = serial (default: all CPUs)")
    args = parser.parse_args()

    seeds = [args.seed + i for i in range(args.trials)]

    all_trials = []
    try:
        if args.workers == 1:
            for s in tqdm(seeds, desc="Running trials", unit="maze"):
                try:
                    all_trials.append(run_trial(args.size, s))
                except Exception as exc:
                    print(f"\nWarning: trial seed={s} failed: {exc}", file=sys.stderr)
        else:
            with ProcessPoolExecutor(max_workers=args.workers) as ex:
                futures = [ex.submit(run_trial, args.size, s) for s in seeds]
                for fut in tqdm(as_completed(futures), total=len(futures),
                                desc="Running trials", unit="maze"):
                    try:
                        all_trials.append(fut.result())
                    except Exception as exc:
                        print(f"\nWarning: a trial failed: {exc}", file=sys.stderr)
    except KeyboardInterrupt:
        print("\nInterrupted — computing partial results...", file=sys.stderr)

    if not all_trials:
        print("No trials completed.", file=sys.stderr)
        return

    stats = aggregate(all_trials)
    table = format_table(stats, n_trials=len(all_trials), maze_size=args.size)

    print(table)
    with open(args.log, "w") as f:
        f.write(table)
    print(f"Results written to {args.log}")


if __name__ == "__main__":
    main()
