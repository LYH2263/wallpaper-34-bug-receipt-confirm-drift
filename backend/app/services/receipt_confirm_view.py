"""Helpers for shaping receipt confirm payloads and write-path figures."""

from __future__ import annotations

import json


def pinned_result(receipt: dict) -> dict:
    """回执钉住的干算快照：确认写库与响应一律取该面值，不按当前实体重算。"""
    return json.loads(receipt["result_json"])
