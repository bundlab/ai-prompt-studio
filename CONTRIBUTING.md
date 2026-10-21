# Contributing to AI Prompt Studio

Thank you for your interest in contributing to **AI Prompt Studio**!  
We welcome contributions of all kinds — bug reports, feature requests, documentation improvements, tests, and pull requests.

This document outlines how to get started, our coding standards, and the pull request process so that collaborating is smooth and consistent.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Guidelines](#issue-guidelines)
- [Community](#community)

---

## Code of Conduct

This project follows a simple principle: **be respectful, inclusive, and constructive**.

- Use welcoming and inclusive language.
- Be respectful of differing viewpoints and experiences.
- Accept constructive criticism gracefully.
- Focus on what is best for the community and the project.
- Show empathy toward other community members.

Harassment, discrimination, or unprofessional behavior will not be tolerated.  
By participating, you agree to uphold these standards.

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:

   ```bash
   git clone https://github.com/<your-username>/ai-prompt-studio.git
   cd ai-prompt-studio
   ```

3. Add the upstream remote:

   ```bash
   git remote add upstream https://github.com/<original-owner>/ai-prompt-studio.git
   ```

4. Create a new branch for your work:

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

---

## Development Setup

### Prerequisites

- **Python** 3.11+
- **Node.js** 20+ and npm / pnpm / yarn
- **Docker** & Docker Compose (recommended)
- **Git**

### Quick Start with Docker (Recommended)

```bash
# Copy environment file
cp .env.example .env

# Start all services (PostgreSQL + Backend + Frontend)
docker-compose up --build
```

- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:5173` (or the port defined in `docker-compose.yml`)
- API docs (Swagger): `http://localhost:8000/docs`

### Manual Setup

#### Backend (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # or: uv sync / poetry install

# Run migrations (if applicable)
# alembic upgrade head

# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (React + Vite / Next.js)

```bash
cd frontend
npm install          # or pnpm install / yarn
npm run dev
```

### Environment Variables

Copy `.env.example` to `.env` and fill in the required values:

```env
# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/ai_prompt_studio
SECRET_KEY=your-secret-key
# ... other variables
```

Never commit real secrets. Keep `.env` in `.gitignore`.

---

## Project Structure

```
ai-prompt-studio/
├── backend/                  # FastAPI
│   ├── app/
│   │   ├── api/             # routers: users.py, items.py, etc.
│   │   ├── core/            # config, security, dependencies
│   │   ├── crud/            # database operations
│   │   ├── models/          # SQLModel / Pydantic
│   │   ├── schemas/         # Pydantic models
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt / pyproject.toml
│   └── Dockerfile
├── frontend/                 # React (Vite or Next.js)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/ or app/
│   │   ├── hooks/
│   │   ├── services/        # API calls
│   │   ├── types/
│   │   └── main.tsx
│   ├── public/
│   ├── vite.config.ts / next.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .github/workflows/
├── .env.example
├── README.md
└── .gitignore
```

Please keep new code in the appropriate directory and follow existing patterns.

---

## How to Contribute

### Reporting Bugs

- Search existing issues first to avoid duplicates.
- Use the **Bug Report** issue template (if available).
- Include:
  - Clear title and description
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment (OS, browser, Python/Node versions)
  - Screenshots or logs when helpful

### Suggesting Features

- Open a **Feature Request** issue.
- Describe the problem the feature solves and a possible solution.
- Explain why it would be useful to the majority of users.

### Submitting Code

1. Fork → Clone → Create a feature/fix branch.
2. Make your changes.
3. Add or update tests.
4. Ensure the code passes linting and tests.
5. Update documentation if needed.
6. Commit with a clear message (see below).
7. Push and open a Pull Request against the `main` (or `develop`) branch.

---

## Coding Standards

### Backend (Python / FastAPI)

- Follow **PEP 8** and use a formatter (`ruff`, `black`, or `ruff format`).
- Prefer type hints everywhere.
- Use Pydantic models for request/response schemas.
- Keep routers thin; put business logic in services or CRUD layers.
- Write docstrings for public functions and classes.
- Avoid hardcoded secrets and magic numbers.

### Frontend (React / TypeScript)

- Use **TypeScript** strictly (`strict: true`).
- Prefer functional components and hooks.
- Keep components small and focused.
- Use consistent naming: `PascalCase` for components, `camelCase` for functions/variables.
- Place API calls in `services/` and prefer React Query / TanStack Query for data fetching.
- Follow the existing folder structure under `src/`.

### General

- Write self-documenting code; add comments only when the “why” is non-obvious.
- Keep pull requests focused — one logical change per PR is preferred.
- Do not commit generated files, `node_modules`, `.venv`, or `.env`.

---

## Commit Messages

We follow a conventional, readable style:

```
<type>(optional scope): <short summary>

[optional body]

[optional footer]
```

**Types:**

| Type       | Description                          |
|------------|--------------------------------------|
| `feat`     | New feature                          |
| `fix`      | Bug fix                              |
| `docs`     | Documentation only                   |
| `style`    | Formatting, missing semi-colons, etc.|
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test`     | Adding or correcting tests           |
| `chore`    | Build process, tooling, dependencies |

**Examples:**

```
feat(api): add prompt versioning endpoint
fix(frontend): correct infinite re-render in PromptEditor
docs: update contributing guidelines
chore(deps): bump fastapi to 0.115.0
```

---

## Pull Request Process

1. Ensure your branch is up to date with the target branch:

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Make sure all tests pass and the code is linted.
3. Fill out the Pull Request template (if present).
4. Link related issues with `Closes #123` or `Fixes #123`.
5. Request review from maintainers.
6. Address review feedback promptly.
7. Once approved and CI is green, a maintainer will merge.

**PR Checklist (recommended):**

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if needed)
- [ ] Tests added / updated and passing
- [ ] No new warnings or lint errors
- [ ] Commit messages follow conventions

---

## Testing

### Backend

```bash
cd backend
pytest                          # run all tests
pytest --cov=app --cov-report=term-missing
```

### Frontend

```bash
cd frontend
npm run test                    # or pnpm test / yarn test
npm run lint
npm run typecheck               # if available
```

Please add tests for new features and bug fixes. Aim for meaningful coverage rather than 100% at all costs.

---

## Documentation

- Update the `README.md` when you change setup steps, environment variables, or public APIs.
- Keep code comments and docstrings accurate.
- For significant architectural changes, consider adding or updating a short design note.

---

## Issue Guidelines

- Use clear, descriptive titles.
- Provide enough context for someone else to understand and reproduce the problem.
- Label issues appropriately when you have permission (`bug`, `enhancement`, `documentation`, etc.).
- Be patient — maintainers are volunteers / part-time.

---

## Community

- Be kind and constructive in issues and pull requests.
- If you have questions, open a Discussion (if enabled) or an issue tagged `question`.
- We appreciate every contribution, no matter how small.

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see the `LICENSE` file).

---

Thank you for helping make **AI Prompt Studio** better!  
We look forward to your contributions.
