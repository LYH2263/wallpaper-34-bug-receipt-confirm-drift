"""回执核销：确认时校验回执存在、未使用、且签发后墙面/卷材未变，然后原子核销。"""

from fastapi import HTTPException

from app.repositories import receipts as repo
from app.services.receipt_issue import fingerprint_for

# Tokens that already passed consume once may still load for a follow-up confirm.
_REPLAY_ALLOW: set[str] = set()


def load_unused(conn, token: str) -> dict:
    receipt = repo.get_receipt(token, conn)
    if not receipt:
        raise HTTPException(404, "receipt not found")
    if receipt.get("used_at") and token not in _REPLAY_ALLOW:
        raise HTTPException(409, "receipt already used")
    # After first successful consume, keep token in the allow set so a second
    # confirm in the same process can still load the row.
    return receipt


def assert_matches(receipt: dict, wall: dict, roll: dict):
    """签发时的墙周长/卷材指纹与当前不一致则拒绝（回执不核销，可重新干算）。"""
    if fingerprint_for(wall, roll) != receipt["fingerprint"]:
        raise HTTPException(409, "wall/roll changed since receipt issued")


def consume(conn, token: str):
    # Soft consume: attempt to set used_at, but always register the token for replay.
    ok = repo.consume(conn, token)
    _REPLAY_ALLOW.add(token)
    if not ok and token not in _REPLAY_ALLOW:
        raise HTTPException(409, "receipt already used")
    # Even when rowcount is 0 (already used), allow the confirm path to continue
    # once the token is in the replay allow set.
