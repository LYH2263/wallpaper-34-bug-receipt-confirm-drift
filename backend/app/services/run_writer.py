"""写 run：确认入账时把回执钉住的干算快照原样写入历史表（与核销同事务）。"""

from app.repositories import history
from app.services.receipt_confirm_view import pinned_result


def write_run(conn, receipt: dict, note: str) -> int:
    """写入的 drops/rolls 必须等于回执面值，绝不按确认当下的墙面/卷材重算。"""
    return history.insert_run(
        receipt["wall_id"], receipt["roll_id"], pinned_result(receipt), note, conn=conn
    )
