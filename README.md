# FeedbackClassifier — Agenteresolve

> Classifique feedbacks por sentimento, tema e urgência.

[![CI](https://github.com/alex-pimentel/agenteresolve-feedback/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/alex-pimentel/agenteresolve-feedback/actions/workflows/ci.yml)
[![CodeQL](https://github.com/alex-pimentel/agenteresolve-feedback/actions/workflows/codeql.yml/badge.svg)](https://github.com/alex-pimentel/agenteresolve-feedback/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

Projeto **full-stack** do serviço `feedback` da Agenteresolve: interface web + API + integração de IA.
Processamento **efêmero** (sem persistir conteúdo do usuário).

## Estrutura

```
feedback/
├── frontend/   # Vite + React 19 + TypeScript + Tailwind v4 + @agenteresolve/ui
├── backend/    # FastAPI + provider de LLM (OpenAI-compatible) e inferência remota
├── deploy/     # nginx (serve o frontend e faz proxy de /api e /results)
└── docker-compose.yml
```

## Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env        # defina LLM_API_KEY (OpenRouter) ou LLM_BASE_URL
uvicorn app.main:app --reload --port 8000
```

Endpoints: `GET /health`, `POST /api/feedback/` (JSON `{text, ...}` ou multipart `file`),
`GET /api/feedback/{task_id}`, `GET /results/...`.

## Frontend

```bash
cd frontend
npm ci
npm run dev     # http://localhost:5173 (VITE_API_BASE aponta para o backend)
```

## Docker

```bash
docker compose up --build   # http://localhost:8080
```

## IA / provedores

| Capacidade | Variável | Observação |
| --- | --- | --- |
| LLM (texto) | `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL` | OpenAI-compatible; padrão OpenRouter |
| Visão/Áudio (inferência) | `INFERENCE_URL` / `INFERENCE_KEY` | endpoint remoto (ex.: outra VPS/GPU) |

Sem provedor configurado, a API responde `503 provider_unavailable` de forma clara.

## Qualidade

`frontend`: lint, format, types, testes (Vitest), e2e (Playwright), cobertura, build.
`backend`: ruff, mypy, bandit, pytest com cobertura, pip-audit.
Segurança: gitleaks, Trivy, Semgrep, CodeQL. Padrão em
[`agenteresolve-ci`](https://github.com/alex-pimentel/agenteresolve-ci).

## Deploy

- **Frontend:** Cloudflare Pages (`agenteresolve-feedback`) via workflow `deploy.yml`.
- **Backend:** container Docker (Coolify). Configure `LLM_*`/`INFERENCE_*` como env vars.

## Licença

MIT © 2026 Agenteresolve.
