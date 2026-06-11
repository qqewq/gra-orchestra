# GRA-Orchestra: Живой оркестр ИИ-агентов

[English](#english) | [Русский](#russian)

<a name="english"></a>
## English

### Principle
> **The orchestra encourages the foam of AI agents, but nullifies the foam in the orchestra.**

- **Local foam** (agent's inner contradictions, quirks, personality) – allowed and even encouraged.
- **Global foam** (collective falsehood, conflicts, broken goal) – nullified by GRA-Core.

This repository contains a full implementation: backend (FastAPI + GRA-Core), frontend dashboard, and a scientific paper (LaTeX).

### Quick start

```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py

# Frontend (any static server)
cd frontend
python -m http.server 3000
# or open index.html directly
```

Open http://localhost:3000 and http://localhost:8000/docs for API.

### Architecture
- `GRAOrchestra` class – maintains agents, computes global/local foam, performs GRA steps.
- Agents keep their local foam (character) > 0, only alignment error is minimized.
- Stability condition: Φ_global = 0, ΔΦ_global = 0, Δ²Φ_global > 0.

### API endpoints
- `GET /state` – current foam values, agent states, stability flag.
- `POST /step` – perform GRA nullification steps.
- `POST /connect` – connect a previously detached agent.
- `POST /disconnect/{id}` – remove agent from orchestra (its foam remains stored).

### Paper
See `paper.tex` – describes the hierarchical stability theory, local/global foam separation, and experimental results.

---

<a name="russian"></a>
## Русский

### Принцип
> **Оркестр поощряет пену ИИ‑агентов, но обнуляет пену в оркестре.**

- **Локальная пена** (внутренние противоречия агента, его «тараканы», характер) – разрешена и даже поощряется.
- **Глобальная пена** (общая фальшь, конфликты, нарушение цели) – обнуляется через GRA‑Core.

Репозиторий содержит полную реализацию: бекенд (FastAPI + GRA‑Core), фронтенд‑панель и научную статью (LaTeX).

### Быстрый старт

```bash
# Бекенд
cd backend
pip install -r requirements.txt
python app.py

# Фронтенд (простой сервер)
cd frontend
python -m http.server 3000
# или просто откройте index.html
```

Откройте http://localhost:3000 и http://localhost:8000/docs для API.

### Архитектура
- Класс `GRAOrchestra` – управляет агентами, вычисляет глобальную/локальную пену, выполняет GRA‑шаги.
- Агенты сохраняют локальную пену (характер) > 0, минимизируется только ошибка выравнивания.
- Условие стабильности: Φ_global = 0, ΔΦ_global = 0, Δ²Φ_global > 0.

### API endpoints
- `GET /state` – текущие значения пены, состояния агентов, флаг стабильности.
- `POST /step` – выполнить шаги обнуления GRA.
- `POST /connect` – подключить ранее отсоединённого агента.
- `POST /disconnect/{id}` – удалить агента из оркестра (его пена сохраняется).

### Статья
См. `paper.tex` – описание теории иерархической стабильности, разделения локальной/глобальной пены, экспериментальные результаты.
