from ingest import main as ingest_main
from process import main as process_main
from features import main as features_main

import argparse

def run_phase(func, phase_name):
    print(f"Running {phase_name}")

    try:
        print(f"Running {phase_name}")
        func()
    except Exception as e:
        print(f"Failed {phase_name}: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["all", "ingest", "process", "features"], default="all")
    args = parser.parse_args()

    if args.phase in ["ingest","all"]:
        run_phase(ingest_main, "ingest")
    elif args.phase in ["process","all"]:
        run_phase(process_main, "process")
    elif args.phase in ["features", "all"]:
        run_phase(features_main, "features")


if __name__ == "__main__":
    main()