from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from relaygrid.models import Branch, Bus, FeederSnapshot, SwitchState
from relaygrid.sim.engine import GridSimulator


def demo_summary() -> dict[str, object]:
    """Run a deterministic switching example and return its public summary."""
    buses = {bus_id: Bus(bus_id, 12.47) for bus_id in "ABCD"}
    branches = {
        "ab": Branch("ab", "A", "B", 0.1, 0.1, 300.0),
        "bc": Branch("bc", "B", "C", 0.1, 0.1, 300.0),
        "cd": Branch("cd", "C", "D", 0.1, 0.1, 300.0, True, False),
        "ad": Branch("ad", "A", "D", 0.1, 0.1, 300.0, True, False),
    }
    snapshot = FeederSnapshot(
        buses,
        branches,
        {"cd": SwitchState.OPEN, "ad": SwitchState.OPEN},
    )
    simulator = GridSimulator(snapshot)
    energized_before = simulator.energized_bus_count()
    simulator.operate_switch("cd", SwitchState.CLOSED)
    return {
        "energized_after": simulator.energized_bus_count(),
        "energized_before": energized_before,
        "events": len(simulator.log.events),
        "project": "RelayGrid",
        "switch": "cd",
        "switch_state": snapshot.switch_state["cd"].value,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="relaygrid")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("demo", help="run a deterministic feeder demo")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "demo":
        print(json.dumps(demo_summary(), sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
