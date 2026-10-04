"""Provider layer: OpenAI-compatible LLM and remote inference with URL + key."""

from __future__ import annotations

import httpx

from .config import get_settings


class ProviderUnavailable(RuntimeError):  # noqa: N818 - mirrors the platform naming
    """Raised when a required AI provider is not configured."""


def _llm_base() -> str | None:
    settings = get_settings()
    if settings.llm_base_url:
        return settings.llm_base_url.rstrip("/")
    if settings.llm_api_key:
        return "https://openrouter.ai/api/v1"
    return None


def llm_complete(prompt: str, system: str | None = None, temperature: float = 0.2) -> str:
    base = _llm_base()
    if not base:
        raise ProviderUnavailable("LLM não configurado. Defina LLM_API_KEY ou LLM_BASE_URL.")
    settings = get_settings()
    messages = ([{"role": "system", "content": system}] if system else []) + [
        {"role": "user", "content": prompt}
    ]
    payload = {"model": settings.llm_model, "temperature": temperature, "messages": messages}
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key or ''}",
        "Content-Type": "application/json",
    }
    with httpx.Client(timeout=settings.llm_timeout) as client:
        response = client.post(f"{base}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
    return str(data["choices"][0]["message"]["content"]).strip()


def remote_call(
    endpoint: str,
    *,
    files: dict[str, object] | None = None,
    data: dict[str, str] | None = None,
) -> httpx.Response:
    settings = get_settings()
    if not settings.inference_url:
        raise ProviderUnavailable("Inferência remota não configurada. Defina INFERENCE_URL.")
    headers = (
        {"Authorization": f"Bearer {settings.inference_key}"} if settings.inference_key else {}
    )
    url = settings.inference_url.rstrip("/") + endpoint
    with httpx.Client(timeout=300.0) as client:
        response = client.post(url, headers=headers, files=files, data=data)  # type: ignore[arg-type]
        response.raise_for_status()
        return response
