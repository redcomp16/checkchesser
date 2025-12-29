def Filter_Players(players, *, name = None, min_rating = None, max_rating = None, school = None, grade = None,):
    results = players.values()

    if name:
        q = name.lower()
        results = [p for p in results if p.name.lower().startswith(q) or p.name.lower().split()[-1].startswith(q)]

    if min_rating is not None:
        results = [p for p in results if p.live_rating is not None and p.live_rating >= min_rating]

    if max_rating is not None:
        results = [p for p in results if p.live_rating is not None and p.live_rating <= max_rating]

    if school:
        results = [p for p in results if p.school == school]

    if grade:
        results = [p for p in results if p.grade == grade]

    return list(results)