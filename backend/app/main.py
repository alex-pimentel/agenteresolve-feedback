"""FastAPI entrypoint for FeedbackClassifier (Agenteresolve)."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from . import tools
from .config import get_settings
from .jobs import store
from .providers import ProviderUnavailable

settings = get_settings()
app = FastAPI(title=f"Agenteresolve · {settings.tool_name}", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)

RESULT_DIR = Path(settings.results_dir)
RESULT_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/results", StaticFiles(directory=str(RESULT_DIR)), name="results")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "tool": settings.tool_slug}


async def _parse(request: Request) -> tools.ToolInput:
    content_type = request.headers.get("content-type", "")
    text = ""
    file_bytes: bytes | None = None
    filename: str | None = None
    params: dict[str, object] = {}
    if "multipart/form-data" in content_type:
        form = await request.form()
        for key, value in form.items():
            if hasattr(value, "read") and hasattr(value, "filename"):
                file_bytes = await value.read()
                filename = value.filename
                params["content_type"] = value.content_type
            else:
                params[key] = value
    else:
        body = await request.json()
        text = str(body.get("text", ""))
        params = {key: value for key, value in body.items() if key != "text"}
    return tools.ToolInput(
        text=text,
        file_bytes=file_bytes,
        filename=filename,
        content_type=str(params.get("content_type") or "") or None,
        params=params,
    )


@app.post("/api/{slug}/")
async def create_job(slug: str, request: Request) -> dict[str, str]:
    if slug != settings.tool_slug:
        raise HTTPException(status_code=404, detail="Ferramenta desconhecida.")
    tool_input = await _parse(request)
    job = store.create(slug)
    store.update(job.task_id, status="processing", progress=20)
    try:
        data, content_type, out_name = tools.run(tool_input)
    except ProviderUnavailable as exc:
        store.update(job.task_id, status="error", error=str(exc))
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001 - reported on the job
        store.update(job.task_id, status="error", error=f"{type(exc).__name__}: {exc}")
        return {"task_id": job.task_id, "tool": slug, "status": "error"}

    out_dir = RESULT_DIR / job.task_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / out_name).write_bytes(data)
    store.update(
        job.task_id,
        status="done",
        progress=100,
        result_url=f"/results/{job.task_id}/{out_name}",
    )
    return {"task_id": job.task_id, "tool": slug, "status": "done"}


@app.get("/api/{slug}/{task_id}")
def get_job(slug: str, task_id: str) -> JSONResponse:
    job = store.get(task_id)
    if job is None or job.tool != slug:
        raise HTTPException(status_code=404, detail="Job não encontrado.")
    return JSONResponse(
        {
            "task_id": job.task_id,
            "tool": job.tool,
            "status": job.status,
            "progress": job.progress,
            "result_url": job.result_url,
            "error": job.error,
        }
    )
