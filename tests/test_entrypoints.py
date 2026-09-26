from __future__ import annotations

import importlib
import json
import pkgutil

import relaygrid
from relaygrid.cli import main


def test_public_package_exports_are_importable():
    assert relaygrid.__all__ == [
        "Branch",
        "Bus",
        "FeederSnapshot",
        "GridSimulator",
        "SwitchState",
        "TelemetrySample",
    ]
    for name in relaygrid.__all__:
        assert getattr(relaygrid, name) is not None


def test_cli_demo_returns_success(capsys):
    assert main(["demo"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "energized_after": 4,
        "energized_before": 3,
        "events": 1,
        "project": "RelayGrid",
        "switch": "cd",
        "switch_state": "closed",
    }


def test_all_shipped_modules_import():
    modules = sorted(
        item.name
        for item in pkgutil.walk_packages(
            relaygrid.__path__, relaygrid.__name__ + "."
        )
    )
    assert len(modules) >= 130
    for module in modules:
        importlib.import_module(module)
