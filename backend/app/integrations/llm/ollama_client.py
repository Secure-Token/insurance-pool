import httpx
import json
import logging
from app.config import settings

logger = logging.getLogger(__name__)


async def assess_claim(claim):
    prompt = claim.get("evaluation_prompt")
    if not prompt:
        raise ValueError("evaluation_prompt missing; use evaluation_service")
    async with httpx.AsyncClient(timeout=settings.ollama_timeout) as client:
        response = await client.post(
            settings.ollama_base_url.rstrip("/") + "/api/generate",
            json={"model": settings.ollama_model, "prompt": prompt,
                  "stream": False, "format": "json",
                  "options": {"temperature": 0}},
        )
        response.raise_for_status()
        raw = response.json().get("response", "{}")
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error("Invalid Ollama JSON: %s", raw)
        raise ValueError("Ollama returned invalid JSON") from exc
    if not isinstance(result, dict):
        raise ValueError("Ollama output must be a JSON object")
    return result
