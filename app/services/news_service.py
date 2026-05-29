from rapidfuzz import fuzz, process

from app.schemas.news import NewsSearchIn, NewsSearchOut


async def search(data: NewsSearchIn) -> NewsSearchOut:
    if not data.items:
        return NewsSearchOut(results=[])

    haystack = {idx: f"{n.title} {n.summary or ''}".strip() for idx, n in enumerate(data.items)}
    matches = process.extract(
        data.query,
        haystack,
        scorer=fuzz.WRatio,
        limit=data.limit,
        score_cutoff=40,
    )
    results = [data.items[idx].model_dump() for _text, _score, idx in matches]
    return NewsSearchOut(results=results)
