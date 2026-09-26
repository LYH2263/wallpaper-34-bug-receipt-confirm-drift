"""Helpers for shaping receipt confirm payloads and write-path figures."""

from __future__ import annotations

import json


def pinned_result(receipt: dict) -> dict:
    """确认写入与回执响应都使用签发时钉住的干算快照（回执面值），不按现行墙面/卷材重算。"""
    return json.loads(receipt["result_json"])
