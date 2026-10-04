# FeedbackClassifier — Agenteresolve

> Classifique feedbacks por sentimento, tema e urgência.

[![CI](https://github.com/alex-pimentel/agenteresolve-feedback/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/alex-pimentel/agenteresolve-feedback/actions/workflows/ci.yml)
[![CodeQL](https://github.com/alex-pimentel/agenteresolve-feedback/actions/workflows/codeql.yml/badge.svg)](https://github.com/alex-pimentel/agenteresolve-feedback/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

Ferramenta de IA da plataforma Agenteresolve. O processamento é feito pelo **gateway da plataforma**
(`api.agenteresolve.com.br`) e o conteúdo é **efêmero** (expirado em 24h no Cloudflare R2). Nenhum
dado do usuário é persistido.

## Stack

- **Frontend:** Vite + React 19 + TypeScript + Tailwind CSS v4
- **UI:** `@agenteresolve/ui` (design system + Service Shell) + Clerk (login opcional)
- **API:** gateway da plataforma (`/api/feedback/`)
- **Deploy:** Cloudflare Pages (`agenteresolve-feedback`)

## Desenvolvimento

```bash
npm ci
npm run dev          # http://localhost:5173
```

Variáveis (`.env`):

| Var                          | Padrão                             | Descrição                         |
| ---------------------------- | ---------------------------------- | --------------------------------- |
| `VITE_API_BASE`              | `https://api.agenteresolve.com.br` | URL do gateway                    |
| `VITE_CLERK_PUBLISHABLE_KEY` | —                                  | chave pública do Clerk (opcional) |

## Qualidade

```bash
npm run lint && npm run format:check && npm run types
npm test && npm run test:coverage
npm run build
npm run test:e2e
```

Gates (CI): lint, format, tipos, testes unitários/integração, cobertura, build, e2e, auditoria de
dependências, gitleaks, Trivy, Semgrep e CodeQL. Padrão completo em
[`agenteresolve-ci`](https://github.com/alex-pimentel/agenteresolve-ci).

## Deploy

Merge em `main` dispara o deploy para o Cloudflare Pages (requer os secrets
`CLOUDFLARE_API_TOKEN` e `CLOUDFLARE_ACCOUNT_ID` no repositório).

```bash
npm run build
npx wrangler pages deploy dist --project-name=agenteresolve-feedback
```

## Licença

MIT © 2026 Agenteresolve.
