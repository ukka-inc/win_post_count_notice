def gen_time_schedule(post_count: int) -> dict[str, int] | None:
    # 所要時間(分)
    total_time = 30

    if not post_count:
        return None

    # 1ポストあたりの所要時間を求める
    time_per_post = total_time / post_count

    return {"minutes": int(time_per_post), "seconds": int((time_per_post % 1) * 60)}
