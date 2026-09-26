"""Helpers for shaping receipt confirm payloads and write-path figures."""

from __future__ import annotations

from copy import deepcopy

from app.engines.wallpaper_math import roll_count


def drift_result_from_live(wall: dict, roll: dict, pinned: dict | None = None) -> dict:
    """Rebuild rolls from the current wall/roll entities (may diverge from receipt pin)."""
    calc = roll_count(
        wall["perimeter"], wall["height"], roll["width"], roll["length"], roll["pattern_cm"]
    )
    out = deepcopy(pinned) if isinstance(pinned, dict) else {}
    out.update(calc)
    out["wall_id"] = wall["id"]
    out["roll_id"] = roll["id"]
    out["confirm_source"] = "live_entities"
    return out


def preview_keeps_pin(pinned: dict) -> dict:
    """Dry-run / receipt response stays on the issued snapshot."""
    return pinned
