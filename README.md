# PotyNews Backend

Backend enxuto em FastAPI para o app PotyNews. Persiste **apenas** usuários e estado do jogo — notícias e lugares vivem no frontend e são enviados como payload para endpoints stateless.

## Stack
- FastAPI + Uvicorn
- SQLAlchemy 2.0 async + asyncpg
- PostgreSQL 16
- Alembic (migrations)
- Poetry
- JWT (python-jose) + bcrypt (passlib)
- OpenRouter (structured output JSON Schema) para recomendações
- rapidfuzz para busca de notícias

## Como rodar (um comando só)

```bash
cd backend
cp .env.example .env   # edite OPENROUTER_API_KEY se quiser testar /discover/recommend com LLM real
docker compose up --build
```

A API sobe em `http://localhost:8000`. Migrations Alembic rodam automaticamente no boot.
Swagger UI: `http://localhost:8000/docs`.

## Endpoints

| Método | Rota | Auth |
|---|---|---|
| `POST` | `/auth/register` | – |
| `POST` | `/auth/login` | – |
| `GET`  | `/users/me` | ✅ |
| `POST` | `/game/submit` | ✅ |
| `GET`  | `/game/percentile` | ✅ |
| `GET`  | `/game/ranking` | ✅ |
| `POST` | `/discover/recommend` | ✅ |
| `POST` | `/news/search` | ✅ |
| `GET`  | `/health` | – |

### Notas
- **Login**: `identifier` aceita email (contém `@`) ou nickname.
- **Reset diário**: lazy — se `last_played_date != today`, `has_played_today` e `daily_score` são retornados zerados sem precisar de cron.
- **Submit**: rejeita 409 se o usuário já jogou hoje. Atualiza `streak_days` (+1 se jogou ontem, senão reinicia em 1).
- **/discover/recommend**: usa OpenRouter com `response_format=json_schema` (`{ranked_ids: [int]}`). Sem `OPENROUTER_API_KEY` ou erro/lista vazia → fallback de 3 lugares aleatórios.
- **/news/search**: usa `rapidfuzz.WRatio` em `title + summary`, cutoff 40.

## Estrutura

```
app/
├── api/routers/   # controllers
├── services/      # regras de negócio + integrações
├── repositories/  # queries SQLAlchemy
├── models/        # SQLAlchemy
├── schemas/       # Pydantic
└── core/          # config, db, security
```
