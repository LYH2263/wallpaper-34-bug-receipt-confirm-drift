"""写 run：确认入账时按回执钉住的干算结果写入历史表（与核销同事务）。"""

from app.repositories import history
from app.services.receipt_confirm_view import pinned_result


def write_run(conn, receipt: dict, note: str) -> int:
    result = pinned_result(receipt)
    return history.insert_run(receipt["wall_id"], receipt["roll_id"], result, note, conn=conn)
