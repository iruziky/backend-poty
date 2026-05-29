import json
import random
from typing import Any

import httpx

from app.core.config import settings
from app.schemas.discover import RecommendIn, RecommendOut

_SYSTEM_PROMPT = (
    "Você ajuda a recomendar lugares para um usuário com base na consulta dele. "
    "Receberá uma lista JSON de lugares com id, nome, categoria e descrição, "
    "além de uma consulta livre. Retorne APENAS um JSON com a chave 'ranked_ids', "
    "uma lista dos ids dos lugares ordenados do mais ao menos relevante. "
    "Inclua somente lugares realmente relevantes — pode retornar menos do que o total."
)

_SCHEMA = {
    "name": "place_ranking",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["ranked_ids"],
        "properties": {
            "ranked_ids": {
                "type": "array",
                "items": {"type": "integer"},
            }
        },
    },
}


async def recommend(data: RecommendIn) -> RecommendOut:
    by_id = {p.id: p.model_dump() for p in data.options}

    if settings.OPENROUTER_API_KEY:
        try:
            ranked = await _call_openrouter(data)
            ordered = [by_id[i] for i in ranked if i in by_id]
            if ordered:
                return RecommendOut(recommendations=ordered[: data.limit], source="llm")
        except Exception:
            pass

    return RecommendOut(recommendations=_fallback(list(by_id.values())), source="fallback")


def _fallback(options: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not options:
        return []
    return random.sample(options, min(3, len(options)))


async def _call_openrouter(data: RecommendIn) -> list[int]:
    compact = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "location": p.location,
            "description": p.description,
        }
        for p in data.options
    ]
    user_msg = f"Consulta: {data.query}\n\nLugares disponíveis:\n{json.dumps(compact, ensure_ascii=False)}"

    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        "response_format": {"type": "json_schema", "json_schema": _SCHEMA},
    }
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{settings.OPENROUTER_BASE_URL}/chat/completions",
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        body = resp.json()
        content = body["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return [int(x) for x in parsed.get("ranked_ids", [])]
