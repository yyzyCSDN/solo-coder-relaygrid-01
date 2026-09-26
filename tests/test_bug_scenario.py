from relaygrid.models import Branch, Bus, FeederSnapshot
from relaygrid.restoration.backfeed import (
    SourceCapacity,
    TieCandidate,
    apply_transfers,
    choose_backfeeds,
)
from relaygrid.topology.radiality import connected_components, energized_edges


def test_normally_open_ties_and_shared_source_headroom_are_consistent():
    snapshot = FeederSnapshot(
        buses={name: Bus(name, 12.47) for name in ("S", "A", "B")},
        branches={
            "sa": Branch("sa", "S", "A", 0.1, 0.1, 300.0),
            "tie": Branch(
                "tie", "A", "B", 0.1, 0.1, 200.0,
                switchable=True, normally_closed=False,
            ),
        },
    )

    assert list(snapshot.closed_branches()) == [snapshot.branches["sa"]]
    assert [edge[0] for edge in energized_edges(snapshot)] == ["sa"]
    assert connected_components(snapshot) == [{"A", "S"}, {"B"}]

    source = SourceCapacity("S", normal_kw=80.0, current_kw=80.0, emergency_kw=100.0)
    candidates = [
        TieCandidate("T1", "S", 15.0, 40.0, 0.98, 0.1),
        TieCandidate("T2", "S", 15.0, 40.0, 0.98, 0.2),
    ]
    decisions = choose_backfeeds(candidates, {"S": source})

    assert [(d.tie_id, d.accepted) for d in decisions] == [("T1", True), ("T2", False)]
    assert "insufficient_capacity" in decisions[1].reasons
    applied, usage = apply_transfers(decisions, {"S": source}, {c.tie_id: c for c in candidates})
    assert applied == [("T1", 15.0)]
    assert usage == {"S": 95.0}
