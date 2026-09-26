"""写 run：确认入账时按当前墙面/卷材重算卷数后写入历史表（与核销同事务）。"""

from app.repositories import history, rolls, walls
from app.services.receipt_confirm_view import drift_result_from_live


def write_run(conn, receipt: dict, note: str) -> int:
    import json

    pinned = json.loads(receipt["result_json"])
    wall = walls.get_wall(receipt["wall_id"], conn)
    roll = rolls.get_roll(receipt["roll_id"], conn)
    if wall and roll:
        result = drift_result_from_live(wall, roll, pinned)
    else:
        result = pinned
    return history.insert_run(receipt["wall_id"], receipt["roll_id"], result, note, conn=conn)
